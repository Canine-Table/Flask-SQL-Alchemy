from wtforms import StringField,SubmitField,TextAreaField,BooleanField,RadioField
from wtforms.validators import Length,EqualTo,DataRequired,Email
from flask_wtf import FlaskForm

class InspectQueryForm(FlaskForm):
    text_body = TextAreaField()
    rollback = BooleanField()
    commit = BooleanField()
    example = RadioField('Label', choices=[('query_database','Query Database'),('query_query_dump','Query History Logs'),('query_error_dump','Query Error Logs')])
    submit = SubmitField(label="Submit Query")
