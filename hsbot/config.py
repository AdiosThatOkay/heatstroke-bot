import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///database/heatstroke.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN',
                                           'DUMMY_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET',
                                     'DUMMY_SECRET')
DEBUG = True
