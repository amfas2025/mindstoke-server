from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from .routes.labs import labs_bp

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mindstoke.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    app.config['RESULTS_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'extracted_results')
    
    # Ensure upload directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from .routes import auth, main, clients, reports
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(clients.bp)
    app.register_blueprint(reports.bp)
    app.register_blueprint(labs_bp, url_prefix='/labs')
    
    # Register CLI commands
    from .commands import create_admin_command
    app.cli.add_command(create_admin_command)
    
    return app 