from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Client, Report

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # If user is authenticated, show dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    # Otherwise redirect to login
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    total_clients = Client.query.count()
    total_labs = Report.query.count()
    total_hhq = 0  # We'll add HHQ functionality later
    recent_clients = Client.query.order_by(Client.created_at.desc()).limit(5).all()
    
    return render_template('main/index.html',
                         total_clients=total_clients,
                         total_labs=total_labs,
                         total_hhq=total_hhq,
                         recent_clients=recent_clients) 