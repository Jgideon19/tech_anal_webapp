from sqlalchemy import Column, Integer, String, Float, Date
from .database import db

class StockData(db.Model):
    __tablename__ = 'stock_data'

    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    ma_200 = Column(Float)
    ma_50 = Column(Float)
    ma_20 = Column(Float)
    ma_9 = Column(Float)
    rsi = Column(Float)
    vwap = Column(Float)
