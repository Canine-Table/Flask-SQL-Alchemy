from flask import render_template,request,url_for,flash,get_flashed_messages,redirect
from sqlalchemy.orm import Session,sessionmaker,scoped_session
from sqlalchemy.exc import IntegrityError,PendingRollbackError
from alchemy.models import Account,Phone,Email,Name,MyBase
from alchemy.forms import RegistrationForm,LoginForm
from alchemy.exceptions import QueryException
from alchemy import app,engine
from sqlalchemy import select
from re import match
import transaction
import sys

Session = scoped_session(sessionmaker(bind=engine))

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home_page():
    return render_template('home.html')


@app.route('/register', methods=[ 'GET','POST'])
def register_page():
    form = RegistrationForm()
    if request.method == "POST":
        with Session() as session:
            with transaction.manager:
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
                    session.add_all([account_to_create,phone_to_create,email_to_create,name_to_create])
                    session.commit()
                    flash(f"{form.username.data} was successfully created.",category='success')
                    return redirect(url_for('login_page'))

    return render_template('register.html',
        form=form)


@app.route('/login', methods=[ 'GET','POST'])
def login_page():
    form=LoginForm()
    if request.method == "POST":
        with Session() as session:
            with transaction.manager:
                try:
                    QueryException.clear_errors()
                    attempted_user = session.query(Account,Account.id).filter_by(username=form.username.data).first()
                    if attempted_user[0] and attempted_user[0].check_password_correction(form.password.data):
                        fullname = session.query(Name.first_name,Name.last_name).filter_by(id=attempted_user[1]).first()
                        flash(f'Welcome back {(" ".join(fullname)).title()} (\'{form.username.data}\')', category='success')
                    else:
                        QueryException.add_error_message(f"The username or password does not match.")

                    if QueryException.error_count() > 0:
                        QueryException.show_error_messages()
                        raise QueryException
                except QueryException:
                    pass
                except Exception as e:
                    flash(f"{e}", category='danger')

    return render_template('login.html',
    form=form,
    messages=get_flashed_messages())


@app.route('/market', methods=[ 'GET','POST'])
def market_page():
    return render_template('market.html')
