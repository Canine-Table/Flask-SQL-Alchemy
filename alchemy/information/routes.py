from flask import render_template,request,url_for,flash,redirect,current_app
from alchemy.information.utils import filter_results,n_to_br
from flask_login import current_user,login_required
from alchemy.information.forms import SearchModule
from flask import render_template
from flask import Blueprint
import subprocess
import json


information = Blueprint('information',__name__,template_folder='templates',static_folder='static',static_url_path='/information/static')


@information.route('/information/modules/versions',methods=['GET','POST'])
@login_required
def version_page():
    if current_user.groups.user_group in ['root_users','privilaged_users']:
        form=SearchModule()
        pip3_modules = {}
        pip3_modules['load'] = None
        pip3_modules['TypeNone'] = False
        pip3_modules['names_n_versions'] = json.loads(subprocess.check_output(["pip", "list","--format","json"]).decode())
        pip3_modules['names'] = [modules['name'] for modules in pip3_modules['names_n_versions']]
        if request.method == 'POST':
            if request.form['get_more_info']:
                pip3_modules['load'] = request.form['get_more_info']
            else:
                pip3_modules['load'] = None

            pip3_modules['names_n_versions'] = json.loads(subprocess.check_output(["pip", "list","--format","json"]).decode())
            filter_result = filter_results(form.search.data,pip3_modules['names'])
            if filter_result == None:
                pip3_modules['TypeNone'] = True
            else:
                pip3_modules['names'] = filter_result
            if pip3_modules['load'] != 'None':
                return redirect(url_for('information.module_info_page',module_name=pip3_modules['load']))
        return render_template('versions.html',form=form,pip3_modules=pip3_modules)
    else:
        return redirect(url_for('main.home_page'))


@information.route('/information/presentation')
@login_required
def presentation_page():
    if current_user.groups.user_group in ['root_users','privilaged_users']:
        return render_template('presentation.html')
    else:
        return redirect(url_for('main.home_page'))


@information.route('/information/modules/<module_name>',methods=['GET'])
@login_required
def module_info_page(module_name):
    if current_user.groups.user_group in ['root_users','privilaged_users']:
        get_module_info = subprocess.check_output(["pip", "show",f"{module_name}"]).decode()
        module_info = n_to_br(get_module_info)

        return render_template('module_information.html',module_name=module_name,module_info=module_info)
    else:
        return redirect(url_for('main.home_page'))


@information.route('/information/css',methods=['GET'])
@login_required
def cascading_style_sheets_info_page():
    if current_user.groups.user_group == 'root_users':
        return render_template('cascading_style_sheets.html')
    else:
        return redirect(url_for('main.home_page'))

@information.route('/information/sql/setup',methods=['GET'])
@login_required
def sql_setup_page():
    if current_user.groups.user_group == 'root_users':
        return render_template('sql_setup.html')
    else:
        return redirect(url_for('main.home_page'))
