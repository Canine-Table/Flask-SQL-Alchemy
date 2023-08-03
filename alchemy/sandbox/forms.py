from wtforms import StringField,SubmitField,TextAreaField,BooleanField,RadioField
from wtforms.validators import Length,EqualTo,DataRequired,Email
from flask_wtf import FlaskForm
from markupsafe import Markup,escape



class FormValidationForm(FlaskForm):
    inputbox = StringField(DataRequired(),)
    submit = SubmitField(id='FormValidationFormId',render_kw={'style':'background-color: transparent;color: transparent; height:0px; width:0px; border: none; position: absolute;'})
