from sqlalchemy.orm import relationship,Mapped,declarative_base
from sqlalchemy import Column,Integer,String,DateTime,func,Index,UniqueConstraint,text
from alchemy import engine,bcrypt
from typing import Optional

Base = declarative_base()
class MyBase(Base):
    __abstract__ = True
    __table_args__ = ({'mysql_auto_increment': '1'},)

    @classmethod
    def _update_state(cls,session,engine):
        count = session.scalar(session.query(func.count(cls.id)))
        engine.execute(text(f"ALTER TABLE {cls.__tablename__} AUTO_INCREMENT = {str(count)}"))

class Account(MyBase):
    __tablename__ = 'account_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)
    password_hash = Column(String(60), nullable=False)
    creation_date = Column(DateTime, nullable=False, default=func.now())

    email_address: Mapped['Email'] = relationship('Email', uselist=False, backref='user_account', primaryjoin='Account.id==foreign(Email.id)', cascade='all, delete-orphan')
    phone_number: Mapped['Phone'] = relationship('Phone', uselist=False, backref='user_account', primaryjoin='Account.id==foreign(Phone.id)', cascade='all, delete-orphan')
    name: Mapped['Name'] = relationship('Name', uselist=False, backref='user_account', primaryjoin='Account.id==foreign(Name.id)', cascade='all, delete-orphan')

    __table_args__ = (UniqueConstraint(username),Index('ix_username_password',username,password_hash))

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, password={self.password}, creation_date={self.creation_date})"


class Name(MyBase):
    __tablename__ = 'name_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    first_name: Mapped[str] = Column(String(32), nullable=False)
    last_name: Mapped[str] = Column(String(32), nullable=False)

    __table_args__ = (Index('ix_fullname',first_name,last_name),)

    def __repr__(self) -> str:
        return f"Name(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"


class Email(MyBase):
    __tablename__ = 'email_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    email_address: Mapped[str] = Column(String(64), nullable=False)

    __table_args__ = (UniqueConstraint(email_address),)

    def __repr__(self) -> str:
        return f"Email(id={self.id}, email_address={self.email_address})"


class Phone(MyBase):
    __tablename__ = 'phone_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    phone_number: Mapped[str] = Column(String(20), nullable=False)

    __table_args__ = (UniqueConstraint(phone_number),)


    def __repr__(self) -> str:
        return f"Phone(id={self.id}, phone_number={self.phone_number})"


Base.metadata.create_all(bind=engine)
#Base.metadata.drop_all(bind=engine)
