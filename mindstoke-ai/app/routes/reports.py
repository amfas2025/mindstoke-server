from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from ..models import Report, Client, db
from ..utils.lab_extractor import process_pdf, save_results
import os
import json
from werkzeug.utils import secure_filename

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.route('/')
@login_required
def index():
    reports = Report.query.all()
    return render_template('reports/index.html', reports=reports)

@bp.route('/new/<int:client_id>', methods=['GET', 'POST'])
@login_required
def new(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == 'POST':
        # Handle lab file upload
        lab_data = None
        if 'lab_file' in request.files:
            lab_file = request.files['lab_file']
            if lab_file and lab_file.filename.endswith('.pdf'):
                # Save the uploaded file
                filename = f"lab_{client_id}_{lab_file.filename}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                lab_file.save(filepath)
                
                # Extract labs from PDF
                lab_data = process_pdf(filepath)
                if lab_data:
                    # Save extracted data to JSON
                    save_results(filename, lab_data, current_app.config['RESULTS_FOLDER'])
                else:
                    flash('Error extracting lab data from PDF.')
                    return redirect(url_for('reports.new', client_id=client_id))
            else:
                flash('Invalid file format. Please upload a PDF file.')
                return redirect(url_for('reports.new', client_id=client_id))

        # Handle HHQ data
        hhq_data = None
        if request.form.get('hhq_data'):
            try:
                hhq_data = json.loads(request.form['hhq_data'])
            except json.JSONDecodeError:
                flash('Invalid HHQ data format.')
                return redirect(url_for('reports.new', client_id=client_id))

        # Create report
        report = Report(
            client_id=client_id,
            created_by=current_user.id,
            lab_data=lab_data,
            hhq_data=hhq_data,
            recommendations=request.form.get('recommendations')
        )
        db.session.add(report)
        db.session.commit()
        flash('Report created successfully.')
        return redirect(url_for('reports.index'))
    return render_template('reports/new.html', client=client)

@bp.route('/<int:report_id>')
@login_required
def view(report_id):
    report = Report.query.get_or_404(report_id)
    return render_template('reports/view.html', report=report)

@bp.route('/<int:report_id>/finalize', methods=['POST'])
@login_required
def finalize(report_id):
    report = Report.query.get_or_404(report_id)
    report.status = 'final'
    db.session.commit()
    flash('Report finalized successfully.')
    return redirect(url_for('reports.index'))

@bp.route('/upload', methods=['POST'])
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
                return jsonify({'message': 'File processed successfully', 'results': results})
            else:
                return jsonify({'error': 'No results could be extracted'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file'}), 400 