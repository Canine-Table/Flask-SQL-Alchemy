from wtforms import StringField,SubmitField,TextAreaField,BooleanField,RadioField
from wtforms.validators import Length,EqualTo,DataRequired,Email
from flask_wtf import FlaskForm
from flask import Markup

class FormValidationForm(FlaskForm):
    inputbox = StringField(DataRequired(),)
    submit = SubmitField('submit')
