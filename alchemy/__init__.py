from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from alchemy.config import Config
from flask_bcrypt import Bcrypt
from flask import Flask
from alchemy.main.jinja2env import Jinja2Env
import os

bcrypt = Bcrypt()
login_manager = LoginManager()
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



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from alchemy.main.routes import main
    app.register_blueprint(main)

    from alchemy.market.routes import market
    app.register_blueprint(market)

    from alchemy.accounts.routes import account
    app.register_blueprint(account)

    from alchemy.administration.routes import administration
    app.register_blueprint(administration)

    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app
