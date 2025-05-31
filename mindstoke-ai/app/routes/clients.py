from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from datetime import datetime
from ..utils.supabase_client import fetch_clients, create_client, update_client, delete_client

bp = Blueprint('clients', __name__, url_prefix='/clients')

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
                'sex': request.form.get('sex'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email'),
                'created_at': datetime.utcnow().isoformat()
            }

            print("DEBUG: Client data to insert:", client_data)
            created = create_client(client_data)
            print("DEBUG: Insert result:", created)

            if created:
                flash('Client added successfully!', 'success')
                return redirect(url_for('clients.view', id=created['id']))
            else:
                flash('Error adding client', 'danger')

        except Exception as e:
            flash(f'Error adding client: {str(e)}', 'danger')

    return render_template('clients/new.html')

@bp.route('/<id>')
@login_required
def view(id):
    clients = fetch_clients()
    client = next((c for c in clients if str(c['id']) == id), None)
    if not client:
        flash('Client not found', 'danger')
        return redirect(url_for('clients.index'))
    return render_template('clients/view.html', client=client)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    clients = fetch_clients()
    client = next((c for c in clients if str(c['id']) == id), None)
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
