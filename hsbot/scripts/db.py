from flask_script import Command
from hsbot import (
    app, db
)
from hsbot.models.users import User
from hsbot.models.observatories import Observatory
import csv
import os.path


class InitDB(Command):
    "create database"

    def run(self):
        db.create_all()


class InsertCSV(Command):
    "insert observatories data from csv"

    def run(self):
        csv_path = os.path.join(app.root_path,
                                'database/all_observatories_2019.csv')
        with open(csv_path) as csv_obj:
            reader = csv.reader(csv_obj)
            for row in reader:
                if reader.line_num == 1:
                    continue
                observatory = Observatory(
                    code=row[1], pref=row[0], name=row[3], name_kana=row[4],
                    location=row[5], lat_deg=row[6], lat_min=row[7],
                    lon_deg=row[8], lon_min=row[9])
                db.session.add(observatory)
            db.session.commit()
