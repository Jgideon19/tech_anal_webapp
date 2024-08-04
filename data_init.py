import logging
from app import create_app, db
from app.models import StockData
from app.utils import TechnicalAnalysisPlatform

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_data():
    app = create_app()
    with app.app_context():
        platform = TechnicalAnalysisPlatform(db.session)
        tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB']  # Add your list of tickers
        start_date = '2020-01-01'  # Adjust as needed
        end_date = '2024-08-04'  # Use current date in production

        logger.info("Starting data initialization...")
        platform.load_historical_data(tickers, start_date, end_date)
        logger.info("Data initialization complete.")

if __name__ == "__main__":
    initialize_data()