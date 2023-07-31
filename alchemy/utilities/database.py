from sqlalchemy import create_engine,inspect
from alchemy.utils import get_configurations
from sqlalchemy.orm import sessionmaker
import os


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
            echo=get_configurations(False),
            connect_args={"ssl": {
                "ssl_ca": "/etc/ssl/cert.pem",
                "init_command": "SET foreign_key_checks=0"}})


engine = Database.create()
Session = sessionmaker(bind=engine)
inspector = inspect(engine)
