from flask import render_template,request,url_for,flash,redirect,current_app
from flask import render_template,request,flash,get_flashed_messages
from flask_login import current_user,login_required
from alchemy.utilities.database import Session
from alchemy.utils import error_log
from alchemy.sandbox.forms import FormValidationForm
from flask import Blueprint
import json


sandbox = Blueprint('sandbox',__name__,template_folder='templates',static_folder='static',static_url_path='/sandbox/static')

@sandbox.route('/<username>/sandbox/forms', methods=['GET','POST'])
@login_required
def form_validation_page(username):
    if current_user.groups.user_group == 'root_users':
        form=FormValidationForm()
        if request.method == "POST":
            form_data =  form.inputbox.data
            print(form_data)
            flash(f"{form_data}",category="success")
        return render_template('form_validation.html',form=form)
    else:
        return redirect(url_for('main.home_page'))
