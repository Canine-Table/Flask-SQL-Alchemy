from sqlalchemy import Column,Integer,String,DateTime,Date,func,Index,UniqueConstraint,text,CheckConstraint,event,DECIMAL
from sqlalchemy.orm import relationship,Mapped,declarative_base,Mapper
from alchemy.accounts.utils import after_create_account_table
from alchemy.market.utils import after_create_item_table
from alchemy.utilities.database import Session,engine
from alchemy import bcrypt,login_manager
from flask_login import UserMixin
from decimal import Decimal
import secrets


Base = declarative_base()


class Signin(UserMixin):

    @classmethod
    def get_session(cls, session):
        cls.session = session
        return cls

    @login_manager.user_loader
    def load_user(user_id):
        return Signin.session.query(Account).get(int(user_id)) or None


class MyBase(Base):
    __abstract__ = True
    __table_args__ = ({'mysql_auto_increment': '1'},)


class Account(Signin,MyBase):
    __tablename__ = 'account_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(32), nullable=False)
    password_hash: Mapped[str] = Column(String(60), nullable=False)
    profile_picture: Mapped[str] = Column(String(8192), nullable=False, default='data:image/webp;base64,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')
    age: Mapped[Date] = Column(Date, nullable=False)
    creation_date: Mapped[DateTime] = Column(DateTime, nullable=False, default=func.now())
    last_updated: Mapped[DateTime] = Column(DateTime)

    __table_args__ = (UniqueConstraint(username),Index('ix_username_password',username,password_hash))

    email_address: Mapped['Email'] = relationship('Email', backref='user_account', primaryjoin='Account.id==foreign(Email.id)', cascade="all, delete-orphan")
    phone_number: Mapped['Phone'] = relationship('Phone', backref='user_account', primaryjoin='Account.id==foreign(Phone.id)', cascade="all, delete-orphan")
    name: Mapped['Name'] = relationship('Name', backref='user_account', primaryjoin='Account.id==foreign(Name.id)', cascade="all, delete-orphan")
    balance: Mapped['Wallet'] = relationship('Wallet', backref='user_account', primaryjoin='Account.id==foreign(Wallet.id)', cascade="all, delete-orphan")
    groups: Mapped['Group'] = relationship('Group', backref='user_account', primaryjoin='Account.id==foreign(Group.uid)', cascade="all, delete-orphan", lazy=True,)
    purchases: Mapped['Purchase'] = relationship('Purchase', backref='user_account', primaryjoin='Account.id==foreign(Purchase.owner)', cascade="all, delete-orphan", lazy=True)
    comments: Mapped['Comment'] = relationship('Comment', backref='user_account', primaryjoin='Account.id==foreign(Comment.written_by)', cascade="all, delete-orphan", lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)

    @classmethod
    def unique_username(cls,session,username) -> bool:
        return bool(session.query(cls.username).filter_by(username = username).scalar() != None)

    def password_match(password_one,password_two) -> bool:
        return bool(password_one != password_two)

    def create_account(**kwargs):
        with Session() as session:
            account_to_create = Account(username=kwargs['username'],password=kwargs['password'],age=kwargs['age'])
            name_to_create = Name(first_name=(kwargs['first_name']).title(),last_name=(kwargs['last_name']).title(),user_account=account_to_create)
            email_to_create = Email(email_address=kwargs['email_address'],user_account=account_to_create)
            phone_to_create = Phone(phone_number=kwargs['phone_number'],user_account=account_to_create)
            balance_to_create = Wallet(balance=kwargs.get('balance',1000),user_account=account_to_create)
            session.add_all([account_to_create,phone_to_create,email_to_create,name_to_create,balance_to_create])
            session.commit()
            if not kwargs.get('uid',False):
                with Session() as session:
                    kwargs['uid'] = session.query(Account.id).filter_by(username=kwargs['username']).scalar()
            group_to_create = Group(uid=kwargs['uid'],user_group=kwargs.get('group','standard_user'),privilages=kwargs.get('privilages',744))
            session.add(group_to_create)
            session.commit()
            if kwargs.get('login',False):
                return kwargs['uid']

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, password={self.password}, creation_date={self.creation_date})"


class Group(MyBase):
    __tablename__ = 'group_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    uid: Mapped[int] = Column(Integer, nullable=False)
    user_group: Mapped[str] = Column(String(16), nullable=False, default='standard_user')
    privilages: Mapped[int] = Column(Integer, nullable=False, default=744)

    __table_args__ = (CheckConstraint('FORMAT(privilages, "000") BETWEEN 0 AND 777', name='user_privilages'),)

    def __repr__(self) -> str:
        return f"Group(id={self.id}, uid={self.uid}, user_group={self.user_group}, privilages={self.privilages})"



class Name(MyBase):
    __tablename__ = 'name_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    first_name: Mapped[str] = Column(String(32), nullable=False)
    last_name: Mapped[str] = Column(String(32), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime)

    __table_args__ = (Index('ix_fullname',first_name,last_name),)

    def __repr__(self) -> str:
        return f"Name(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"


class Email(MyBase):
    __tablename__ = 'email_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    email_address: Mapped[str] = Column(String(64), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime)

    __table_args__ = (UniqueConstraint(email_address),)

    @classmethod
    def unique_email(cls,session,email) -> bool:
        return bool(session.query(Email.email_address).filter_by(email_address = email).scalar() != None)

    def __repr__(self) -> str:
        return f"Email(id={self.id}, email_address={self.email_address})"


class Phone(MyBase):
    __tablename__ = 'phone_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    phone_number: Mapped[str] = Column(String(10), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime)

    __table_args__ = (UniqueConstraint(phone_number),CheckConstraint('char_length(phone_number) = 10', name='phone_number_length'))

    @classmethod
    def unique_phone(cls,session,phone) -> bool:
        return bool(session.query(Phone.phone_number).filter_by(phone_number = phone).scalar() != None)

    def __repr__(self) -> str:
        return f"Phone(id={self.id}, phone_number={self.phone_number})"


class Item(MyBase):
    __tablename__ = 'item_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(length=32), nullable=False)
    price: Mapped[Decimal] = Column(DECIMAL(precision=10, scale=2), nullable=False)
    barcode: Mapped[str] = Column(String(length=128), nullable=False)
    description: Mapped[str] = Column(String(2048), nullable=False)
    stock: Mapped[int] = Column(Integer, nullable=False, default=1)
    date_added: Mapped[DateTime] = Column(DateTime, nullable=False, default=func.now())
    last_updated: Mapped[DateTime] = Column(DateTime)

    __table_args__ = (UniqueConstraint(barcode),)

    comments: Mapped['Comment'] = relationship('Comment', uselist=True, backref='item_comments', primaryjoin='Item.barcode==foreign(Comment.barcode)', lazy=True)
    purchases: Mapped['Purchase'] = relationship('Purchase', uselist=True, backref='item_purchase', primaryjoin='Item.barcode==foreign(Purchase.barcode)')

    def create_item(**kwargs):
        with Session() as session:
            item = Item(name=kwargs['name'],price=kwargs['price'],barcode=kwargs['barcode'],description=kwargs['description'],stock=kwargs['stock'],date_added=kwargs['date_added'])
            item.barcode = (secrets.token_hex(32)).upper()
            session.add(item)
            session.commit()

    def __repr__(self) -> str:
        return f"Item(id={self.id}, name={self.name} price={self.price}, barcode={self.barcode}, stock={self.stock})"


class Purchase(MyBase):
    __tablename__ = 'purchase_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    count: Mapped[int] = Column(Integer, nullable=False)
    owner: Mapped[int] = Column(Integer, nullable=False)
    barcode: Mapped[str] = Column(String(length=128), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime)
    date_purchased: Mapped[DateTime] = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self) -> str:
        return f"Purchase(id={self.id}, count={self.count}, owner={self.owner}, barcode={self.barcode})"


class Comment(MyBase):
    __tablename__ = 'item_comments_list'
    id: Mapped[int] = Column(Integer, primary_key=True)
    barcode: Mapped[str] = Column(String(length=128), nullable=False)
    written_by: Mapped[str] = Column(String(32), nullable=False)
    title: Mapped[str] =  Column(String(length=128), nullable=False)
    body: Mapped[str] =  Column(String(length=8192), nullable=False)
    rating: Mapped[int] = Column(Integer, nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime)
    creation_date: Mapped[DateTime] = Column(DateTime, nullable=False, default=func.now())

    __table_args__ = (CheckConstraint('rating >= 0 AND rating <= 5', name='check_item_rating'),)

    def __repr__(self) -> str:
        return f"Comment(id={self.id}, owner={self.written_by} title={self.title}, creation_date={self.creation_date})"


class Wallet(MyBase):
    __tablename__ = 'wallet_list'
    id: Mapped[int] = Column(Integer, primary_key=True)
    balance: Mapped[Decimal] = Column(DECIMAL(precision=10, scale=2), nullable=False, default=1000)
    last_updated: Mapped[DateTime] = Column(DateTime)
    last_purchase: Mapped[DateTime] = Column(DateTime)

    def __repr__(self) -> str:
        return f"Wallet(id={self.id}, balance={self.balance}"


def create_account_table(*args,**kwargs):
    for kw in after_create_account_table():
        Account.create_account(**kw)


def create_item_table(*args,**kwargs):
    for kw in after_create_item_table():
        Item.create_item(**kw)


event.listen(Wallet.__table__, 'after_create', create_account_table)
event.listen(Item.__table__, 'after_create', create_item_table)


#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@event.listens_for(Mapper,"after_update")
def update_table(mapper,conn,target):
    if isinstance(target,(Account,Name,Email,Phone,Item,Wallet,Purchase,Comment)):
        conn.execute(target.__table__.update().where(target.__table__.c.id == target.id).values(last_updated=func.now()))


@event.listens_for(Name,'before_delete')
def delete_account(mapper,conn,target):
    with Session() as session:
        purchases = session.query(Purchase).filter_by(owner=target.id)
        for row in purchases:
            item = session.query(Item).filter_by(barcode=row.barcode).one_or_none()
            if item is not None:
                item.stock += row.count
        session.commit()
