from flask import Flask, render_template
from config import Config
from .extensions import db, login_manager, mail, migrate
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import sys
from werkzeug.middleware.proxy_fix import ProxyFix

# Load environment variables
load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'mindstoke.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 20,  # Increased from 10 to handle more concurrent requests
        'pool_recycle': 1800,  # Reduced from 3600 to recycle connections more frequently
        'pool_pre_ping': True,
        'pool_timeout': 30,  # Added timeout for connection acquisition
        'max_overflow': 10  # Allow up to 10 additional connections when pool is full
    }
    
    # Configure upload folders
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    app.config['RESULTS_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'extracted_results')
    
    # Base URL for external links
    app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:5000')
    
    # Email configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    # HHQ configuration
    app.config['HHQ_EXPIRATION_DAYS'] = config_class.HHQ_EXPIRATION_DAYS
    app.config['HHQ_AUTOSAVE_INTERVAL'] = config_class.HHQ_AUTOSAVE_INTERVAL
    
    # Configure logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/mindstoke.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Mindstoke startup')
    
    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)
    
    # Configure CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    # Add ProxyFix middleware for proper handling of proxy headers
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    with app.app_context():
        # Import routes
        from .routes import main, auth, clients, reports, hhq, roadmap
        from .routes.client_images import client_images_bp
        
        # Register blueprints
        app.register_blueprint(main.main)
        app.register_blueprint(auth.bp)
        app.register_blueprint(clients.bp)
        app.register_blueprint(reports.bp)
        app.register_blueprint(hhq.bp)
        app.register_blueprint(roadmap.bp)
        app.register_blueprint(client_images_bp)
        
        # Create database tables
        db.create_all()
        
        # Register CLI commands
        from .commands import create_admin_command, recreate_db_command
        app.cli.add_command(create_admin_command)
        app.cli.add_command(recreate_db_command)
    
    # Exempt auth routes from CSRF (moved outside app context)
    csrf.exempt(auth.bp)
    
    return app 