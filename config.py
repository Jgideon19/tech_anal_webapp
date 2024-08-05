import os

class Config:
    SECRET_KEY = os.getenv('b\x98\x9a\x12\x8d\x7f\x9b\x9a\x1b\x8e\x9f\x8b\x7d\x6e\xaf\xae\xba\x9c\x8d\x9b\x1e\x8a\x7e\xaf\xde', 'my_secret_key')  # Add a strong secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:////var/app/current/stock_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
