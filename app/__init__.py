from flask import Flask
from .database import db
from flask_migrate import Migrate
import logging
from flask_apscheduler import APScheduler
from app.utils import TechnicalAnalysisPlatform
from . import commands

scheduler = APScheduler()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    scheduler.init_app(app)
    scheduler.start()

    with app.app_context():
        # Import parts of our application
        from .views import main_bp
        
        # Register blueprints
        app.register_blueprint(main_bp)

        # Create database tables for our data models
        db.create_all()

        logger.info("Application instance created and configured")

    commands.init_app(app)

    return app