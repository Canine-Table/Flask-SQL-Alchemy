from alchemy.accounts.forms import RegistrationForm,ResetPasswordForm,LoginForm,DeleteAccountForm,EditAccountForm,ResetPasswordForm,ProfilePictureForm
from flask import render_template,request,url_for,flash,get_flashed_messages,redirect
from flask_login import login_user,current_user,logout_user,login_required
from alchemy.models import Account,Phone,Email,Name,Signin,Item,Wallet
from alchemy.main.exceptions import QueryException
from alchemy.accounts.utils import crop_to_square
from alchemy.main.jinja2env import jinja2_env
from flask import Blueprint
from alchemy import Session
from io import BytesIO
from PIL import Image
import base64


account = Blueprint('account',__name__)


@account.route('/register', methods=['GET','POST'])
def register_page():
    form = RegistrationForm()
    if request.method == "POST":
        with Session() as session:
            try:
                QueryException.clear_errors()
                if Account.unique_username(session,form):
                    QueryException.add_error_message(f"The username {form.username.data} is already in use.")

                if Email.unique_email(session,form):
                    QueryException.add_error_message(f"The email {form.email_address.data} is already in use.")

                if Phone.unique_phone(session,form):
                    QueryException.add_error_message(f"The phone number {form.phone_number.data} is already in use.")

                if Account.password_match(form):
                    QueryException.add_error_message(f"The passwords do not match.")

                if QueryException.error_count():
                    QueryException.show_error_messages()

            except QueryException:
                pass
            except Exception as e:
                flash(f"{e}", category='danger')
            else:
                account_to_create = Account(username=form.username.data,password=form.password.data)
                phone_to_create = Phone(phone_number=form.phone_number.data,user_account=account_to_create)
                email_to_create = Email(email_address=form.email_address.data,user_account=account_to_create)
                name_to_create = Name(first_name=(form.first_name.data).title(),last_name=(form.last_name.data).title(),user_account=account_to_create)
                balance_to_create = Wallet(user_account=account_to_create)
                session.add_all([account_to_create,phone_to_create,email_to_create,name_to_create,balance_to_create])
                session.commit()
                flash(f"{form.username.data} was successfully created.",category='success')
                get_user = Signin.get_session(session).load_user(account_to_create.id)
                login_user(get_user,remember=False)
                return redirect(url_for('market.market_page', username=current_user.username))

    return render_template('register.html',form=form,env=jinja2_env)


@account.route('/login', methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if request.method == "POST":
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
                flash(f"{e}", category='danger')

    return render_template('login.html',
        messages=get_flashed_messages(),
        form=form,env=jinja2_env,
        current_user=current_user)


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
            if delete_form.submit.data and request.form['form_name'] =='delete_form':
                if (delete_form.username.data).strip() == current_user.username:
                        session.query(Item).filter_by(owner=current_user.id).update({Item.owner: None})
                        for delete_row in [Account,Email,Name,Phone,Wallet]:
                            session.query(delete_row).filter_by(id=current_user.id).delete()
                            delete_row._update_state(session)
                        session.commit()
                        return redirect(url_for('account.logout_page'))
                else:
                    flash(f"input box did not match your username, account was not deleted", category='warning')

            if edit_form.submit.data and request.form['form_name'] == 'edit_form':
                try:
                    QueryException.clear_errors()

                    if Email.unique_email(session,edit_form) and edit_form.email_address.data != current_user.email_address.email_address:
                        QueryException.add_error_message(f"The email {edit_form.email_address.data} is already in use.")

                    if Phone.unique_phone(session,edit_form) and edit_form.phone_number.data != current_user.phone_number.phone_number:
                        QueryException.add_error_message(f"The phone number {edit_form.phone_number.data} is already in use.")

                    if QueryException.error_count():
                        QueryException.show_error_messages()

                except QueryException:
                    pass
                except Exception as e:
                    flash(f"{e}", category='danger')
                else:
                    message_template = "You have successfully updated your {} from {} to {}!"
                    if edit_form.first_name.data != current_user.name.first_name:
                        session.query(Name).filter_by(id=current_user.id).update({Name.first_name: (edit_form.first_name.data).title()})
                        Name._update_timestamp(session)
                        flash(message_template.format('first name',current_user.name.first_name,edit_form.first_name.data), category='success')
                        current_user.name.first_name = edit_form.first_name.data

                    if edit_form.last_name.data != current_user.name.last_name:
                        session.query(Name).filter_by(id=current_user.id).update({Name.last_name: (edit_form.last_name.data).title()})
                        Name._update_timestamp(session)
                        flash(message_template.format('last name',current_user.name.last_name,edit_form.last_name.data), category='success')
                        current_user.name.last_name = edit_form.last_name.data

                    if edit_form.email_address.data != current_user.email_address.email_address:
                        session.query(Email).filter_by(id=current_user.id).update({Email.email_address: edit_form.email_address.data})
                        Email._update_timestamp(session)
                        flash(message_template.format('email address',current_user.email_address.email_address,edit_form.email_address.data), category='success')
                        current_user.email_address.email_address = edit_form.email_address.data

                    if edit_form.phone_number.data != current_user.phone_number.phone_number:
                        session.query(Phone).filter_by(id=current_user.id).update({Phone.phone_number: edit_form.phone_number.data})
                        Phone._update_timestamp(session)
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
                    flash(f"{e}", category='danger')
                else:
                    current_user.password = password_form.new_password.data
                    session.query(Account).filter_by(id=current_user.id).update({Account.password_hash:current_user.password_hash})
                    Account._update_timestamp(session)
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
                            session.query(Account).filter_by(id=current_user.id).update({Account.profile_picture: str(base64_image)})
                            Account._update_timestamp(session)
                            session.commit()
                except Exception as e:
                    flash(f"{e}", category='danger')


    return render_template('settings.html',user=current_user,
        delete_form=delete_form,
        edit_form=edit_form,
        password_form=password_form,
        image_form=image_form,
        env=jinja2_env)
