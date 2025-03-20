import click
from flask.cli import with_appcontext
from .models import User, db

@click.command('create-admin')
@with_appcontext
def create_admin_command():
    """Create an admin user."""
    admin = User(
        username='admin',
        email='admin@mindstoke.ai',
        is_admin=True
    )
    admin.set_password('admin123')  # Change this password in production!
    
    if User.query.filter_by(username='admin').first():
        click.echo('Admin user already exists.')
        return
    
    db.session.add(admin)
    db.session.commit()
    click.echo('Admin user created successfully.') 