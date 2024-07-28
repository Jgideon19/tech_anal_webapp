from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class LoadDataForm(FlaskForm):
    tickers = StringField('Tickers (comma-separated)', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Load Data')

class AnalyzeStockForm(FlaskForm):
    ticker = StringField('Ticker', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Analyze')
