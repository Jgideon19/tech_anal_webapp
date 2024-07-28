from matplotlib import pyplot as plt
import mplfinance as mpf
import pandas as pd
import yfinance as yf
from datetime import timedelta
from .models import StockData
from .database import db

class TechnicalAnalysisPlatform:
    def __init__(self, db_session):
        self.db_session = db_session

    def load_historical_data(self, tickers, start_date, end_date):
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                data = stock.history(start=start_date, end=end_date)
                if data.empty:
                    print(f"No data available for {ticker}. Skipping.")
                    continue
                data.index = data.index.tz_localize(None)
                data = self.calculate_indicators(data)

                for date, row in data.iterrows():
                    stock_data = StockData(
                        ticker=ticker,
                        date=date.date(),
                        open=row['Open'],
                        high=row['High'],
                        low=row['Low'],
                        close=row['Close'],
                        volume=row['Volume'],
                        ma_200=row['200_MA'],
                        ma_50=row['50_MA'],
                        ma_20=row['20_MA'],
                        ma_9=row['9_MA'],
                        rsi=row['RSI'],
                        vwap=row['VWAP']
                    )
                    self.db_session.add(stock_data)

                self.db_session.commit()
                print(f"Data loaded successfully for {ticker} from {data.index.min().date()} to {data.index.max().date()}")
            except Exception as e:
                print(f"Error loading data for {ticker}: {str(e)}")
                self.db_session.rollback()

    def calculate_indicators(self, data):
        data['200_MA'] = data['Close'].rolling(window=200).mean()
        data['50_MA'] = data['Close'].rolling(window=50).mean()
        data['20_MA'] = data['Close'].rolling(window=20).mean()
        data['9_MA'] = data['Close'].rolling(window=9).mean()
        data['RSI'] = self.calculate_rsi(data['Close'], period=14)
        data['VWAP'] = self.calculate_vwap(data)
        return data

    def calculate_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def calculate_vwap(self, data):
        v = data['Volume'].values
        tp = (data['Low'] + data['Close'] + data['High']).div(3).values
        return pd.Series(data=tp.cumsum() / v.cumsum(), index=data.index)

    def analyze_stock(self, ticker, date):
        try:
            return self.find_similar_situations(ticker, date)
        except ValueError as e:
            print(f"Error: {str(e)}")
            return []

    def find_similar_situations(self, ticker, current_date, exclusion_period=365):
        current_date = pd.Timestamp(current_date).date()
        current_data = self.db_session.query(StockData).filter(
            StockData.ticker == ticker,
            StockData.date <= current_date
        ).order_by(StockData.date.desc()).first()

        if not current_data:
            raise ValueError(f"No data available for {ticker} on or before {current_date}")

        similar_situations = []
        exclusion_start = current_date - timedelta(days=exclusion_period)

        all_data = self.db_session.query(StockData).filter(
            StockData.date < current_date
        ).all()

        for row in all_data:
            if row.ticker == ticker and exclusion_start <= row.date <= current_date:
                continue

            similarity_score = self.calculate_similarity(current_data, row)
            if similarity_score > 0.9:  # Arbitrary threshold, adjust as needed
                similar_situations.append({
                    'date': row.date.strftime('%Y-%m-%d'),
                    'ticker': row.ticker,
                    'similarity_score': similarity_score
                })

        return sorted(similar_situations, key=lambda x: x['similarity_score'], reverse=True)

    def calculate_similarity(self, current, historical):
        indicators = ['ma_200', 'ma_50', 'ma_20', 'ma_9', 'rsi', 'vwap']
        differences = []
        for indicator in indicators:
            current_value = getattr(current, indicator)
            historical_value = getattr(historical, indicator)
            if current_value is not None and historical_value is not None and current_value != 0:
                diff = abs(current_value - historical_value) / current_value
                differences.append(1 - diff)
        return sum(differences) / len(differences) if differences else 0

    def get_available_date_range(self, ticker):
        min_date = self.db_session.query(StockData.date).filter(StockData.ticker == ticker).order_by(StockData.date.asc()).first()
        max_date = self.db_session.query(StockData.date).filter(StockData.ticker == ticker).order_by(StockData.date.desc()).first()

        if not min_date or not max_date:
            raise ValueError(f"No data available for {ticker}")

        return min_date[0], max_date[0]

    def plot_comparison(self, ticker, date, similar_situation, window=30):
        current_date = pd.Timestamp(date).date()
        similar_date = pd.Timestamp(similar_situation['date']).date()

        current_data = pd.DataFrame(self.db_session.query(StockData).filter(
            StockData.ticker == ticker,
            StockData.date.between(current_date - timedelta(days=window), current_date + timedelta(days=window))
        ).all())

        similar_data = pd.DataFrame(self.db_session.query(StockData).filter(
            StockData.ticker == similar_situation['ticker'],
            StockData.date.between(similar_date - timedelta(days=window), similar_date + timedelta(days=window))
        ).all())

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

        mpf.plot(current_data.set_index('date'), type='candle', style='yahoo', ax=ax1)
        ax1.set_title(f'{ticker} around {date}')
        ax1.axvline(current_date, color='r', linestyle='--', label='Analysis Date')
        ax1.legend()

        mpf.plot(similar_data.set_index('date'), type='candle', style='yahoo', ax=ax2)
        ax2.set_title(f'{similar_situation["ticker"]} around {similar_situation["date"]}')
        ax2.axvline(similar_date, color='r', linestyle='--', label='Similar Date')
        ax2.legend()

        plt.tight_layout()
        plt.show()
