from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from ..utils.lab_extractor import process_pdf, save_results
from datetime import datetime

labs_bp = Blueprint('labs', __name__)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@labs_bp.route('/upload', methods=['POST'])
def upload_lab():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], f'temp_{timestamp}_{filename}')
        file.save(temp_filepath)
        
        try:
            # Process the PDF and extract lab results
            results = process_pdf(temp_filepath)
            
            if results:
                # Save results to CSV
                client_id = os.path.splitext(filename)[0]
                csv_path = save_results(client_id, results, current_app.config['RESULTS_FOLDER'])
                
                # Clean up the temporary PDF file
                os.remove(temp_filepath)
                
                return jsonify({
                    'message': 'Lab results extracted successfully',
                    'results': results,
                    'csv_path': os.path.basename(csv_path)
                })
            else:
                return jsonify({'error': 'No results could be extracted from the PDF'}), 400
                
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

@labs_bp.route('/results/<filename>')
def get_results(filename):
    try:
        filepath = os.path.join(current_app.config['RESULTS_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'Results file not found'}), 404
            
        # Here you could read and return the CSV contents if needed
        return jsonify({'message': 'Results file found', 'path': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 