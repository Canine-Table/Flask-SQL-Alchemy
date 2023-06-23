from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, ForeignKeyConstraint, select, DateTime, func

metadata = MetaData()
user_table = Table(
    'users_list', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(80), nullable=False, unique=True))

email_table = Table(
    'emails_list', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('email', String(80), nullable=False, unique=True))


account_table = Table(
    'account_list', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
	Column('username', String(32), nullable=False, default='johndoe', unique=True),
	Column('first_name', String(64), nullable=False, default='John', unique=True),
	Column('last_name', String(64), nullable=False, default='Doe', unique=True),
	Column('email_address', String(64), nullable=False, default='johndoe@gmail.com', unique=True),
	Column('phone_number', String(20), nullable=False, default='123-456-7890', unique=True),

)

name_table = Table('name_list', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
	Column('first_name', String(64), nullable=False, default='John', unique=True),
	Column('last_name', String(64), nullable=False, default='Doe', unique=True))


username_table = Table('username_list', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
	Column('username', String(32), nullable=False, default='johndoe', unique=True),
    Column('user_id', Integer, ForeignKey('name_list.id'), nullable=False))


address_table = Table('address_list', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
	Column('email_address', String(64), nullable=False, default='johndoe@gmail.com', unique=True),
    Column('user_id', Integer, ForeignKey('name_list.id'), nullable=False))


phone_table = Table('phone_list', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('phone_number', String(20), nullable=False, default='123-456-7890', unique=True),
    Column('user_id', Integer, ForeignKey('name_list.id'), nullable=False))
