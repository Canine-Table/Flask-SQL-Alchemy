from alchemy.utilities.jinja2env import Jinja2Env
from jinja2 import PackageLoader, ChoiceLoader
from alchemy.utilities.config import Config
from flask_login import LoginManager
from flask_webpack import Webpack
from flask_bcrypt import Bcrypt
from flask_scss import Scss
from flask import Flask


bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_message_category = "info"
login_manager.login_view = "account.login_page"


def create_app(specify_config=None):

    app = Flask(__name__)

    if specify_config == None:
        app.config.from_object(Config)
    else:
        app.config.from_object(specify_config)


    Jinja2Env.loaders.append(PackageLoader(package_name='alchemy', package_path='templates', encoding='utf-8'))
    Jinja2Env.loaders.append(PackageLoader(package_name='alchemy.main', package_path='templates', encoding='utf-8'))
    from alchemy.main.routes import main
    app.register_blueprint(main)


    Jinja2Env.loaders.append(PackageLoader(package_name='alchemy.market', package_path='templates', encoding='utf-8'))
    from alchemy.market.routes import market
    app.register_blueprint(market)


    Jinja2Env.loaders.append(PackageLoader(package_name='alchemy.accounts', package_path='templates', encoding='utf-8'))
    from alchemy.accounts.routes import account
    app.register_blueprint(account)


    Jinja2Env.loaders.append(PackageLoader(package_name='alchemy.administration', package_path='templates', encoding='utf-8'))
    from alchemy.administration.routes import administration
    app.register_blueprint(administration)


    Jinja2Env.loaders.append(PackageLoader(package_name='alchemy.information', package_path='templates', encoding='utf-8'))
    from alchemy.information.routes import information
    app.register_blueprint(information)


    app.jinja_env = Jinja2Env(loader=ChoiceLoader(Jinja2Env.loaders))


    login_manager.init_app(app)
    bcrypt.init_app(app)
    Scss(app,static_dir=app.config['SCSS_STATIC_DIR'],asset_dir=app.config['SCSS_ASSET_DIR'])

    return app
