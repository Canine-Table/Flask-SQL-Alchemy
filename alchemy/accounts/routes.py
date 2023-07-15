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
                        flash(message_template.format('first name',current_user.name.first_name,edit_form.first_name.data), category='success')
                        current_user.name.first_name = edit_form.first_name.data

                    if edit_form.last_name.data != current_user.name.last_name:
                        session.query(Name).filter_by(id=current_user.id).update({Name.last_name: (edit_form.last_name.data).title()})
                        flash(message_template.format('last name',current_user.name.last_name,edit_form.last_name.data), category='success')
                        current_user.name.last_name = edit_form.last_name.data

                    if edit_form.email_address.data != current_user.email_address.email_address:
                        session.query(Email).filter_by(id=current_user.id).update({Email.email_address: edit_form.email_address.data})
                        flash(message_template.format('email address',current_user.email_address.email_address,edit_form.email_address.data), category='success')
                        current_user.email_address.email_address = edit_form.email_address.data

                    if edit_form.phone_number.data != current_user.phone_number.phone_number:
                        session.query(Phone).filter_by(id=current_user.id).update({Phone.phone_number: edit_form.phone_number.data})
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

                    if QueryException.error_count():
                        QueryException.show_error_messages()

                except QueryException:
                    pass
                except Exception as e:
                    flash(f"{e}", category='danger')
                else:
                    current_user.password = password_form.new_password.data
                    session.query(Account).filter_by(id=current_user.id).update({Account.password_hash:current_user.password_hash})
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
                            session.commit()
                            current_user.profile_picture = session.query(Account.profile_picture).filter_by(id=current_user.id).scalar() or 'data:image/webp;base64,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'
                except Exception as e:
                    flash(f"{e}", category='danger')


    return render_template('settings.html',user=current_user,
        delete_form=delete_form,
        edit_form=edit_form,
        password_form=password_form,
        image_form=image_form,
        env=jinja2_env)
