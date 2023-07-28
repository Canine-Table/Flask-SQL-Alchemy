from flask import render_template
from flask import Blueprint


main = Blueprint('main',__name__,template_folder='templates',static_folder='static',static_url_path='/main/static')


@main.route('/')
@main.route('/home')
def home_page():
    return render_template('home.html')
