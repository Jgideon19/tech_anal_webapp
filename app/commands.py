import click
from flask.cli import with_appcontext
from .utils import TechnicalAnalysisPlatform
from . import db
import datetime
from datetime import timedelta

@click.command('load-data')
@with_appcontext
def load_data():
    platform = TechnicalAnalysisPlatform(db.session)
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'NVDA', 'META', 'AVGO', 'ORCL', 'ADBE', 'CSCO',
        'CRM', 'ACN', 'QCOM', 'INTC', 'AMD', 'TXN', 'IBM', 'MU', 'INTU', 'AMAT',
        'ADI', 'LRCX', 'NOW', 'SNPS', 'CDNS', 'AMZN', 'NFLX', 'PYPL', 'SHOP', 'SQ',
        'ZM', 'TWLO', 'SPOT', 'DOCU', 'ROKU', 'UBER', 'LYFT', 'BABA', 'JD', 'PDD'] # Your list of tickers
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')  # Get last 5 days of data
    platform.load_historical_data(tickers, start_date, end_date)

@click.command('update-stock-data')
@with_appcontext
def update_stock_data():
    platform = TechnicalAnalysisPlatform(db.session)
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'NVDA', 'META', 'AVGO', 'ORCL', 'ADBE', 'CSCO',
        'CRM', 'ACN', 'QCOM', 'INTC', 'AMD', 'TXN', 'IBM', 'MU', 'INTU', 'AMAT',
        'ADI', 'LRCX', 'NOW', 'SNPS', 'CDNS', 'AMZN', 'NFLX', 'PYPL', 'SHOP', 'SQ',
        'ZM', 'TWLO', 'SPOT', 'DOCU', 'ROKU', 'UBER', 'LYFT', 'BABA', 'JD', 'PDD'] # Your list of tickers
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')  # Update last week's data
    platform.load_historical_data(tickers, start_date, end_date)
    click.echo('Stock data update complete.')

def init_app(app):
     app.cli.add_command(load_data)