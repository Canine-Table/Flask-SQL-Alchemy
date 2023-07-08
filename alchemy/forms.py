from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError,Regexp
from wtforms import StringField,SubmitField,PasswordField,EmailField,BooleanField
from flask_wtf import FlaskForm

class RegistrationForm(FlaskForm):
    username=StringField("Username", validators=[DataRequired(),Length(min=2,max=32)])
    first_name=StringField("Name", validators=[DataRequired(),Length(min=1,max=32)])
    last_name=StringField("Last name", validators=[DataRequired(),Length(min=1,max=32)])
    password=PasswordField("Password", validators=[DataRequired(),Length(min=6,max=60)])
    verify_password=PasswordField("Confirm password", validators=[DataRequired(),EqualTo("password"),Length(min=6,max=60)])
    email_address=EmailField("Email address", validators=[DataRequired(),Length(min=16,max=64)])
    phone_number=StringField("Phone Number", validators=[DataRequired(),Length(min=12,max=12)])
    submit = SubmitField(label="Create Account")

class LoginForm(FlaskForm):
    username = StringField("Username:",validators=[DataRequired()])
    password = PasswordField("Password:",validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField(label="Sign in")

class DeleteAccountForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    submit = SubmitField(label="Delete Account")

class EditAccountForm(FlaskForm):
    first_name=StringField("First Name", validators=[DataRequired(),Length(min=1,max=32)])
    last_name=StringField("Last name", validators=[DataRequired(),Length(min=1,max=32)])
    email_address=EmailField("Email address", validators=[DataRequired(),Length(min=16,max=64)])
    phone_number=StringField("Phone Number", validators=[DataRequired(),Length(min=12,max=12)])
    submit = SubmitField(label="Save Changes")

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField("Old Password:",validators=[DataRequired()])
    new_password = PasswordField("New Password:",validators=[DataRequired()])
    confirm_new_password = PasswordField("Confirm Password:",validators=[DataRequired()])
    submit = SubmitField(label="Reset")
