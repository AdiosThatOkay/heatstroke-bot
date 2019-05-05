from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)
app.config.from_object('hsbot.config')

db = SQLAlchemy(app)

import hsbot.views

scheduler = BackgroundScheduler()


@scheduler.scheduled_job('cron', hour='7-21', minute='5,35')
def request_for_check():
    requests.get('http://localhost:5000/check')


@scheduler.scheduled_job('cron', hour='7')
def request_every_morning():
    requests.get('http://localhost:5000/morning')


scheduler.start()
