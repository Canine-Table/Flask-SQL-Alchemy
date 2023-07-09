from sqlalchemy import create_engine, inspect
from jinja2 import Environment, PackageLoader, select_autoescape
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from jinja2.ext import do,i18n
from flask import Flask
import os


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.urandom(12).hex()
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
bcrypt = Bcrypt(app)


class Jinja2Env(Environment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comment_start_string = '<#'
        self.comment_end_string = '#>'
        self.autoescape = select_autoescape(disabled_extensions=('txt','log','md',),default_for_string=True,default=True)
        self.trim_blocks = False
        self.lstrip_blocks = False
        self.keep_trailing_newline = False
        self.optimized = True
        self.auto_reload = True
        self.enable_async = True
        self.newline_sequence = '\n'
        self.cache_size = 400
        self.add_extension(do)
        self.add_extension(i18n)


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
env = Jinja2Env(loader=PackageLoader(__name__, 'templates'))


from alchemy import routes
