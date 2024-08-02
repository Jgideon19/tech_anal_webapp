from flask import Blueprint, render_template, request, redirect, url_for, flash
from .database import db
from .models import StockData
from .utils import TechnicalAnalysisPlatform
from .forms import AnalyzeStockForm
import logging

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    analyze_stock_form = AnalyzeStockForm()

    if analyze_stock_form.validate_on_submit() and analyze_stock_form.submit.data:
        ticker = analyze_stock_form.ticker.data
        date = analyze_stock_form.date.data

        platform = TechnicalAnalysisPlatform(db.session)
        try:
            results = platform.analyze_stock(ticker, date)
            return render_template('analysis.html', results=results)
        except ValueError as e:
            flash(str(e), "warning")
            logger.warning(f"ValueError in stock analysis: {str(e)}")
        except Exception as e:
            flash("An unexpected error occurred. Please try again later.", "danger")
            logger.error(f"Unexpected error in stock analysis: {str(e)}")

    return render_template('index.html', analyze_stock_form=analyze_stock_form)