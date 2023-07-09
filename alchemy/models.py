from sqlalchemy import Column,Integer,String,DateTime,func,Index,UniqueConstraint,text,CheckConstraint
from sqlalchemy.orm import relationship,Mapped,declarative_base,mapped_column
from alchemy import engine,bcrypt,login_manager
from flask_login import UserMixin
from sqlalchemy import select


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

    @classmethod
    def _update_state(cls,session):
        count = session.scalar(session.query(func.count(cls.id)))
        engine.execute(text(f"ALTER TABLE {cls.__tablename__} AUTO_INCREMENT = {str(count)}"))

class Account(Signin,MyBase):
    __tablename__ = 'account_list'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)
    password_hash = Column(String(60), nullable=False)
    creation_date = Column(DateTime, nullable=False, default=func.now())

    email_address: Mapped['Email'] = relationship('Email', uselist=False, backref='user_account', primaryjoin='Account.id==foreign(Email.id)')
    phone_number: Mapped['Phone'] = relationship('Phone', uselist=False, backref='user_account', primaryjoin='Account.id==foreign(Phone.id)')
    balance: Mapped['Wallet'] = relationship('Wallet', uselist=False, backref='user_account', primaryjoin='Account.id==foreign(Wallet.id)')
    name: Mapped['Name'] = relationship('Name', uselist=False, backref='user_account', primaryjoin='Account.id==foreign(Name.id)')
    item: Mapped['Item'] = relationship('Item', uselist=True, backref='user_account', primaryjoin='Account.id==foreign(Item.owner)')

    __table_args__ = (UniqueConstraint(username),Index('ix_username_password',username,password_hash))

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)

    @classmethod
    def unique_username(cls,session,form):
        return bool(session.execute(select(cls.username).where(cls.username == form.username.data)).scalar() != None)

    def password_match(form):
        return bool(form.password.data != form.verify_password.data)

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, password={self.password}, creation_date={self.creation_date})"


class Name(MyBase):
    __tablename__ = 'name_list'

    id: Mapped[int] = Column(Integer, primary_key=True, nullable=True)
    first_name: Mapped[str] = Column(String(32), nullable=False)
    last_name: Mapped[str] = Column(String(32), nullable=False)

    __table_args__ = (Index('ix_fullname',first_name,last_name),)

    def __repr__(self) -> str:
        return f"Name(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"


class Email(MyBase):
    __tablename__ = 'email_list'

    id: Mapped[int] = Column(Integer, primary_key=True, nullable=True)
    email_address: Mapped[str] = Column(String(64), nullable=False)

    __table_args__ = (UniqueConstraint(email_address),)

    @classmethod
    def unique_email(cls,session,form):
        return bool(session.execute(select(Email.email_address).where(Email.email_address == form.email_address.data)).scalar() != None)

    def __repr__(self) -> str:
        return f"Email(id={self.id}, email_address={self.email_address})"


class Phone(MyBase):
    __tablename__ = 'phone_list'

    id: Mapped[int] = Column(Integer, primary_key=True, nullable=True)
    phone_number: Mapped[str] = Column(String(20), nullable=False)

    __table_args__ = (UniqueConstraint(phone_number),)

    @classmethod
    def unique_phone(cls,session,form):
        return bool(session.execute(select(Phone.phone_number).where(Phone.phone_number == form.phone_number.data)).scalar() != None)

    def __repr__(self) -> str:
        return f"Phone(id={self.id}, phone_number={self.phone_number})"


class Item(MyBase):
    __tablename__ = 'item_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(length=30), nullable=False)
    price: Mapped[float] = Column(Integer, nullable=False)
    barcode: Mapped[int] = Column(String(length=12), nullable=False)
    description: Mapped[str] = Column(String(2048), nullable=True)
    owner: Mapped['int'] = Column(Integer, nullable=True, default=None)

    __table_args__ = (CheckConstraint('char_length(barcode) = 12', name='barcode_min_length'),)

    def __repr__(self) -> str:
        return f"Item(id={self.id}, name={self.name} price={self.price}, barcode={self.barcode}, owner={self.owner})"

class Wallet(MyBase):
    __tablename__ = 'wallet_list'
    id: Mapped[int] = Column(Integer, primary_key=True, nullable=True)
    balance: Mapped[int] = Column(Integer, nullable=False, default=1000)

    def __repr__(self) -> str:
        return f"Wallet(id={self.id}, balance={self.balance}"



Base.metadata.create_all(bind=engine)
#Base.metadata.drop_all(bind=engine)
# INSERT INTO item_list (name, price, barcode, description)
# VALUES
# ('Laptop', 999.99, '123456789012', 'A portable computer with a 15-inch screen and 8 GB of RAM.'),
# ('Book', 19.99, '987654321098', 'A hardcover novel by a famous author.'),
# ('Shoes', 49.99, '456789123456', 'A pair of sneakers with a comfortable fit and a stylish design.'),
# ('Watch', 199.99, '789123456789', 'A smartwatch that can track your fitness and notifications.'),
# ('Headphones', 59.99, '321654987321', 'A wireless headphones with noise cancellation and high-quality sound.'),
# ('Camera', 299.99, '654321987654', 'A digital camera with a 20-megapixel sensor and a zoom lens.'),
# ('Bag', 39.99, '147258369147', 'A backpack with multiple pockets and a durable material.'),
# ('Guitar', 149.99, '258369147258', 'An acoustic guitar with a wooden body and steel strings.'),
# ('Game', 59.99, '369147258369', 'A video game for a popular console with an immersive storyline and graphics.'),
# ('Phone', 699.99, '741852963741', 'A smartphone with a large screen and a fast processor.'),
# ('Jacket', 79.99, '852963741852', 'A leather jacket with a zipper and a collar.'),
# ('Sunglasses', 29.99, '963741852963', 'A pair of sunglasses with UV protection and a trendy shape.'),
# ('Bike', 199.99, '159357159357', 'A mountain bike with a sturdy frame and a suspension system.'),
# ('Coffee Maker', 49.99, '357159357159', 'A coffee maker that can brew up to 12 cups of coffee at a time.'),
# ('Speaker', 69.99, '951753951753', 'A Bluetooth speaker that can play music from your devices and has a long battery life.'),
# ('Keyboard', 29.99, '753951753951', 'A wireless keyboard that can connect to your computer or tablet and has a slim design.');
