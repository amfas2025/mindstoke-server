from flask import Flask
from config import Config
from .extensions import db, login_manager
from flask_wtf.csrf import CSRFProtect
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'mindstoke.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    app.config['RESULTS_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'extracted_results')
    
    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    with app.app_context():
        # Import routes
        from .routes import main, auth, clients, reports
        
        # Register blueprints
        app.register_blueprint(main.main)
        app.register_blueprint(auth.bp)
        app.register_blueprint(clients.bp)
        app.register_blueprint(reports.bp)
        
        # Create database tables
        db.create_all()
        
        # Register CLI commands
        from .commands import create_admin_command, recreate_db_command
        app.cli.add_command(create_admin_command)
        app.cli.add_command(recreate_db_command)
        
        # Exempt auth routes from CSRF
        csrf.exempt(auth.bp)
    
    return app 