"""
Client Images Routes
Handles image uploads for roadmap visual content
"""

import os
import uuid
from datetime import datetime
from flask import Blueprint, request, flash, redirect, url_for, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import mimetypes

from ..utils.supabase_client import get_supabase_client

client_images_bp = Blueprint('client_images', __name__)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(filename):
    """Generate unique filename while preserving extension"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    unique_name = str(uuid.uuid4())
    return f"{unique_name}.{ext}" if ext else unique_name

def resize_image_if_needed(filepath, max_width=1200, max_height=800, quality=85):
    """Resize image if it's too large, maintaining aspect ratio"""
    try:
        with Image.open(filepath) as img:
            # Convert RGBA to RGB if needed (for JPEG compatibility)
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img, mask=img.split()[-1])
                img = background
            
            # Check if resize is needed
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                img.save(filepath, optimize=True, quality=quality)
                
    except Exception as e:
        current_app.logger.error(f"Error resizing image {filepath}: {str(e)}")

@client_images_bp.route('/clients/<client_id>/images/upload', methods=['POST'])
def upload_client_image(client_id):
    """Upload an image for a specific client"""
    try:
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('clients.view_client', client_id=client_id))
        
        file = request.files['file']
        image_type = request.form.get('image_type', 'other')
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('clients.view_client', client_id=client_id))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload an image file (PNG, JPG, JPEG, GIF, BMP, WEBP, TIFF)', 'error')
            return redirect(url_for('clients.view_client', client_id=client_id))
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            flash('File too large. Maximum size is 10MB', 'error')
            return redirect(url_for('clients.view_client', client_id=client_id))
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        filename = get_unique_filename(original_filename)
        
        # Create directory structure
        upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'client_images', image_type)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        
        # Resize if needed
        resize_image_if_needed(file_path)
        
        # Get actual file size after processing
        actual_file_size = os.path.getsize(file_path)
        
        # Get MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # Store in database
        supabase = get_supabase_client()
        relative_path = f"uploads/client_images/{image_type}/{filename}"
        
        image_data = {
            'client_id': client_id,
            'image_type': image_type,
            'filename': filename,
            'original_filename': original_filename,
            'file_path': relative_path,
            'file_size': actual_file_size,
            'mime_type': mime_type,
            'title': title or original_filename,
            'description': description,
            'uploaded_by': 'admin',  # TODO: Replace with actual user when auth is implemented
            'created_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('client_images').insert(image_data).execute()
        
        if result.data:
            flash(f'Image "{original_filename}" uploaded successfully', 'success')
        else:
            flash('Error saving image information to database', 'error')
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
        
        return redirect(url_for('clients.view_client', client_id=client_id))
        
    except Exception as e:
        current_app.logger.error(f"Error uploading image for client {client_id}: {str(e)}")
        flash('Error uploading image', 'error')
        return redirect(url_for('clients.view_client', client_id=client_id))

@client_images_bp.route('/clients/<client_id>/images')
def get_client_images(client_id):
    """Get all images for a specific client"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('client_images').select('*').eq('client_id', client_id).eq('is_active', True).order('display_order', desc=False).execute()
        
        return jsonify({
            'success': True,
            'images': result.data or []
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting images for client {client_id}: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@client_images_bp.route('/clients/<client_id>/images/<int:image_id>/delete', methods=['POST'])
def delete_client_image(client_id, image_id):
    """Delete a client image"""
    try:
        supabase = get_supabase_client()
        
        # Get image info first
        result = supabase.table('client_images').select('*').eq('id', image_id).eq('client_id', client_id).execute()
        
        if not result.data:
            flash('Image not found', 'error')
            return redirect(url_for('clients.view_client', client_id=client_id))
        
        image_info = result.data[0]
        
        # Delete from database
        supabase.table('client_images').update({'is_active': False}).eq('id', image_id).execute()
        
        # Optionally delete physical file
        file_path = os.path.join(current_app.root_path, '..', image_info['file_path'])
        if os.path.exists(file_path):
            os.remove(file_path)
        
        flash('Image deleted successfully', 'success')
        return redirect(url_for('clients.view_client', client_id=client_id))
        
    except Exception as e:
        current_app.logger.error(f"Error deleting image {image_id} for client {client_id}: {str(e)}")
        flash('Error deleting image', 'error')
        return redirect(url_for('clients.view_client', client_id=client_id))

@client_images_bp.route('/uploads/client_images/<path:filename>')
def serve_client_image(filename):
    """Serve uploaded client images"""
    try:
        # Reconstruct the full path
        upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'client_images')
        return send_from_directory(upload_dir, filename)
    except Exception as e:
        current_app.logger.error(f"Error serving image {filename}: {str(e)}")
        return "Image not found", 404 