import click
from flask.cli import with_appcontext
from .extensions import db
from .models import User
from werkzeug.security import generate_password_hash

@click.command('create-admin')
@with_appcontext
def create_admin_command():
    """Create an admin user."""
    admin = User(
        username='admin'
    )
    admin.set_password('admin123')  # Change this password in production!
    
    if User.query.filter_by(username='admin').first():
        click.echo('Admin user already exists.')
        return
    
    db.session.add(admin)
    db.session.commit()
    click.echo('Admin user created successfully!')

@click.command('recreate-db')
@with_appcontext
def recreate_db_command():
    """Recreate the database."""
    db.drop_all()
    db.create_all()
    click.echo('Database recreated successfully!') 