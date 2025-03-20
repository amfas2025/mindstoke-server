from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from ..models import Client
from ..extensions import db
from datetime import datetime

bp = Blueprint('clients', __name__, url_prefix='/clients')

@bp.route('/')
@login_required
def index():
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return render_template('clients/index.html', clients=clients)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        try:
            client = Client(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                date_of_birth=datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date() if request.form.get('date_of_birth') else None,
                phone=request.form.get('phone'),
                email=request.form.get('email')
            )
            db.session.add(client)
            db.session.commit()
            flash('Client added successfully!', 'success')
            return redirect(url_for('clients.view', id=client.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding client: {str(e)}', 'danger')
    return render_template('clients/new.html')

@bp.route('/<int:id>')
@login_required
def view(id):
    client = Client.query.get_or_404(id)
    return render_template('clients/view.html', client=client)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    client = Client.query.get_or_404(id)
    if request.method == 'POST':
        try:
            client.first_name = request.form['first_name']
            client.last_name = request.form['last_name']
            
            # Handle date of birth with better error handling
            dob = request.form.get('date_of_birth')
            if dob:
                try:
                    client.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
                except ValueError:
                    flash('Invalid date format. Please use YYYY-MM-DD format.', 'danger')
                    return render_template('clients/edit.html', client=client)
            else:
                client.date_of_birth = None
            
            client.phone = request.form.get('phone')
            client.email = request.form.get('email')
            
            db.session.commit()
            flash('Client updated successfully!', 'success')
            return redirect(url_for('clients.view', id=client.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating client: {str(e)}', 'danger')
    return render_template('clients/edit.html', client=client)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    client = Client.query.get_or_404(id)
    try:
        db.session.delete(client)
        db.session.commit()
        flash('Client deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting client: {str(e)}', 'danger')
    return redirect(url_for('clients.index')) 