from flask_script import Manager
from hsbot import app
from hsbot.scripts.db import (
    InitDB, InsertCSV
)

if __name__ == '__main__':
    manager = Manager(app)
    manager.add_command('init_db', InitDB())
    manager.add_command('insert_observatories', InsertCSV())
    manager.run()
