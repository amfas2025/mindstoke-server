from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..models import Client, db

bp = Blueprint('clients', __name__, url_prefix='/clients')

@bp.route('/')
@login_required
def index():
    clients = Client.query.all()
    return render_template('clients/index.html', clients=clients)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        client = Client(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            phone=request.form['phone']
        )
        db.session.add(client)
        db.session.commit()
        flash('Client created successfully.')
        return redirect(url_for('clients.index'))
    return render_template('clients/new.html') 