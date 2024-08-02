from flask import Flask
from .database import db
from flask_migrate import Migrate
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    with app.app_context():
        # Import parts of our application
        from .views import main_bp
        
        # Register blueprints
        app.register_blueprint(main_bp)

        # Create database tables for our data models
        db.create_all()

        logger.info("Application instance created and configured")

    return app