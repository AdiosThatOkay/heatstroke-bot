from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('hsbot.config')

db = SQLAlchemy(app)

import hsbot.views
