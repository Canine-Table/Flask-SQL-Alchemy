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
import json
import os

administration = Blueprint('administration',__name__,template_folder='templates',static_folder='static')


@administration.route('/<username>/administration/inspector', methods=['GET','POST'])
@login_required
def inspector_page(username):
    if current_user.username in ['root','johndoe0123','administrator']:
        static_folder = os.path.join(current_app.root_path, 'administration', 'static')
        error_dump = os.path.join(static_folder,'json','_error_logs.json')
        query_dump = os.path.join(static_folder,'json','_query_logs.json')

        data = {}
        form=InspectQueryForm()
        data['pending_query'] = False
        data['frozen_not_set'] = True
        data['selected'] = None
        data['md5_hash'] = None
        data['done_query'] = 0

        if not os.path.exists(query_dump):
            with open(query_dump, 'w'):
                pass

        if os.path.getsize(query_dump) != 0:
            with open(query_dump) as f:
                loaded_query_dump = json.load(f)
        else:
            loaded_query_dump = None

        if not os.path.exists(error_dump):
            with open(error_dump, 'w'):
                pass

        if os.path.getsize(error_dump) != 0:
            with open(error_dump) as f:
                loaded_error_dump = json.load(f)
        else:
            loaded_error_dump = None

        if request.method == 'POST':

            if request.form['md5_hash'] != None:
                data['md5_hash'] = request.form['md5_hash']
            else:
                data['md5_hash'] = None


            if request.form['pending_query'] == 'True':
                data['pending_query'] = True
            else:
                data['pending_query'] = False


            with engine.connect() as conn:
                try:
                    data['selected'] = request.form['inlineRadioOptions']
                    match data['selected']:
                        case 'query_database':
                            query = form.text_body.data
                            _data = conn.execute(text(f"{query}"))

                            data['frozen_headers'] = _data.keys()
                            data['frozen_rows'] = _data.freeze()
                            data['frozen_not_set'] = False

                            if form.rollback.data:
                                conn.rollback()

                            if form.commit.data:
                                conn.commit()

                            json_database(query,data)
                        case 'query_query_dump':
                            data['frozen_not_set'] = False
                        case 'query_error_dump':
                            data['frozen_not_set'] = False
                        case _:
                            raise



                except Exception as e:

                    flash(f"{type(e).__name__}: {error_string(error=e)}",category="danger")
                    error_log(error=e,file_dump=error_dump)

        return render_template('inspect.html',env=jinja2_env,form=form,data=data,loaded_query_dump=loaded_query_dump,loaded_error_dump=loaded_error_dump)
    else:
        return redirect(url_for('main.home_page'))
