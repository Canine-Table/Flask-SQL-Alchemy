from flask import render_template,request,url_for,flash,get_flashed_messages,redirect
from jinja2 import Environment, select_autoescape
from jinja2.ext import do,i18n,loopcontrols
import secrets
import sys

class Jinja2Env(Environment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.autoescape = select_autoescape(disabled_extensions=('txt','log','md',),default_for_string=True,default=True)

        self.add_extension(loopcontrols)
        self.add_extension(i18n)
        self.add_extension(do)

        self.globals['secrets'] = secrets
        self.globals['python_version'] = sys.version
        self.globals['python_version_info'] = sys.version_info
        self.globals['redirect'] = redirect
        self.globals['url_for'] = url_for
        self.globals['get_flashed_messages'] = get_flashed_messages
        self.globals['flash'] = flash
        self.globals['str'] = str
        self.globals['int'] = int
        self.globals['bool'] = bool
        self.globals['float'] = float
        self.globals['object'] = object
        self.globals['dir'] = dir
        self.globals['None'] = None
        self.globals['null'] = None
        self.globals['type'] = type

