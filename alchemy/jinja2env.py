from jinja2 import Environment, select_autoescape
from jinja2.ext import do,i18n
from alchemy import app
import secrets


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
        self.globals['secrets'] = secrets


jinja2_env = Jinja2Env()
