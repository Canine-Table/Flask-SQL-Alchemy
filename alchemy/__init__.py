from alchemy.main.jinja2env import Jinja2Env
from jinja2 import PackageLoader, ChoiceLoader
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from alchemy.config import Config
from flask_bcrypt import Bcrypt
from flask import Flask
import os


app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "account.login_page"
login_manager.login_message_category = "info"


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


engine = Database.create()
Session = sessionmaker(bind=engine)
inspector = inspect(engine)
loaders = []


loaders.append(PackageLoader(package_name='alchemy', package_path='templates', encoding='utf-8'))
loaders.append(PackageLoader(package_name='alchemy.main', package_path='templates', encoding='utf-8'))
from alchemy.main.routes import main
app.register_blueprint(main)


loaders.append(PackageLoader(package_name='alchemy.market', package_path='templates', encoding='utf-8'))
from alchemy.market.routes import market
app.register_blueprint(market)


loaders.append(PackageLoader(package_name='alchemy.accounts', package_path='templates', encoding='utf-8'))
from alchemy.accounts.routes import account
app.register_blueprint(account)


loaders.append(PackageLoader(package_name='alchemy.administration', package_path='templates', encoding='utf-8'))
from alchemy.administration.routes import administration
app.register_blueprint(administration)


loaders.append(PackageLoader(package_name='alchemy.information', package_path='templates', encoding='utf-8'))
from alchemy.information.routes import information
app.register_blueprint(information)


app.jinja_env = Jinja2Env(loader=ChoiceLoader(loaders))
