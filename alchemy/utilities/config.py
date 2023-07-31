from alchemy.utils import get_configurations
import secrets
import os


class Config:
    SECRET_KEY = secrets.token_hex(12)
    SCSS_STATIC_DIR = os.path.join(os.path.realpath('./'),'alchemy','static')
    SCSS_ASSET_DIR =  os.path.join(os.path.realpath('./'),'alchemy','utilities','static','assets')
    FLASK_DEBUG = True
    if get_configurations(False):
        SQLALCHEMY_TRACK_MODIFICATIONS = True
