from flask import render_template,request,url_for,flash,redirect,current_app
from alchemy.administration.utils import json_database
from alchemy.administration.forms import InspectQueryForm
from flask_login import current_user,login_required
from alchemy.utils import error_log,error_string
from alchemy.main.jinja2env import jinja2_env
from flask import render_template
from flask import Blueprint
from sqlalchemy import text
from alchemy import engine
import os

administration = Blueprint('administration',__name__,template_folder='templates',static_folder='static')


@administration.route('/<username>/administration/inspector', methods=['GET','POST'])
@login_required
def inspector_page(username):
    if current_user.username in ['root','johndoe0123','administrator']:
        form=InspectQueryForm()
        frozen = {}
        frozen['not_set'] = True
        if request.method == 'POST':
            with engine.connect() as conn:
                static_folder = os.path.join(current_app.root_path, 'administration', 'static')
                try:
                    query = form.text_body.data
                    data = conn.execute(text(f"{query}"))

                    frozen['headers'] = data.keys()
                    frozen['rows'] = data.freeze()
                    frozen['not_set'] = False

                    if form.rollback.data:
                        conn.rollback()

                    if form.commit.data:
                        conn.commit()

                    json_database(query,frozen)

                except Exception as e:
                    file_dump = os.path.join(static_folder,'json','_error_logs.json')

                    flash(f"{type(e).__name__}: {error_string(error=e)}",category="danger")
                    error_log(error=e,file_dump=file_dump)

        return render_template('inspect.html',env=jinja2_env,form=form,data=frozen )
    else:
        return redirect(url_for('main.home_page'))
