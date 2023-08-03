from wtforms import StringField,SubmitField,PasswordField,EmailField,BooleanField,DateField,TelField
from wtforms.widgets.core import TextInput
from wtforms.validators import Length,EqualTo,DataRequired,Email
from flask_wtf.file import FileAllowed, FileField
from flask_wtf import FlaskForm


length_validator = "{} must be between {} and {} characters in length."
data_required_validator = "You need to fill in your {} before submitting this form."
equal_to_validator = "{} do not match."


class RegistrationForm(FlaskForm):
    registration_username=StringField(label="Username",id="new_users_username",render_kw={"class":"inptbx rounded-end form-control","placeholder":"username"},validators=[
        DataRequired(message=data_required_validator.format('username')),
        Length(min=2,max=32,message=length_validator.format('Username','2','32'))])
    registration_first_name=StringField(label="Name",id="new_users_first_name",render_kw={"class":"inptbx form-control","placeholder":"first name"},validators=[
        DataRequired(message=data_required_validator.format('first name')),
        Length(min=2,max=32,message=length_validator.format('first name','2','32'))])
    registration_last_name=StringField(label="Last name",id="new_users_last_name",render_kw={"class":"inptbx rounded-end form-control","placeholder":"last name"},validators=[
        DataRequired(message=data_required_validator.format('last name')),
        Length(min=2,max=32,message=length_validator.format('last name','2','32'))])
    registration_password=PasswordField(label="Password",id="new_users_password",render_kw={"class":"inptbx form-control","placeholder":"password"},validators=[
        DataRequired(data_required_validator.format('password')),
        Length(min=6,max=128,message=length_validator.format('password','6','128'))])
    registration_verify_password=PasswordField(label="Confirm password",id="new_users_verify_password",render_kw={"class":"inptbx form-control rounded-end","placeholder":"confirm"},validators=[
        DataRequired(message=data_required_validator.format('password confirmation')),
        EqualTo(fieldname="registration_password",message=equal_to_validator.format("passwords")),
        Length(min=6,max=128,message=length_validator.format('confirmation password','6','128'))])
    registration_email_address=EmailField(label="Email address",id="new_users_email_address",render_kw={"class":"inptbx rounded-end form-control","placeholder":"email"},validators=[
        DataRequired(message=data_required_validator.format('email')),
        Length(min=6,max=64,message=length_validator.format('email','6','64')),
        Email()])
    registration_phone_number=TelField(label="Phone Number",id="new_users_phone_number",render_kw={"class":"inptbx rounded-end form-control","placeholder":"phone"},validators=[
        DataRequired(message=data_required_validator.format('phone number')),
        Length(min=10,max=10,message="Your phone number must be 10 characters in length.")])
    registration_age = DateField(label="Age",id="new_users_age",render_kw={"class":"inptbx datepicker rounded-end form-control"},format="%Y-%m-%d",validators=[
        DataRequired(message='please fill in the date properly.')])
    submit_registration_form = SubmitField(label="Create Account",id='submitRegistrationForm',render_kw={"class":"btn btn-primary col-12 col-sm-8 col-md-6 col-lg-4 col-xl-2 col-xxl-2 my-2"})


class LoginForm(FlaskForm):
    login_username = StringField(label="Username:",id="get_user_username",render_kw={"class":"inptbx rounded-end form-control bg-dark","placeholder":"username","data-bs-theme":'dark'},validators=[
        DataRequired(message=data_required_validator.format('username'))])
    login_password = PasswordField(label="Password:",id="get_user_password",render_kw={"class":"inptbx form-control rounded-end bg-dark","placeholder":"password","data-bs-theme":'dark'},validators=[
        DataRequired(message=data_required_validator.format('password'))])
    login_remember_me = BooleanField(label="Remember me",render_kw={"class":"my-3 ms-2"})
    submit_login_form = SubmitField(label="Sign in",id='submitLoginForm',render_kw={"class":"btn btn-primary col-12 col-sm-8 col-md-6 col-lg-4 col-xl-2 col-xxl-1 my-2"})


class DeleteAccountForm(FlaskForm):
    delete_username = StringField(label='Delete Account',render_kw={'class':'mt-1 rounded p-2',"placeholder":'username',"data-bs-theme":'dark'},validators=[
        DataRequired(message="Enter your username to delete your account")])
    submit_delete_account_form = SubmitField(label="Delete Account",id='confirmDeletingAccount_id',render_kw={"class":"btn btn-danger"})


class EditAccountForm(FlaskForm):
    edit_first_name=StringField(label="First Name", id="edit_first_name",render_kw={"class":"form-control",'placeholder':"first name","data-bs-theme":'dark'},validators=[
        DataRequired(message=data_required_validator.format('first name')),
        Length(min=2,max=32,message=length_validator.format('first name','2','32'))])
    edit_last_name=StringField(label="Last name", id="edit_last_name",render_kw={"class":"form-control rounded-end",'placeholder':"last name","data-bs-theme":'dark'},validators=[
        DataRequired(message=data_required_validator.format('last name')),
        Length(min=2,max=32,message=length_validator.format('last name','2','32'))])
    edit_email_address=EmailField(label="Email address",id="edit_email_address",render_kw={"class":"form-control rounded-end",'placeholder':"email","data-bs-theme":'dark'},validators=[
        DataRequired(message=data_required_validator.format('email')),
        Length(min=6,max=64,message=length_validator.format('email','6','64')),
        Email()])
    edit_phone_number=StringField(label="Phone Number",id="edit_phone_number",render_kw={"class":"form-control rounded-end",'placeholder':"phone","data-bs-theme":'dark'},validators=[
        DataRequired(message=data_required_validator.format('phone number')),
        Length(min=10,max=10,message="Your phone number must be 10 characters in length.")])
    submit_edit_account_form = SubmitField(label="Save Changes",id='SavedChangesConfirmed_id',render_kw={"class":"btn btn-primary"})


class ResetPasswordForm(FlaskForm):
    reset_old_password = PasswordField(label="Old Password:",id="users_old_password",render_kw={"class":"form-control rounded-end",'placeholder':"old","data-bs-theme":'dark'},validators=[
        DataRequired(data_required_validator.format('old password'))])
    reset_new_password = PasswordField(label="New Password:",id="users_password",render_kw={"class":"form-control rounded-end",'placeholder':"new","data-bs-theme":'dark'},validators=[
        DataRequired(data_required_validator.format('new password')),
        Length(min=6,max=128,message=length_validator.format('new password','6','128'))])
    reset_confirm_new_password = PasswordField(label="Confirm Password:",id="users_confirm_new_password",render_kw={"class":"form-control rounded-end",'placeholder':"confirm","data-bs-theme":'dark'},validators=[
        DataRequired(message=data_required_validator.format('password confirmation')),
        EqualTo(fieldname="reset_new_password",message=equal_to_validator.format("passwords")),
        Length(min=6,max=128,message=length_validator.format('confirm password','6','128'))])
    submit_reset_password_form = SubmitField(label="Reset",id='confirmResetingYourPassword_id',render_kw={"class":"btn btn-warning"})


class ProfilePictureForm(FlaskForm):
    selected_image = FileField(label="Select Image", render_kw={"style":"background:#6B6B6B;","class":"btn mt-2 btn-dark col-12","data-bs-theme":'dark'},validators=[
        DataRequired(message='Please enter select a valid image format before submitting your form.'),
        FileAllowed(["jpg","png","jpeg","webp"])])
    selected_image_file_path = StringField(label="Image Path",render_kw={"class":"col-12 mb-2","readonly":True,"data-bs-theme":'dark'},id='image_file_path',validators=[
        DataRequired(message='Please enter a valid file path to a valid image format before submitting your form.'),])
    submit_profile_picture_form = SubmitField(label="Save",id='image_form_id',render_kw={"class":"btn btn-primary",'disabled':True})
