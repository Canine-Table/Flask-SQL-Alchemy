from wtforms import SubmitField,TextAreaField,BooleanField,RadioField,HiddenField
from wtforms.validators import Length,DataRequired
from flask_wtf import FlaskForm
from alchemy.administration.routes import data


class InspectQueryForm(FlaskForm):
    # pending_query = HiddenField(id="pending_query_id",name="pending_query",default=data['pending_query'])
    # json_key = HiddenField(id="json_key_id",name="json_key",default=data['json_key'])
    # md5_hash = HiddenField(id="md5_hash_id",name="md5_hash",default=data['md5_hash'])
    # file_path = HiddenField(id="file_path_id",name="file_path",default=data['file_path'])
    text_body = TextAreaField(label="Query Database",id="query_database_text_body",render_kw={"class":"mt-1 rounded p-2 col-12",'placeholder':'Query Database','data-bs-theme':'dark'},validators=[Length(max=16383, message="Query body must be between 1 and 16383 characters, please enter shortener queries.")])
    rollback = BooleanField(label="Rollback")
    commit = BooleanField(label="Commit")
    radios = RadioField(label='Choices to Query', choices=[('query_database','Query Database'),('query_query_dump','Query History Logs'),('query_error_dump','Query Error Logs')])
    submit_inspect_query_form = SubmitField(label="Submit Query",id='submit_query_choice',render_kw={"class":"btn btn-primary col-12"})
