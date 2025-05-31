from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify, session, g, abort
from flask_login import login_required, current_user
from app.models import HHQResponse, db, Client
from app.forms import HHQForm
from app import db
import uuid
from datetime import datetime, timedelta
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import secrets
from flask_wtf import FlaskForm
from wtforms import SubmitField
from app.utils.mail_utils import send_hhq_invitation
from app.utils.supabase_client import (
    fetch_clients, 
    fetch_hhq_by_token, 
    fetch_client_by_id, 
    fetch_health_history_questions, 
    upsert_individual_hhq_answers, 
    fetch_hhq_responses_dict,
    fetch_hhq_responses_dict_for_attempt,
    create_hhq_attempt,
    upsert_hhq_answers_partial
)

bp = Blueprint('hhq', __name__, url_prefix='/hhq')

# Section titles for the HHQ form
SECTION_TITLES = [
    "Dementia Prevention Client- No diagnosis of dementia", "Has a Diagnosis of Dementia", "Family History", "Head Trauma",
    "History of Headaches", "Social History", "Cardiovascular Health", "Respiratory Health", "Gastrointestinal Health",
    "History of Infectious Disease", "History of Skin Health", "History of Autoimmunity", "Sleep History", "Diabetes Health History",
    "Dental History", "Female Hormone Health", "Male Hormone Health History", "Surgical History", "Mental Health History",
    "History of Cancer or Chemotherapy", "Potential Risk for Mold Toxin Exposure",
    "Potential Risk for Chemical or Metal Exposure", "Muscle and Skeletal Health", "Use of Supplements"
]

def validate_section(form, section):
    """Validate responses for a given section."""
    # Get all questions for this section
    questions = fetch_health_history_questions()
    section_questions = [q for q in questions if q.get('section', 'Unknown') == section]
    
    # Skip validation for gender-specific sections based on client's sex
    client = fetch_client_by_id(g.hhq_response.get('client_id'))
    if not client:
        return True
        
    client_sex = client.get('sex', '').lower()
    
    if section == 'Female Hormone Health' and client_sex != 'female':
        return True
    if section == 'Male Hormone Health History' and client_sex != 'male':
        return True
    
    # Validate each question in the section
    for question in section_questions:
        variable_name = question.get('variable_name')
        if not variable_name:
            continue
            
        form_field_name = variable_name.replace('-', '_')
        if not hasattr(form, form_field_name):
            continue
            
        field = getattr(form, form_field_name)
        
        # Skip validation for optional fields
        if not question.get('required', False):
            continue
            
        # Validate required fields
        if not field.data:
            field.errors.append(f"This field is required")
            return False
            
        # Add any additional validation rules here
        if question.get('validation_rules'):
            for rule in question['validation_rules']:
                if not validate_field_rule(field.data, rule):
                    field.errors.append(f"Invalid value: {rule.get('message', 'Invalid input')}")
                    return False
    
    return True

def validate_field_rule(value, rule):
    """Validate a field value against a specific rule."""
    rule_type = rule.get('type')
    
    if rule_type == 'boolean':
        return isinstance(value, bool)
    elif rule_type == 'date':
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except (ValueError, TypeError):
            return False
    elif rule_type == 'number':
        try:
            num = float(value)
            min_val = rule.get('min')
            max_val = rule.get('max')
            if min_val is not None and num < min_val:
                return False
            if max_val is not None and num > max_val:
                return False
            return True
        except (ValueError, TypeError):
            return False
    elif rule_type == 'text':
        min_len = rule.get('min_length')
        max_len = rule.get('max_length')
        if min_len is not None and len(str(value)) < min_len:
            return False
        if max_len is not None and len(str(value)) > max_len:
            return False
        return True
    
    return True  # Unknown rule type, assume valid

def get_section_fields(section_name):
    """Get all fields that belong to a specific section."""
    questions = fetch_health_history_questions()
    section_questions = [q for q in questions if q.get('section', 'Unknown') == section_name]
    return [q['variable_name'] for q in sorted(section_questions, key=lambda q: int(q.get('question_order', 0)))]

class GenerateHHQForm(FlaskForm):
    """Simple form for CSRF protection."""
    pass

@bp.before_request
def load_hhq_response():
    if 'token' in request.view_args:
        token = request.view_args['token']
        hhq = fetch_hhq_by_token(token)
        if not hhq:
            abort(404)
        g.hhq_response = hhq

@bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate_link():
    print("🧠 REACHED: generate_link route")
    form = GenerateHHQForm()
    print("DEBUG: Method:", request.method)
    if request.method == 'POST':
        print("DEBUG: POST form data:", request.form)
        client_id = request.form.get('client_id')
        print("DEBUG: client_id:", client_id)
        if not client_id:
            print("DEBUG: No client_id provided")
            flash('Client ID is required.', 'error')
            return redirect(url_for('clients.index'))
        
        # Create a simple record to track that HHQ was generated for this client
        # No need to create empty aggregate row anymore
        print("DEBUG: HHQ link generated for client", client_id)
        flash('HHQ link has been generated successfully. You can now direct the client to fill out their questionnaire.', 'success')
        return redirect(url_for('clients.view', id=client_id))
    client_id = request.args.get('client_id')
    print("DEBUG: GET client_id:", client_id)
    return render_template('hhq/generate.html', client_id=client_id, form=form)

@bp.route('/<client_id>/hhq', methods=['GET', 'POST'])
def hhq_form(client_id):
    # Get client info first for gender filtering
    client = fetch_client_by_id(client_id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('main.index'))
    
    form = HHQForm()
    print(f"DEBUG: form data after instantiation: {[ (f, getattr(form, f).data) for f in form._fields ]}")
    
    # Get all questions and organize by section
    questions = fetch_health_history_questions()
    if not questions:
        flash('Unable to load questionnaire questions. Please try again later.', 'error')
        return redirect(url_for('main.index'))

    # Group questions by section - keep section as text, map to numeric index
    sections = {}
    section_names = []
    for question in questions:
        section_name = question.get('section', 'Unknown')
        if section_name not in sections:
            sections[section_name] = []
            section_names.append(section_name)
        sections[section_name].append(question)
    
    # Filter out gender-specific sections based on client's sex
    client_sex = client.get('sex', '').lower()
    print(f"DEBUG: Client sex: {client_sex}")
    print(f"DEBUG: Available sections before filtering: {section_names}")
    
    if client_sex == 'male':
        # Remove Female Hormone Health section
        female_section = 'Female Hormone Health'
        if female_section in sections:
            del sections[female_section]
            if female_section in section_names:
                section_names.remove(female_section)
                print(f"DEBUG: Removed female section for male client")
    elif client_sex == 'female':
        # Remove Male Hormone Health History section
        male_section = 'Male Hormone Health History'
        if male_section in sections:
            del sections[male_section]
            if male_section in section_names:
                section_names.remove(male_section)
                print(f"DEBUG: Removed male section for female client")
    else:
        print(f"DEBUG: Unknown client sex: {client_sex}, not filtering sections")
    
    print(f"DEBUG: Available sections after filtering: {section_names}")
    
    # Sort sections by the order they appear and questions within sections
    for section_name in sections:
        sections[section_name].sort(key=lambda q: int(q.get('question_order', 0)))
    
    # Determine current step/section from request
    current_step = int(request.form.get('step', request.args.get('step', 0)))
    if current_step < 0:
        current_step = 0
    elif current_step >= len(section_names):
        current_step = len(section_names) - 1
    
    current_section_name = section_names[current_step]
    current_section_questions = sections[current_section_name]
    # Get the field names that correspond to this section's questions - convert to form field names
    current_section_fields = [q['variable_name'].replace('-', '_') for q in current_section_questions]
    
    # Get section title - use the section name directly or fall back to generic title
    current_section_title = current_section_name if current_section_name != 'Unknown' else f"Section {current_step + 1}"
    
    # Get attempt_id from request
    attempt_id = request.args.get('attempt_id') or request.form.get('attempt_id')
    if not attempt_id:
        flash('Invalid HHQ link: missing attempt ID.', 'error')
        return redirect(url_for('main.index'))

    # Always prefill from saved responses for this attempt
    saved_answers = fetch_hhq_responses_dict_for_attempt(client_id, attempt_id)
    print(f"DEBUG: fetched saved_answers for attempt: {saved_answers}")
    
    def apply_prefill():
        """Apply prefill data to form fields"""
        if saved_answers:
            # Canonicalize saved_answers keys
            canonical_saved = {canonicalize_key(k): v for k, v in saved_answers.items()}
            prefilled_count = 0
            for form_field in form._fields:
                if form_field in canonical_saved and form_field not in ['next_step', 'prev_step', 'save_exit', 'submit_form', 'csrf_token']:
                    print(f"DEBUG: Setting {form_field} to {canonical_saved[form_field]}")
                    form._fields[form_field].data = bool(canonical_saved[form_field])
                    prefilled_count += 1
            print(f"DEBUG: Prefilled {prefilled_count} fields")
    
    # Apply prefill initially
    apply_prefill()

    if request.method == 'POST':
        print(f"DEBUG: raw POST data: {request.form}")
        # Let's debug some specific fields to see their values
        sample_fields = ['hh_heart_attack', 'hh_prevention_client', 'hh_family_dementia']
        for field_name in sample_fields:
            if hasattr(form, field_name):
                raw_post_value = request.form.get(field_name)
                form_field_value = getattr(form, field_name).data
                checkbox_in_post = field_name in request.form
                print(f"DEBUG FIELD {field_name}: POST={raw_post_value}, InPOST={checkbox_in_post}, Form={form_field_value}, Bool={bool(form_field_value)}")
        
        # Debug a few more fields that were mentioned as problematic
        problem_fields = ['hh_atherosclerosis', 'hh_taking_statin', 'hh_cardiac_bypass']
        for field_name in problem_fields:
            if hasattr(form, field_name):
                raw_post_value = request.form.get(field_name)
                form_field_value = getattr(form, field_name).data
                checkbox_in_post = field_name in request.form
                print(f"DEBUG PROBLEM {field_name}: POST={raw_post_value}, InPOST={checkbox_in_post}, Form={form_field_value}, Bool={bool(form_field_value)}")
        
        # Check if this is an auto-save request
        is_auto_save = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # Don't reapply prefill during navigation - it overrides user selections
        # if not is_auto_save:
        #     apply_prefill()
        
        # Save current answers before any navigation
        answers = {}
        
        # Only save current section fields during navigation to avoid overwriting other sections
        if not is_auto_save:
            # For navigation, only save current section fields that are TRUE
            # Don't save FALSE values during navigation to avoid overwriting previous TRUE values
            for question in current_section_questions:
                db_field_name = question['variable_name']
                form_field_name = form.get_form_field_name(db_field_name)
                if hasattr(form, form_field_name):
                    value = getattr(form, form_field_name).data
                    # Only save TRUE values during navigation
                    if value:
                        answers[db_field_name] = True
        else:
            # For auto-save, also only save TRUE values from current section to avoid overwrites
            for question in current_section_questions:
                db_field_name = question['variable_name']
                form_field_name = form.get_form_field_name(db_field_name)
                if hasattr(form, form_field_name):
                    value = getattr(form, form_field_name).data
                    # Only save TRUE values during auto-save too
                    if value:
                        answers[db_field_name] = True
        
        # Save answers to database only if we have answers to save
        if answers:
            print(f"DEBUG: answers to upsert: {answers}")
            try:
                # Use a new function that only updates True values without overwriting False ones
                upsert_hhq_answers_partial(client_id, answers, attempt_id)
                
                if is_auto_save:
                    return jsonify({'success': True})
                    
            except Exception as e:
                error_msg = f"Error saving HHQ responses: {str(e)}"
                print(error_msg)
                if is_auto_save:
                    return jsonify({'success': False, 'error': error_msg})
                flash('There was an error saving your responses. Please try again.', 'error')
                return redirect(url_for('hhq.hhq_form', client_id=client_id, attempt_id=attempt_id, step=current_step))

        # Handle navigation for non-auto-save requests
        if not is_auto_save:
            if form.next_step.data and current_step < len(section_names) - 1:
                return redirect(url_for('hhq.hhq_form', client_id=client_id, attempt_id=attempt_id, step=current_step + 1))
            elif form.prev_step.data and current_step > 0:
                return redirect(url_for('hhq.hhq_form', client_id=client_id, attempt_id=attempt_id, step=current_step - 1))
            elif form.save_exit.data:
                flash('Your progress has been saved!', 'success')
                return redirect(url_for('hhq.save_exit', client_id=client_id, attempt_id=attempt_id))
            else:
                # Submit form or continue
                if current_step < len(section_names) - 1:
                    return redirect(url_for('hhq.hhq_form', client_id=client_id, attempt_id=attempt_id, step=current_step + 1))
                else:
                    # Form completed - save complete record with all answers
                    print("DEBUG: Final submission - saving complete record")
                    complete_answers = {}
                    debug_true_count = 0
                    debug_false_count = 0
                    
                    # Only process questions from sections that were shown to the client
                    filtered_questions = []
                    for section_name in section_names:  # section_names is already filtered by gender
                        filtered_questions.extend(sections[section_name])
                    
                    for question in filtered_questions:  # Use filtered questions, not all questions
                        db_field_name = question['variable_name']
                        form_field_name = form.get_form_field_name(db_field_name)
                        if hasattr(form, form_field_name):
                            value = getattr(form, form_field_name).data
                            bool_value = bool(value)
                            complete_answers[db_field_name] = bool_value
                            if bool_value:
                                debug_true_count += 1
                            else:
                                debug_false_count += 1
                    
                    print(f"DEBUG FINAL: Saving {debug_true_count} True answers and {debug_false_count} False answers")
                    print(f"DEBUG FINAL: First few True answers: {[k for k, v in list(complete_answers.items())[:10] if v]}")
                    print(f"DEBUG FINAL: First few False answers: {[k for k, v in list(complete_answers.items())[:10] if not v]}")
                    
                    try:
                        # Use the original function for complete save
                        upsert_individual_hhq_answers(client_id, complete_answers, attempt_id)
                        flash('Health History Questionnaire completed successfully!', 'success')
                        return redirect(url_for('hhq.complete', client_id=client_id))
                    except Exception as e:
                        error_msg = f"Error saving final HHQ responses: {str(e)}"
                        print(error_msg)
                        flash('There was an error saving your final responses. Please try again.', 'error')
                        return redirect(url_for('hhq.hhq_form', client_id=client_id, attempt_id=attempt_id, step=current_step))

    return render_template('hhq/form.html', 
                         form=form,
                         current_step=current_step,
                         total_sections=len(section_names),
                         current_section=current_section_title,
                         current_section_fields=current_section_fields,
                         attempt_id=attempt_id)

@bp.route('/<client_id>/complete')
def complete(client_id):
    # Get client info for display
    client = fetch_client_by_id(client_id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('hhq/complete.html', client=client, client_id=client_id)

@bp.route('/client/<client_id>/complete')
def client_complete(client_id):
    # Get client info for display
    client = fetch_client_by_id(client_id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('hhq/client_complete.html', client=client, client_id=client_id)

@bp.route('/<token>/download')
def download_hhq(token):
    print(f"Download route hit with token: {token}")
    hhq_response = fetch_hhq_by_token(token)
    if not hhq_response or not hhq_response.get('completed_at'):
        flash('This HHQ must be completed before downloading.', 'error')
        return redirect(url_for('hhq.hhq_form', token=token))

    # Ensure client info is present
    if 'client' not in hhq_response or not hhq_response['client']:
        client_id = hhq_response.get('client_id')
        if client_id:
            client = fetch_client_by_id(client_id)
            hhq_response['client'] = client or {}
        else:
            hhq_response['client'] = {}

    # Generate PDF
    from app.utils.pdf_generator import generate_hhq_pdf
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        pdf_path = generate_hhq_pdf(hhq_response, tmp.name)

    try:
        client_last_name = hhq_response.get('client', {}).get('last_name', 'client')
        filename = f"HHQ_{client_last_name}_{token}.pdf"
        return send_file(pdf_path, as_attachment=True, download_name=filename)
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

@bp.route('/<client_id>/save_exit')
def save_exit(client_id):
    # Get client info
    client = fetch_client_by_id(client_id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('main.index'))
    
    # Get the attempt_id from the request args (should be passed from the form)
    attempt_id = request.args.get('attempt_id')
    if not attempt_id:
        flash('Invalid session. Please start over.', 'error')
        return redirect(url_for('main.index'))
    
    # Generate the link to continue
    continue_link = url_for('hhq.client_hhq_form', 
                           client_id=client_id, 
                           attempt_id=attempt_id, 
                           _external=True)
    
    return render_template('hhq/progress_saved.html', 
                         client=client,
                         continue_link=continue_link,
                         attempt_id=attempt_id)

@bp.route('/results/<token>')
@login_required
def view_results(token):
    # Fetch the HHQ response from Supabase using the unique_token (which is a string/UUID)
    hhq_response = fetch_hhq_by_token(token)
    if not hhq_response:
        flash('HHQ response not found.', 'error')
        return redirect(url_for('main.index'))

    # Check if the HHQ is completed
    if not hhq_response.get('completed_at'):
        flash('This HHQ has not been completed yet.', 'error')
        return redirect(url_for('clients.view', id=hhq_response.get('client_id')))

    # Convert completed_at to datetime if it's a string
    if isinstance(hhq_response.get('completed_at'), str):
        try:
            hhq_response['completed_at'] = datetime.fromisoformat(hhq_response['completed_at'].replace('Z', '+00:00'))
        except Exception:
            pass

    form = HHQForm()
    # Get section fields from validation function (reuse your get_section_fields logic)
    section_fields = {}
    for section_name in SECTION_TITLES:
        section_fields[section_name] = get_section_fields(section_name)

    # Organize form fields by section
    form_fields = []
    for section_name in SECTION_TITLES:
        section_field_names = section_fields.get(section_name, [])
        section_form_fields = []
        for field_name, field in form._fields.items():
            if field_name in section_field_names:
                field_info = {
                    'name': field_name,
                    'label': field.label,
                    'section': section_name
                }
                section_form_fields.append(field_info)
        form_fields.extend(section_form_fields)

    # Fetch client info if needed (if not included in hhq_response)
    client = None
    if 'client' in hhq_response:
        client = hhq_response['client']
    else:
        # Optionally fetch client from Supabase if needed
        pass

    return render_template('hhq/results.html', 
                         hhq_response=hhq_response,
                         client=client,
                         SECTION_TITLES=SECTION_TITLES,
                         form_fields=form_fields)

@bp.route('/admin/normalize-responses')
@login_required
def normalize_responses():
    """Normalize all HHQ responses to use consistent boolean values."""
    if not current_user.is_admin:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('main.index'))
    
    try:
        normalized_count = 0
        for response in HHQResponse.query.all():
            if response.responses:
                normalized = {}
                changes_made = False
                
                # First, copy non-HHQ fields as is
                for key, value in response.responses.items():
                    if not key.startswith('hh_'):
                        normalized[key] = value
                
                # Then normalize HHQ fields
                for key, value in response.responses.items():
                    if key.startswith('hh_'):
                        if value is True or value == 'on' or value == 'True' or value is True:
                            normalized[key] = True
                            if value != True:  # If the value was changed
                                changes_made = True
                        elif value is False or value == 'off' or value == 'False' or value is False:
                            # Don't include false values in normalized responses
                            if key in response.responses:  # If it was previously included
                                changes_made = True
                
                if changes_made:
                    print(f"Normalizing response {response.id}")
                    print(f"Before: {response.responses}")
                    print(f"After: {normalized}")
                    response.responses = normalized
                    db.session.add(response)
                    normalized_count += 1
        
        db.session.commit()
        flash(f'Successfully normalized {normalized_count} responses.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error normalizing responses: {str(e)}', 'error')
    
    return redirect(url_for('main.index'))

@bp.route('/client/<client_id>/responses')
@login_required 
def view_client_responses(client_id):
    """View HHQ responses for a specific client."""
    # Get client info
    client = fetch_client_by_id(client_id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('clients.index'))
    
    # Get HHQ responses
    responses = fetch_hhq_responses_dict(client_id)
    if not responses:
        flash('No HHQ responses found for this client.', 'info')
        return redirect(url_for('clients.view', id=client_id))
    
    # Get questions for context
    questions = fetch_health_history_questions()
    questions_dict = {q['variable_name']: q for q in questions}
    
    # Group responses by section
    sections = {}
    for variable_name, value in responses.items():
        if variable_name in questions_dict:
            question = questions_dict[variable_name]
            section = question.get('section', 'Unknown')
            if section not in sections:
                sections[section] = []
            sections[section].append({
                'variable_name': variable_name,
                'question_text': question['question_text'],
                'response': value,
                'order': int(question.get('question_order', 0))  # Convert to int
            })
    
    # Sort sections and questions within sections
    sorted_sections = {}
    for section_name in sorted(sections.keys()):
        sorted_sections[section_name] = sorted(sections[section_name], key=lambda x: x['order'])
    
    return render_template('hhq/client_responses.html', 
                         client=client,
                         sections=sorted_sections,
                         section_titles=SECTION_TITLES,
                         response_count=len(responses))

@bp.route('/client/<client_id>/form')
def view_client_form(client_id):
    """View the HHQ form for a client (for direct access)."""
    return redirect(url_for('hhq.hhq_form', client_id=client_id))

@bp.route('/clients/<client_id>/generate_hhq', methods=['POST', 'GET'])
@login_required
def generate_hhq(client_id):
    client = fetch_client_by_id(client_id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('clients.index'))
    form = GenerateHHQForm()
    if request.method == 'POST':
        attempt_id, prefill_answers = create_hhq_attempt(client_id)
        hhq_link = url_for('hhq.client_hhq_form', client_id=client_id, attempt_id=attempt_id, _external=True)
        return render_template('hhq/generate_link_result.html', client=client, hhq_link=hhq_link, attempt_id=attempt_id)
    return render_template('hhq/generate_link_confirm.html', client=client, form=form)

def db_to_form_field(db_key):
    return db_key.replace("-", "_")

def canonicalize_key(key):
    return key.replace('-', '_')

@bp.route('/client/<client_id>/hhq', methods=['GET', 'POST'])
def client_hhq_form(client_id):
    # Get client info first for gender filtering
    client = fetch_client_by_id(client_id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('main.index'))
    
    form = HHQForm()
    print(f"DEBUG: form data after instantiation: {[ (f, getattr(form, f).data) for f in form._fields ]}")
    
    # Get all questions and organize by section
    questions = fetch_health_history_questions()
    if not questions:
        flash('Unable to load questionnaire questions. Please try again later.', 'error')
        return redirect(url_for('main.index'))

    # Group questions by section - keep section as text, map to numeric index
    sections = {}
    section_names = []
    for question in questions:
        section_name = question.get('section', 'Unknown')
        if section_name not in sections:
            sections[section_name] = []
            section_names.append(section_name)
        sections[section_name].append(question)
    
    # Filter out gender-specific sections based on client's sex
    client_sex = client.get('sex', '').lower()
    print(f"DEBUG: Client sex: {client_sex}")
    print(f"DEBUG: Available sections before filtering: {section_names}")
    
    if client_sex == 'male':
        # Remove Female Hormone Health section
        female_section = 'Female Hormone Health'
        if female_section in sections:
            del sections[female_section]
            if female_section in section_names:
                section_names.remove(female_section)
                print(f"DEBUG: Removed female section for male client")
    elif client_sex == 'female':
        # Remove Male Hormone Health History section
        male_section = 'Male Hormone Health History'
        if male_section in sections:
            del sections[male_section]
            if male_section in section_names:
                section_names.remove(male_section)
                print(f"DEBUG: Removed male section for female client")
    else:
        print(f"DEBUG: Unknown client sex: {client_sex}, not filtering sections")
    
    print(f"DEBUG: Available sections after filtering: {section_names}")
    
    # Sort sections by the order they appear and questions within sections
    for section_name in sections:
        sections[section_name].sort(key=lambda q: int(q.get('question_order', 0)))
    
    # Determine current step/section from request
    current_step = int(request.form.get('step', request.args.get('step', 0)))
    if current_step < 0:
        current_step = 0
    elif current_step >= len(section_names):
        current_step = len(section_names) - 1
    
    current_section_name = section_names[current_step]
    current_section_questions = sections[current_section_name]
    # Get the field names that correspond to this section's questions - convert to form field names
    current_section_fields = [q['variable_name'].replace('-', '_') for q in current_section_questions]
    
    # Get section title - use the section name directly or fall back to generic title
    current_section_title = current_section_name if current_section_name != 'Unknown' else f"Section {current_step + 1}"
    
    # Get attempt_id from request
    attempt_id = request.args.get('attempt_id') or request.form.get('attempt_id')
    if not attempt_id:
        flash('Invalid HHQ link: missing attempt ID.', 'error')
        return redirect(url_for('main.index'))

    # Always prefill from saved responses for this attempt
    saved_answers = fetch_hhq_responses_dict_for_attempt(client_id, attempt_id)
    print(f"DEBUG: fetched saved_answers for attempt: {saved_answers}")
    
    def apply_prefill():
        """Apply prefill data to form fields"""
        if saved_answers:
            # Canonicalize saved_answers keys
            canonical_saved = {canonicalize_key(k): v for k, v in saved_answers.items()}
            prefilled_count = 0
            for form_field in form._fields:
                if form_field in canonical_saved and form_field not in ['next_step', 'prev_step', 'save_exit', 'submit_form', 'csrf_token']:
                    print(f"DEBUG: Setting {form_field} to {canonical_saved[form_field]}")
                    form._fields[form_field].data = bool(canonical_saved[form_field])
                    prefilled_count += 1
            print(f"DEBUG: Prefilled {prefilled_count} fields")
    
    # Apply prefill initially
    apply_prefill()

    if request.method == 'POST':
        print(f"DEBUG: raw POST data: {request.form}")
        # Let's debug some specific fields to see their values
        sample_fields = ['hh_heart_attack', 'hh_prevention_client', 'hh_family_dementia']
        for field_name in sample_fields:
            if hasattr(form, field_name):
                raw_post_value = request.form.get(field_name)
                form_field_value = getattr(form, field_name).data
                checkbox_in_post = field_name in request.form
                print(f"DEBUG FIELD {field_name}: POST={raw_post_value}, InPOST={checkbox_in_post}, Form={form_field_value}, Bool={bool(form_field_value)}")
        
        # Debug a few more fields that were mentioned as problematic
        problem_fields = ['hh_atherosclerosis', 'hh_taking_statin', 'hh_cardiac_bypass']
        for field_name in problem_fields:
            if hasattr(form, field_name):
                raw_post_value = request.form.get(field_name)
                form_field_value = getattr(form, field_name).data
                checkbox_in_post = field_name in request.form
                print(f"DEBUG PROBLEM {field_name}: POST={raw_post_value}, InPOST={checkbox_in_post}, Form={form_field_value}, Bool={bool(form_field_value)}")
        
        # Check if this is an auto-save request
        is_auto_save = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # Don't reapply prefill during navigation - it overrides user selections
        # if not is_auto_save:
        #     apply_prefill()
        
        # Save current answers before any navigation
        answers = {}
        
        # Only save current section fields during navigation to avoid overwriting other sections
        if not is_auto_save:
            # For navigation, only save current section fields that are TRUE
            # Don't save FALSE values during navigation to avoid overwriting previous TRUE values
            for question in current_section_questions:
                db_field_name = question['variable_name']
                form_field_name = form.get_form_field_name(db_field_name)
                if hasattr(form, form_field_name):
                    value = getattr(form, form_field_name).data
                    # Only save TRUE values during navigation
                    if value:
                        answers[db_field_name] = True
        else:
            # For auto-save, also only save TRUE values from current section to avoid overwrites
            for question in current_section_questions:
                db_field_name = question['variable_name']
                form_field_name = form.get_form_field_name(db_field_name)
                if hasattr(form, form_field_name):
                    value = getattr(form, form_field_name).data
                    # Only save TRUE values during auto-save too
                    if value:
                        answers[db_field_name] = True
        
        # Save answers to database only if we have answers to save
        if answers:
            print(f"DEBUG: answers to upsert: {answers}")
            try:
                # Use a new function that only updates True values without overwriting False ones
                upsert_hhq_answers_partial(client_id, answers, attempt_id)
                
                if is_auto_save:
                    return jsonify({'success': True})
                    
            except Exception as e:
                error_msg = f"Error saving HHQ responses: {str(e)}"
                print(error_msg)
                if is_auto_save:
                    return jsonify({'success': False, 'error': error_msg})
                flash('There was an error saving your responses. Please try again.', 'error')
                return redirect(url_for('hhq.client_hhq_form', client_id=client_id, attempt_id=attempt_id, step=current_step))

        # Handle navigation for non-auto-save requests
        if not is_auto_save:
            if form.next_step.data and current_step < len(section_names) - 1:
                return redirect(url_for('hhq.client_hhq_form', client_id=client_id, attempt_id=attempt_id, step=current_step + 1))
            elif form.prev_step.data and current_step > 0:
                return redirect(url_for('hhq.client_hhq_form', client_id=client_id, attempt_id=attempt_id, step=current_step - 1))
            elif form.save_exit.data:
                flash('Your progress has been saved!', 'success')
                return redirect(url_for('hhq.save_exit', client_id=client_id, attempt_id=attempt_id))
            else:
                # Submit form or continue
                if current_step < len(section_names) - 1:
                    return redirect(url_for('hhq.client_hhq_form', client_id=client_id, attempt_id=attempt_id, step=current_step + 1))
                else:
                    # Form completed - save complete record with all answers
                    print("DEBUG: Final submission - saving complete record")
                    complete_answers = {}
                    debug_true_count = 0
                    debug_false_count = 0
                    
                    # Only process questions from sections that were shown to the client
                    filtered_questions = []
                    for section_name in section_names:  # section_names is already filtered by gender
                        filtered_questions.extend(sections[section_name])
                    
                    for question in filtered_questions:  # Use filtered questions, not all questions
                        db_field_name = question['variable_name']
                        form_field_name = form.get_form_field_name(db_field_name)
                        if hasattr(form, form_field_name):
                            value = getattr(form, form_field_name).data
                            bool_value = bool(value)
                            complete_answers[db_field_name] = bool_value
                            if bool_value:
                                debug_true_count += 1
                            else:
                                debug_false_count += 1
                    
                    print(f"DEBUG FINAL: Saving {debug_true_count} True answers and {debug_false_count} False answers")
                    print(f"DEBUG FINAL: First few True answers: {[k for k, v in list(complete_answers.items())[:10] if v]}")
                    print(f"DEBUG FINAL: First few False answers: {[k for k, v in list(complete_answers.items())[:10] if not v]}")
                    
                    try:
                        # Use the original function for complete save
                        upsert_individual_hhq_answers(client_id, complete_answers, attempt_id)
                        flash('Health History Questionnaire completed successfully!', 'success')
                        return redirect(url_for('hhq.client_complete', client_id=client_id))
                    except Exception as e:
                        error_msg = f"Error saving final HHQ responses: {str(e)}"
                        print(error_msg)
                        flash('There was an error saving your final responses. Please try again.', 'error')
                        return redirect(url_for('hhq.client_hhq_form', client_id=client_id, attempt_id=attempt_id, step=current_step))

    return render_template('hhq/client_form.html', 
                         form=form,
                         current_step=current_step,
                         total_sections=len(section_names),
                         current_section=current_section_title,
                         current_section_fields=current_section_fields,
                         attempt_id=attempt_id)