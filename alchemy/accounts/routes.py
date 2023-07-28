from alchemy.accounts.forms import RegistrationForm,ResetPasswordForm,LoginForm,DeleteAccountForm,EditAccountForm,ResetPasswordForm,ProfilePictureForm
from flask import render_template,request,url_for,flash,get_flashed_messages,redirect
from flask_login import login_user,current_user,logout_user,login_required
from alchemy.models import Account,Phone,Email,Name,Signin,Item,Wallet
from alchemy.utils import error_log,error_string,get_date_string
from alchemy.main.exceptions import QueryException
from alchemy.accounts.utils import crop_to_square
from flask import Blueprint
from alchemy import Session
from io import BytesIO
from PIL import Image
import base64
import re


account = Blueprint('account',__name__,template_folder='templates',static_folder='static',static_url_path='/accounts/static')


@account.route('/register', methods=['GET','POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        with Session() as session:
            try:
                QueryException.clear_errors()
                year_entered = int(str(form.age.data).split('-')[0])
                current_year = int(get_date_string(date_format='get_year'))
                if Account.unique_username(session,form):
                    QueryException.add_error_message(f"The username {form.username.data} is already in use.")

                if Email.unique_email(session,form):
                    QueryException.add_error_message(f"The email {form.email_address.data} is already in use.")

                if not re.match('^[0-9]{3}-[0-9]{3}-[0-9]{4}$',form.phone_number.data):
                    QueryException.add_error_message(f"The phone number you entered is invalid.")
                elif Phone.unique_phone(session,form):
                    QueryException.add_error_message(f"The phone number {form.phone_number.data} is already in use.")

                if Account.password_match(form):
                    QueryException.add_error_message(f"The passwords do not match.")

                if current_year - year_entered < 0:
                    QueryException.add_error_message(f"Come back when your born.")
                elif  current_year - year_entered < 18:
                    QueryException.add_error_message(f"Your must be 18 or older to signup.")
                elif current_year - year_entered >= 135:
                    QueryException.add_error_message(f"You must be in the land of the living to signup.")

                if QueryException.error_count():
                    QueryException.show_error_messages()

            except QueryException:
                pass
            except Exception as e:
                if form.age.data == None:
                    flash(f"The date you entered is invalid.",category="danger")
                else:
                    flash(f"{type(e).__name__}: {error_string(error=e)}",category="danger")
                error_log(error=e)
            else:

                new_user = {
                    'username':form.username.data,
                    'password':form.password.data,
                    'first_name':(form.first_name.data).title(),
                    'last_name':(form.last_name.data).title(),
                    'email_address':form.email_address.data,
                    'phone_number':form.phone_number.data,
                    'age':form.age.data,
                    'login':True
                }

                login_user(Signin.get_session(session).load_user(Account.create_account(**new_user)),remember=True)
                flash(f"{form.username.data} was successfully created.",category='success')
                return redirect(url_for('market.market_page', username=current_user.username))

    return render_template('register.html',form=form)


@account.route('/login', methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        with Session() as session:
            try:
                QueryException.clear_errors()
                attempted_user = session.query(Account).filter_by(username=form.username.data).first()
                if attempted_user and attempted_user.check_password_correction(form.password.data):
                    flash(f'Welcome back {(" ".join([attempted_user.name.first_name,attempted_user.name.last_name])).title()} (\'{form.username.data}\')', category='success')
                    get_user = Signin.get_session(session).load_user(attempted_user.id)
                    login_user(get_user,remember=form.remember_me.data)

                    return redirect(url_for('market.market_page', username=attempted_user.username))
                else:
                    QueryException.add_error_message(f"The username or password does not match.")
                if QueryException.error_count():
                    QueryException.show_error_messages()
            except QueryException:
                pass
            except Exception as e:
                flash(f"{type(e).__name__}: {error_string(error=e)}",category="danger")
                error_log(error=e)

    return render_template('login.html',messages=get_flashed_messages(),form=form)


@account.route('/logout')
def logout_page():
    flash("you logged out of your account", category='primary')
    logout_user()
    return redirect( url_for('main.home_page'))


@account.route('/<username>/settings', methods=['GET','POST'])
@login_required
def settings_page(username):
    delete_form=DeleteAccountForm()
    edit_form=EditAccountForm()
    password_form=ResetPasswordForm()
    image_form=ProfilePictureForm()

    edit_form.first_name.data = edit_form.first_name.data or current_user.name.first_name
    edit_form.last_name.data = edit_form.last_name.data or current_user.name.last_name
    edit_form.email_address.data = edit_form.email_address.data or current_user.email_address.email_address
    edit_form.phone_number.data = edit_form.phone_number.data or current_user.phone_number.phone_number

    if request.method == 'POST':
        with Session() as session:
            user = session.query(Account).get(current_user.id)
            if delete_form.submit.data and request.form['form_name'] =='delete_form':
                if (delete_form.username.data).strip() == current_user.username:
                    session.delete(session.query(Account).get(current_user.id))
                    session.commit()
                    return redirect(url_for('account.logout_page'))
                else:
                    flash(f"input box did not match your username, account was not deleted", category='warning')

            if edit_form.submit.data and request.form['form_name'] == 'edit_form':
                try:
                    QueryException.clear_errors()

                    if Email.unique_email(session,edit_form) and edit_form.email_address.data != current_user.email_address.email_address:
                        QueryException.add_error_message(f"The email {edit_form.email_address.data} is already in use.")

                    if not re.match('^[0-9]{3}-[0-9]{3}-[0-9]{4}$',edit_form.phone_number.data):
                        QueryException.add_error_message(f"The phone number you entered is invalid.")
                    elif Phone.unique_phone(session,edit_form) and edit_form.phone_number.data != current_user.phone_number.phone_number:
                        QueryException.add_error_message(f"The phone number {edit_form.phone_number.data} is already in use.")

                    if QueryException.error_count():
                        QueryException.show_error_messages()

                except QueryException:
                    pass
                except Exception as e:
                    flash(f"{type(e).__name__}: {error_string(error=e)}",category="danger")
                    error_log(error=e)
                else:
                    message_template = "You have successfully updated your {} from {} to {}!"
                    name = session.query(Name).get(current_user.id)
                    if edit_form.first_name.data != current_user.name.first_name:
                        name.first_name = (edit_form.first_name.data).title()
                        flash(message_template.format('first name',current_user.name.first_name,edit_form.first_name.data), category='success')
                        current_user.name.first_name = edit_form.first_name.data

                    if edit_form.last_name.data != current_user.name.last_name:
                        name.last_name = (edit_form.last_name.data).title()
                        flash(message_template.format('last name',current_user.name.last_name,edit_form.last_name.data), category='success')
                        current_user.name.last_name = edit_form.last_name.data

                    if edit_form.email_address.data != current_user.email_address.email_address:
                        email = session.query(Email).get(current_user.id)
                        email.email_address = edit_form.email_address.data
                        flash(message_template.format('email address',current_user.email_address.email_address,edit_form.email_address.data), category='success')
                        current_user.email_address.email_address = edit_form.email_address.data

                    if edit_form.phone_number.data != current_user.phone_number.phone_number:
                        phone = session.query(Phone).get(current_user.id)
                        phone.phone_number = edit_form.phone_number.data
                        flash(message_template.format('phone number',current_user.phone_number.phone_number,edit_form.phone_number.data), category='success')
                        current_user.phone_number.phone_number = edit_form.phone_number.data
                    session.commit()

            if password_form.submit.data and request.form['form_name'] == 'password_form':
                try:
                    QueryException.clear_errors()
                    if not current_user.check_password_correction(password_form.old_password.data):
                        QueryException.add_error_message(f"the password you entered is incorrect")

                    if password_form.new_password.data != password_form.confirm_new_password.data:
                        QueryException.add_error_message("the new passwords do not match")

                    if password_form.old_password.data == password_form.new_password.data or password_form.old_password.data == password_form.confirm_new_password.data:
                        QueryException.add_error_message("the new password must be different from the old password")

                    if QueryException.error_count():
                        QueryException.show_error_messages()

                except QueryException:
                    pass
                except Exception as e:
                    flash(f"{type(e).__name__}: {error_string(error=e)}",category="danger")
                    error_log(error=e)
                else:
                    current_user.password = password_form.new_password.data
                    user.password_hash = current_user.password_hash
                    session.commit()
                    flash(f"Your password has been updated", category='success')

            if image_form.submit.data and request.form['form_name'] == 'image_form':
                try:
                    ctype = image_form.selected_image.data.content_type
                    if ctype not in ['image/jpeg','image/pjpeg','image/png','image/tiff','image/x-tiff','image/jpg','image/svg+xml','image/webp','image/bmp']:
                        flash(f'{ctype} is not a valid image type',category='danger')
                    else:
                        with Image.open(image_form.selected_image.data) as image:
                            square_image = crop_to_square(image)
                            output_size = (48,48)
                            buffer = BytesIO()
                            square_image.thumbnail(output_size)
                            square_image.save(buffer, format=ctype[6::].upper())
                            base64_image = f"data:{ctype};base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
                            user.profile_picture = str(base64_image)
                            session.commit()
                            current_user.profile_picture = session.query(Account.profile_picture).filter_by(id=current_user.id).scalar()
                except Exception as e:
                    flash(f"{type(e).__name__}: {error_string(error=e)}",category="danger")
                    error_log(error=e)

    return render_template('settings.html',user=current_user,delete_form=delete_form,edit_form=edit_form,password_form=password_form,image_form=image_form)
