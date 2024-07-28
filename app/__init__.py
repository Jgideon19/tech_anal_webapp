from flask import Flask
from .database import db
from .utils import TechnicalAnalysisPlatform
from .models import StockData

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        from .views import main_bp
        app.register_blueprint(main_bp)
        db.create_all()

        # Automatically load tickers
        platform = TechnicalAnalysisPlatform(db.session)
        tickers = tickers = ['WMT', 'HPQ', 'BMRN', 'DAL', 'KEYS', 'NOW',
               'SJI', 'ECL', 'TRV', 'LOGC', 'LLY', 'ISRG',
               'PNC', 'LSI', 'ONCS', 'TXN', 'PRGO', 'BIDU',
               'GS', 'CMS', 'SPLK', 'SGEN', 'CWT', 'SO',
               'EXR', 'CVAC', 'MDLZ', 'TFC', 'DHC', 'SNAP',
               'HTA', 'PGR', 'EMR', 'BIIB', 'APDN', 'WFC',
               'SJW', 'PAYC', 'AGEN', 'NBIX', 'ITW', 'ED',
               'HUM', 'KRC', 'PNW', 'ADBE', 'ORCL', 'JPM',
               'LVGO', 'WYNN', 'FUTU', 'FVRR', 'ES', 'MU',
               'ETN', 'D', 'TJX', 'REGN', 'PSTI', 'TSLA',
               'ASND', 'MORF', 'AEE', 'MPC', 'FIXX', 'LI',
               'PCTY', 'AFL', 'MSFT', 'EW', 'NWE', 'COF',
               'MCD', 'QURE', 'SYK', 'FATE', 'AXDX', 'IDA',
               'DLTR', 'ARCT', 'GSX', 'AIV', 'SPGI', 'INO',
               'YY', 'KNSA', 'OTTR', 'ARE', 'FLXN', 'MREO',
               'CPT', 'AES', 'WTRG', 'BEKE', 'HPE', 'NIO',
               'ALXN', 'TCRR', 'CARA', 'CVX', 'ZSAN', 'BZUN',
               'TIGIT', 'ITCI', 'SBUX', 'SHOP', 'EVRG', 'GNFT',
               'GENI', 'NVAX', 'CAPR', 'HCA', 'CMCSA', 'WIX',
               'AFRM', 'BSX', 'ABT', 'SRC', 'MNST', 'VZ', 'INFI',
               'NTGN', 'FIS', 'AXP', 'PEAK', 'VEEV', 'SWTX', 'MSCI',
               'PTC', 'DOCU', 'HIW', 'PFE', 'PRTA', 'RGNX', 'FITB',
               'MMC', 'QCOM', 'BCLI', 'FSLY', 'OHI', 'CRM', 'V', 'NVDA',
               'USB', 'ALE', 'EIDX', 'PNM', 'RGEN', 'ICE', 'MELI', 'ROST',
               'AVGO', 'UDR', 'ONCR', 'ADI', 'ZNTL', 'GLPG', 'AMZN',
               'HST', 'TGT', 'TWST', 'VXRT', 'AON', 'XLRN', 'CAT',
               'TXG', 'CVNA', 'INTC', 'PM', 'META', 'ACN', 'CSCO',
               'VRTX', 'PCVX', 'CL', 'MBOT', 'PRU', 'BCYC', 'IRM',
               'EDIT', 'XOM', 'IQ', 'HGEN', 'HHC', 'MCHP', 'FFIV',
               'DVAX', 'PTON', 'AVRO', 'COE', 'XNCR', 'EOG', 'PG',
               'UNH', 'UPS', 'AIG', 'MAA', 'UPWK', 'HPP', 'XP', 'QGEN',
               'AVIR', 'AUTL', 'MCO', 'AAPL', 'KOD', 'DUK', 'SBRA',
               'XENE', 'FISV', 'NEM', 'TTD', 'AXSM', 'ZM', 'NVS', 'MSEX',
               'NFLX', 'VICI', 'EIX', 'RTX', 'SRNE', 'TDOC', 'O', 'XAIR',
               'CERN', 'MA', 'NSTG', 'SNY', 'JD', 'CMG', 'EDU', 'BLK',
               'XEL', 'WEC', 'IBM', 'OGE', 'GRMN', 'SPG', 'CUBE', 'EBS',
               'SMAR', 'VTR', 'NTLA', 'HON', 'TWTR', 'STT', 'BK', 'GLYC',
               'CYTK', 'PINS', 'ADP', 'CLX', 'MS', 'CI', 'CNP', 'FRT', 'BGNE',
               'KO', 'W', 'ATVI', 'BLU', 'VNO', 'BTA', 'ZEN', 'BPMC', 'RPRX',
               'NET', 'ABBV', 'ADSK', 'IMTX', 'MDT', 'WDAY', 'NLTX', 'VERV',
               'ESS', 'CEMI', 'RARE', 'NEE', 'DDOG', 'SAN', 'NHI', 'ILMN',
               'TMO', 'ZYME', 'AMT', 'T', 'ANSS', 'BFS', 'TIGR', 'HD', 'LMT',
               'SE', 'MRSN', 'BDX', 'PLD', 'EQIX', 'ATO', 'HTBX', 'DIS', 'DTE',
               'APD', 'ETSY', 'BKNG', 'GE', 'TGTX', 'STTK', 'SRE', 'UNP', 'YORW',
               'RCUS', 'HE', 'CRWD', 'NOC', 'KR', 'OKTA', 'LOW', 'NSA', 'YUM', 'HR',
               'DXC', 'BAND', 'LSPD', 'GMAB', 'NTRA', 'DAO', 'ROG', 'AKAM', 'RNA',
               'TAK', 'TPTX', 'MGTA', 'CB', 'C', 'KMI', 'CTIC', 'SNOW', 'RF', 'HCM',
               'WPC', 'SQ', 'GM', 'DE', 'GBT', 'BMY', 'PYPL', 'ANAB', 'CLOV', 'GILD',
               'PACB', 'DHR', 'MRNA', 'ROK', 'PEG', 'SBSI', 'EL', 'XOMA', 'RDHL', 'ELV',
               'MO', 'XPEV', 'VIPS', 'DOC', 'BXP', 'TEAM', 'PGEN', 'DNLI', 'SGMO', 'ABUS',
               'BILI', 'CRSP', 'CME', 'WORK', 'SPOT', 'DOW', 'KALA', 'REPL', 'ROKU', 'NKE',
               'BTAI', 'MMM', 'SYY', 'INCY', 'BLUE', 'PEP', 'NATI', 'ALT', 'TME', 'BABA', 'PDD',
               'AEP', 'DADA', 'NSC', 'BOX', 'PSA', 'PPL', 'YSG', 'FOLD', 'CNC', 'SWX', 'OCGN', 'CODX',
               'AMD', 'BA', 'TLRY', 'CEG', 'ATHX', 'NXTC', 'F', 'ZTS', 'SAVA', 'AVB', 'ORTX', 'FDX', 'EVBG',
               'ALNY', 'MET', 'ZLAB', 'CMRX', 'DIDI', 'PTE', 'HIG', 'AMGN', 'CALT', 'OXY', 'BEAM', 'COST', 'MRK',
               'POR', 'EQR', 'SRPT', 'ALL', 'HUYA', 'SCHW', 'ZS', 'GDS', 'INOV', 'VYGR', 'AMP', 'BNTX', 'ABCL', 'CHCT',
               'WB', 'NI', 'TRMB', 'KMB', 'MDB', 'VLO', 'ASMB', 'TAL', 'SLB', 'MYGN', 'NWN', 'LIN', 'NGM', 'KIM', 'AWK',
               'INTU', 'GMRE', 'WMB', 'MTCH', 'BLKB', 'SYRS', 'MPW', 'QFIN', 'GH', 'EXC', 'OZON', 'AWR', 'CSX', 'GSK',
               'AZN', 'DOYU', 'LRCX', 'JNJ', 'GOOGL']  # Add more tickers as needed
        start_date = '1900-01-01'
        end_date = '2024-07-22'
        platform.load_historical_data(tickers, start_date, end_date)

        for ticker in tickers:
            if not db.session.query(StockData).filter_by(ticker=ticker).first():
                print(f"Loading data for {ticker}")
                platform.load_historical_data([ticker], start_date, end_date)
            else:
                print(f"Data for {ticker} already exists")

    return app
