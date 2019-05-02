from flask_script import Command
from hsbot import db
from hsbot.models.users import User
from hsbot.models.observatories import Observatory


class InitDB(Command):
    "create database"

    def run(self):
        db.create_all()
