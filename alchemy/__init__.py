from sqlalchemy import create_engine
import mysql.connector
from flask import Flask
import os

app = Flask(__name__)

class Database:
    db_host = os.environ['DB_HOST']
    db_port = os.environ['DB_PORT']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_uri = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(db_user,db_password,db_host,db_port,db_name),connect_args={"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}})


db = Database()

from alchemy import routes
