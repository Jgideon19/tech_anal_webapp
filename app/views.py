from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .database import db
from .models import StockData
from .utils import TechnicalAnalysisPlatform
from .forms import AnalyzeStockForm
from flask_caching import Cache
from celery import Celery
import logging

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

# Setup caching
cache = Cache(config={'CACHE_TYPE': 'simple'})

# Setup Celery
celery = Celery(__name__, broker='redis://localhost:6379/0')

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    analyze_stock_form = AnalyzeStockForm()
    return render_template('index.html', analyze_stock_form=analyze_stock_form)

@main_bp.route('/analyze', methods=['POST'])
def analyze():
    form = AnalyzeStockForm(request.form)
    if form.validate():
        ticker = form.ticker.data
        date = form.date.data
        task = analyze_stock_task.delay(ticker, date)
        return jsonify({"task_id": task.id}), 202
    return jsonify({"error": "Invalid form data"}), 400

@main_bp.route('/task_status/<task_id>')
def task_status(task_id):
    task = analyze_stock_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Task is pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    return jsonify(response)

@celery.task(bind=True)
def analyze_stock_task(self, ticker, date):
    self.update_state(state='PROGRESS', meta={'status': 'Starting analysis...'})
    platform = TechnicalAnalysisPlatform(db.session)
    try:
        results = platform.analyze_stock(ticker, date)
        return {'status': 'Task completed!', 'result': results}
    except Exception as e:
        logger.error(f"Error in stock analysis: {str(e)}")
        return {'status': 'Task failed!', 'error': str(e)}