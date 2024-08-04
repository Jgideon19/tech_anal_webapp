from flask import Flask
from .database import db
from flask_migrate import Migrate
import logging
from flask_apscheduler import APScheduler
from app.utils import TechnicalAnalysisPlatform
import datetime
from datetime import timedelta

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

        @scheduler.task('cron', id='update_stock_data', hour=1)  # Run daily at 1 AM
        def update_stock_data():
            platform = TechnicalAnalysisPlatform(db.session)
            tickers = ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'NVDA', 'META', 'AVGO', 'ORCL', 'ADBE', 'CSCO',
           'CRM', 'ACN', 'QCOM', 'INTC', 'AMD', 'TXN', 'IBM', 'MU', 'INTU', 'AMAT',
           'ADI', 'LRCX', 'NOW', 'SNPS', 'CDNS', 'AMZN', 'NFLX', 'PYPL', 'SHOP', 'SQ',
           'ZM', 'TWLO', 'SPOT', 'DOCU', 'ROKU', 'UBER', 'LYFT', 'BABA', 'JD', 'PDD']
  # Your list of tickers
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')  # Get last 5 days of data
            platform.load_historical_data(tickers, start_date, end_date)

    return app