from alchemy.utils import get_configurations
import secrets
import os


class Config:
    FLASK_DEBUG = True
    WTF_CSRF_TIME_LIMIT = 1800
    SECRET_KEY = secrets.token_hex(32)
    WTF_CSRF_FIELD_NAME = 'flask_csrf_token'
    WTF_CSRF_SECRET_KEY = secrets.token_bytes(32)
    SCSS_STATIC_DIR = os.path.join(os.path.realpath('./'),'alchemy','static')
    SCSS_ASSET_DIR =  os.path.join(os.path.realpath('./'),'alchemy','utilities','static','assets')
    if get_configurations(False):
        SQLALCHEMY_TRACK_MODIFICATIONS = True
