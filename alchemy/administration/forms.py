from wtforms import StringField,SubmitField,TextAreaField,BooleanField
from wtforms.validators import Length,EqualTo,DataRequired,Email
from flask_wtf import FlaskForm

class InspectQueryForm(FlaskForm):
    text_body = TextAreaField()
    rollback = BooleanField()
    commit = BooleanField()
    submit = SubmitField(label="Submit Query")
