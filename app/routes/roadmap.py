from flask import Blueprint, flash, redirect, url_for
from flask_login import login_required

bp = Blueprint('roadmap', __name__, url_prefix='/roadmap')

@bp.route('/generate/<client_id>')
@login_required
def generate(client_id):
    flash('Roadmap generation functionality coming soon.', 'info')
    return redirect(url_for('clients.view', id=client_id)) 