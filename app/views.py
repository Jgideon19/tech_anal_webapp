from flask import Blueprint, render_template, request, redirect, url_for, flash
from .database import db
from .models import StockData
from .utils import TechnicalAnalysisPlatform
from .forms import AnalyzeStockForm

# Define the blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    analyze_stock_form = AnalyzeStockForm()

    if analyze_stock_form.validate_on_submit() and analyze_stock_form.submit.data:
        ticker = analyze_stock_form.ticker.data
        date = analyze_stock_form.date.data
        
        platform = TechnicalAnalysisPlatform(db.session)
        results = platform.analyze_stock(ticker, date)
        
        return render_template('analysis.html', results=results)

    return render_template('index.html', analyze_stock_form=analyze_stock_form)
