from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from ..utils.supabase_client import fetch_clients, create_client, update_client, delete_client, fetch_hhq_responses_for_client, fetch_client_by_id, fetch_health_history_questions, save_lab_results, fetch_lab_results_for_client
from ..utils.lab_extractor import process_pdf
import json
import pytz
import os
from werkzeug.utils import secure_filename

bp = Blueprint('clients', __name__, url_prefix='/clients')

def format_mt(dt_str):
    # Format UTC ISO string to 'May 21, 2025 7:03pm MT'
    dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    mt = pytz.timezone('US/Mountain')
    dt_mt = dt.astimezone(mt)
    return dt_mt.strftime('%b %d, %Y %-I:%M%p MT')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    search_query = request.form.get('search', '') if request.method == 'POST' else request.args.get('search', '')
    all_clients = fetch_clients()
    
    if search_query:
        clients = [c for c in all_clients if search_query.lower() in (
            f"{c['first_name']} {c['last_name']} {c['email']}".lower())]
    else:
        clients = all_clients
        
    return render_template('clients/index.html', clients=clients, search_query=search_query)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        try:
            client_data = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'date_of_birth': request.form.get('date_of_birth'),
                'sex': request.form['sex'],
                'phone': request.form.get('phone'),
                'email': request.form.get('email'),
                'created_at': datetime.utcnow().isoformat()
            }
            
            client = create_client(client_data)
            if client:
                flash('Client added successfully!', 'success')
                return redirect(url_for('clients.view', id=client['id']))
            else:
                flash('Error adding client', 'danger')
        except Exception as e:
            flash(f'Error adding client: {str(e)}', 'danger')
    return render_template('clients/new.html')

@bp.route('/<id>')
@login_required
def view(id):
    clients = fetch_clients()
    client = next((c for c in clients if str(c['id']) == str(id)), None)
    if not client:
        flash('Client not found', 'danger')
        return redirect(url_for('clients.index'))
    # Fetch HHQ responses for this client from Supabase
    client['hhq_responses'] = fetch_hhq_responses_for_client(client['id'])
    # Fetch lab results for this client from Supabase
    client['lab_results'] = fetch_lab_results_for_client(client['id'])
    # Add empty reports list for template compatibility
    client['reports'] = []
    return render_template('clients/view.html', client=client)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    clients = fetch_clients()
    client = next((c for c in clients if str(c['id']) == str(id)), None)
    if not client:
        flash('Client not found', 'danger')
        return redirect(url_for('clients.index'))
        
    if request.method == 'POST':
        try:
            client_data = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'sex': request.form['sex'],
                'date_of_birth': request.form.get('date_of_birth'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email')
            }
            
            updated_client = update_client(id, client_data)
            if updated_client:
                flash('Client updated successfully!', 'success')
                return redirect(url_for('clients.view', id=id))
            else:
                flash('Error updating client', 'danger')
        except Exception as e:
            flash(f'Error updating client: {str(e)}', 'danger')
    return render_template('clients/edit.html', client=client)

@bp.route('/<id>/delete', methods=['POST'])
@login_required
def delete(id):
    try:
        if delete_client(id):
            flash('Client deleted successfully!', 'success')
        else:
            flash('Error deleting client', 'danger')
    except Exception as e:
        flash(f'Error deleting client: {str(e)}', 'danger')
    return redirect(url_for('clients.index'))

@bp.route('/clients/<client_id>/hhq_history')
def hhq_history(client_id):
    client = fetch_client_by_id(client_id)
    all_responses = fetch_hhq_responses_for_client(client_id)
    # Group by attempt_id
    attempts = {}
    for row in all_responses:
        attempt_id = row['attempt_id']
        if attempt_id not in attempts:
            attempts[attempt_id] = {
                'taken_at': row['taken_at'],
                'responses': row['responses'],
            }
    # Sort by taken_at descending
    sorted_attempts = sorted(attempts.items(), key=lambda x: x[1]['taken_at'], reverse=True)
    return render_template('clients/hhq_history.html', client=client, attempts=sorted_attempts, format_mt=format_mt)

@bp.route('/clients/<client_id>/hhq_history/<attempt_id>')
def hhq_attempt_detail(client_id, attempt_id):
    client = fetch_client_by_id(client_id)
    all_responses = fetch_hhq_responses_for_client(client_id)
    attempt_row = next((r for r in all_responses if r['attempt_id'] == attempt_id), None)
    answers = {}
    if attempt_row and attempt_row['responses']:
        answers = json.loads(attempt_row['responses'])
    # Map variable_name to display_text
    questions = fetch_health_history_questions()
    question_map = {q['variable_name']: q.get('display_text') or q.get('label') or q['variable_name'] for q in questions}
    # Build display answers
    display_answers = [(question_map.get(q, q), answers[q]) for q in answers]
    taken_at = attempt_row['taken_at'] if attempt_row else None
    return render_template('clients/hhq_attempt_detail.html', client=client, taken_at=taken_at, display_answers=display_answers, format_mt=format_mt)

@bp.route('/<client_id>/upload_lab', methods=['POST'])
@login_required
def upload_lab(client_id):
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('clients.view', id=client_id))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('clients.view', id=client_id))

    if not file.filename.lower().endswith('.pdf'):
        flash('Please upload a PDF file', 'error')
        return redirect(url_for('clients.view', id=client_id))

    try:
        # Create uploads directory if it doesn't exist
        upload_dir = 'uploads'
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file with secure filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(upload_dir, safe_filename)
        file.save(file_path)
        
        # Process the PDF and extract lab results
        print(f"Processing PDF file: {file_path}")
        extracted_results = process_pdf(file_path)
        
        if not extracted_results:
            flash('No lab results could be extracted from this PDF. Please verify it\'s a LabCorp report.', 'warning')
            return redirect(url_for('clients.view', id=client_id))
        
        # Save results to Supabase
        save_lab_results(client_id, extracted_results)
        
        # Clean up the uploaded file
        os.remove(file_path)
        
        flash(f'Lab results uploaded successfully! Extracted {len(extracted_results)} test results.', 'success')
        return redirect(url_for('clients.view', id=client_id))
        
    except Exception as e:
        print(f"Error uploading lab results: {str(e)}")
        # Clean up file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        flash(f'Error processing lab results: {str(e)}', 'error')
        return redirect(url_for('clients.view', id=client_id))

@bp.route('/<id>/lab-results')
@login_required
def view_all_lab_results(id):
    """View all lab results for a client in detail."""
    clients = fetch_clients()
    client = next((c for c in clients if str(c['id']) == str(id)), None)
    if not client:
        flash('Client not found', 'danger')
        return redirect(url_for('clients.index'))
    
    # Fetch all lab results for this client
    lab_results = fetch_lab_results_for_client(client['id'])
    
    # Group lab results by upload date/batch if needed
    # For now, we'll show them all in chronological order
    
    return render_template('clients/lab_results.html', client=client, lab_results=lab_results) 