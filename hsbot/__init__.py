from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)
app.config.from_object('hsbot.config')

db = SQLAlchemy(app)

import hsbot.views

scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', seconds=10)
def polling():
    requests.get('http://localhost:5000/check')


scheduler.start()
