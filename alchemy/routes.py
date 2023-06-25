from flask import render_template, request, url_for, flash, get_flashed_messages
from alchemy.forms import RegistrationForm,LoginForm
from alchemy import app,db,engine,inspector,bcrypt
from alchemy.models import Account,Phone,Email,Name,MyBase
from sqlalchemy import text, select
from sqlalchemy.orm import Session, sessionmaker,scoped_session
import sqlalchemy
import transaction
import re

Session = scoped_session(sessionmaker(bind=engine))
global_engine = engine

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home_page():
    return render_template('home.html',
        version=sqlalchemy.__version__
    )

@app.route('/register', methods=[ 'GET','POST'])
def register_page():
    form = RegistrationForm()
    if request.method == "POST":
        with Session() as session:
            with transaction.manager:
                try:
                    account_to_create = Account(username=form.username.data,password=form.password.data)
                    phone_to_create = Phone(phone_number=form.phone_number.data,user_account=account_to_create)
                    email_to_create = Email(email_address=form.email_address.data,user_account=account_to_create)
                    name_to_create = Name(first_name=form.first_name.data,last_name=form.last_name.data,user_account=account_to_create)
                    session.add_all([account_to_create,phone_to_create,email_to_create,name_to_create])
                except Exception as e:

                    e = str(e)
                    duplicate_username_iter = len([i for i in re.compile(r"code = AlreadyExists desc = Duplicate entry \\'.*\\' for key \\'account_list.username\\'").finditer(e)])
                    duplicate_phone_iter = len([i for i in re.compile(r"code = AlreadyExists desc = Duplicate entry \\'.*\\' for key \\'phone_list.phone_number\\'").finditer(e)])
                    duplicate_email_iter = len([i for i in re.compile(r"code = AlreadyExists desc = Duplicate entry \\'.*\\' for key \\'email_list.email_address\\'").finditer(e)])
                    if duplicate_username_iter+duplicate_email_iter+duplicate_phone_iter > 0:
                        if duplicate_username_iter > 0:
                            flash(f"The username {form.username.data} already taken.", category='warning')
                        if duplicate_phone_iter > 0:
                            flash(f"The phone number {form.phone_number.data} is already taken.", category='warning')
                        if duplicate_email_iter > 0:
                            flash(f"The email address {form.email_address.data} is already taken.", category='warning')
                    else:
                        flash(f"exception caught! {e}", category='danger')

                    with global_engine.connect() as engine:
                        for subclass in MyBase.__subclasses__():
                            subclass._update_state(session,engine)

    return render_template('register.html',
        form=form
    )

@app.route('/login', methods=[ 'GET','POST'])
def login_page():
    form=LoginForm()
    return render_template('login.html',
        form=form
    )
