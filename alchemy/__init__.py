from sqlalchemy import create_engine, inspect
from flask_bcrypt import Bcrypt
from flask import Flask
import os

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.urandom(12).hex()
bcrypt = Bcrypt(app)

class Database:
    db_host = os.environ['DB_HOST']
    db_port = os.environ['DB_PORT']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']

    @classmethod
    def create(cls):
        return create_engine(
            'mysql+pymysql://{}:{}@{}:{}/{}'.format(cls.db_user,cls.db_password,cls.db_host,cls.db_port,cls.db_name),
            echo=True,
            connect_args={"ssl": {
                "ssl_ca": "/etc/ssl/cert.pem",
                "init_command": "SET foreign_key_checks=0"}})

db = Database()
engine = Database.create()
inspector = inspect(engine)

from alchemy import routes
