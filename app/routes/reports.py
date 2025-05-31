from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from ..models import Report, Client, LabResult, db
from ..utils.lab_extractor import process_pdf, save_results
from flask_wtf import FlaskForm
import os
import json
from werkzeug.utils import secure_filename

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.route('/')
@login_required
def index():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return render_template('reports/index.html', reports=reports)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    # Create a basic form for CSRF protection
    form = FlaskForm()
    
    # Get client_id from query parameters for direct uploads
    client_id = request.args.get('client_id')
    client = None
    # Only check for presence, do not fetch from DB
    if not client_id:
        flash('Client ID is required', 'error')
        return redirect(url_for('clients.index'))

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Form validation failed. Please try again.', 'error')
            return redirect(url_for('reports.new'))
            
        # Get client_id from form data if not already set
        client_id = client_id or request.form.get('client_id')
        lab_file = request.files.get('lab_file')
        
        if not client_id:
            flash('Client ID is required', 'error')
            return redirect(url_for('reports.new'))
        # Do not fetch client from DB, just use the ID
        # Create a new report (if you want to keep using SQLAlchemy for reports, you can leave this as is)
        report = Report(
            client_id=client_id,
            created_by=current_user.id,
            status='draft'
        )
        db.session.add(report)
        db.session.flush()  # Get the report ID before committing
        
        # Process lab file if provided
        if lab_file:
            filename = secure_filename(lab_file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            lab_file.save(filepath)
            
            try:
                # Extract data from PDF
                print(f"Processing PDF file: {filepath}")  # Debug print
                extracted_data = process_pdf(filepath)
                print(f"Extracted data: {json.dumps(extracted_data, indent=2)}")  # Debug print
                
                if not extracted_data:
                    print("No data was extracted from the PDF")
                    flash('No lab results could be extracted from the PDF', 'error')
                else:
                    # Create LabResult entries for each test
                    for test_name, data in extracted_data.items():
                        print(f"Creating LabResult for {test_name}: {data}")  # Debug print
                        lab_result = LabResult(
                            client_id=client_id,
                            report_id=report.id,
                            test_name=test_name,
                            value=data.get('value', ''),
                            unit=data.get('unit', ''),
                            reference_range=data.get('reference_range', '')
                        )
                        db.session.add(lab_result)
                        print(f"Added LabResult: {lab_result.test_name} = {lab_result.value} {lab_result.unit}")  # Debug print
                
                flash('Lab results extracted successfully', 'success')
            except Exception as e:
                print(f"Error processing lab file: {str(e)}")  # Debug print
                flash(f'Error processing lab file: {str(e)}', 'error')
            finally:
                # Clean up the file
                if os.path.exists(filepath):
                    os.remove(filepath)
        
        # Save everything to the database
        try:
            db.session.commit()
            print(f"Committed to database. Report ID: {report.id}")  # Debug print
            # Verify lab results were saved
            results = LabResult.query.filter_by(report_id=report.id).all()
            print(f"Number of lab results saved: {len(results)}")  # Debug print
            for result in results:
                print(f"Saved result: {result.test_name} = {result.value} {result.unit}")  # Debug print
            
            flash('Report created successfully', 'success')
            return redirect(url_for('clients.view', id=client_id))
        except Exception as e:
            print(f"Database error: {str(e)}")  # Debug print
            db.session.rollback()
            flash(f'Error saving report: {str(e)}', 'error')
            return redirect(url_for('reports.new'))
    
    # GET request - show form
    clients = Client.query.all()
    return render_template('reports/new.html', clients=clients, client=client, form=form)

@bp.route('/<int:report_id>')
@login_required
def view(report_id):
    report = Report.query.get_or_404(report_id)
    # Debug print to check lab results
    print(f"Viewing report {report_id}")
    print(f"Number of lab results: {len(report.lab_results)}")
    for result in report.lab_results:
        print(f"Lab result: {result.test_name} = {result.value} {result.unit}")
    return render_template('reports/view.html', report=report)

@bp.route('/<int:report_id>/finalize', methods=['POST'])
@login_required
def finalize(report_id):
    report = Report.query.get_or_404(report_id)
    if report.status == 'draft':
        report.status = 'final'
        db.session.commit()
        flash('Report finalized successfully.')
    return redirect(url_for('reports.view', report_id=report.id))

@bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            results = process_pdf(filepath)
            if results:
                save_results(filename, results, current_app.config['RESULTS_FOLDER'])
                return jsonify({
                    'message': 'File processed successfully',
                    'results': results
                })
            else:
                return jsonify({'error': 'No results could be extracted'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file'}), 400 