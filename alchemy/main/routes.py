from alchemy.main.jinja2env import jinja2_env
from flask import render_template
from flask import Blueprint


main = Blueprint('main',__name__)


@main.route('/')
@main.route('/home')
def home_page():
    return render_template('home.html',env=jinja2_env)
