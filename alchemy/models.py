from sqlalchemy import Column,Integer,String,DateTime,func,Index,UniqueConstraint,text,CheckConstraint,event,DDL,DECIMAL
from sqlalchemy.orm import relationship,Mapped,declarative_base,mapped_column
from alchemy import engine,bcrypt,login_manager,Session
from flask_login import UserMixin
from decimal import Decimal


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
        session.execute(text(f"ALTER TABLE {cls.__tablename__} AUTO_INCREMENT = {str(count)}"))

    @classmethod
    def _update_timestamp(cls,session):
        session.query(cls).update({cls.last_updated: func.now()})

class Account(Signin,MyBase):
    __tablename__ = 'account_list'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(32), nullable=False)
    password_hash: Mapped[str] = Column(String(60), nullable=False)
    profile_picture: Mapped[str] = Column(String(8192), nullable=False, default='data:image/webp;base64,UklGRg4MAABXRUJQVlA4WAoAAAAgAAAALwAALwAASUNDUMgBAAAAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADZWUDhMIAoAAC8vwAsADXUhov8BT7dtm5aFbfuKWp9rI+Lwsm2mnDJStpm6rr9g+7pSZtK27ZxtG4GNiNhrjlbi2nEu35IkWZIk2RayqEXd6/8/sqrv13B3FfYtSZIlSZJtIbNZ3av+/1erusOEg4HbRor2GIZn233Db77+BwAAkM5kKydAUAKAR6MzEQARINiZiAIKHXuqQ0jSsdOjsgMAgNNPZ+6CSToKIKbgU0kgiEAAigRSMYilS5KIGHTAhLPkFAQ78217DacebOUQwOLUIBAknUkQBALEklGtH5gKCbQOa/kwuOKGIoAa9k7DP3sDWAgQSAJEmoFAC0uALmZQJulMQvqZYhQZHSlgBABhImCSDiAIhmAxJYIBFocIYBQJneEpO8gupEsPIWJ6IB0OsPTTS2gRSBmt26oPMcCUEANBIhJCRFKx1k9RgZHgRAC/YLGE0/TiAIkDjMTIDkyyyBRTCEATsJgAosRoCA1TI1F65sGBgMAEDStLBwSQAEYCBAExD0JiNAYkoDkkQJwCySExLA4gxG0L0ZDVyqhk3i85dj6xANIZAE7OCHvCtdWECAASNBLsNO/bwl1R7H2/pIrZ7HL+a5YarBLLBAigAIRIYcTWABLDFIBICkMCQdGZnObzTOtkYa3b3Pz3/ppZs1lu1xd6EnPT82SvaNGKLJadqmAhYMdpq7hIsw0l6YCYdiYkAFTMhA4CnWBONyk9BzVxl2dNikIbFdsUhNCkM9iAlGzYNK2rBGJjVx4oqLmbz8FJHrpmBUnLDTuEqujqzlFiYpJ7k7nL56ZUdYRCtAqWeZIbGaonXWDoWVAJ1XRiaCGjZ9V3cHSySYVucztkWItGM2irT0K7oznpM7jzud1ZACWF0JgHA2NMSrZJMsnCANJVEghl9LSsWdurBIiTPNjx5twsFLC7g0IorcZiey7XyKCiEoM0lWAD1VFCkg4oQba9SdH1tvla1jCsoQerV/bez858OwfQxBmA1Knmarlz5wasZoZFJ9zblSGrWhFaZ1QKcahACEy4l11ypa1HBVNsCO+Wry5uLp4jxpSeGvO07RzVtm54brJHRih0yMX4Tu6T+8tD7U65PTFpPQr0kFkgQsckn3NKriuGYF0YrXNz8s7+K7OT2RkepTowTzNGcXKfuJAs1rgw+eHX/16z73/23R3P6s/dZweUQDqw3U6VlLsxAaindCLcuaulxcaPxSsH3935IVPXpIv0ptbgTErThXTDdDjf2z+/LfpeY3ZYb+v7uvn/VE5EYoiSnkGS8k6YtJ0Me4aJtIkNxCiSxLgW/9/sbPaYAEZVL4sAMJnHT29fKOdnxAX+El/wPDi3B1ICuEqCZRdDWtdr1HFZGVL7DMx7phs6EjM5vmlu/kPmo0tJbzhCs2SpS907T997nsFowozP1qKb2AY9mEYvNwy6UcbdUd++sXVgCJZuf/OHyXx203u7yYaeNFqYrr/NfsjOs77paTWtG/cZ5qZukX43nYIAzO2vze/bm88hROuR2VSMddRnbLgzSdbmQMBo2et+7qHiLu1uz8Pf37laTegCydHH8cf0pEUaW6M34TD+kUw6IELoyUFBZfQbciXHN0eflpDE0sUoDGLQOmLlZj5kmX5l8tYf+6TXztmygVhs/clsbjgZJikUmervOLIBAUfFrLscY+Ya1mazvj3qm12gYwdAgIQYMtYkUsgs38XZYXL13VNfbvm5ZTIOs+w2d0kmT+aD/uxMs/vyJEgBoZKJm8X5zX/YcHTfsZiCgAlBgZC0rifr11bvp5KatF1F6kL3T/vw47GvXWanjp7UPfOUnmx3znfJHc7zspMfjHkgQWTgmNcmT6877P3rdpM02KMjEbAAQ0iWt4t3xpu2U1qn1TRd6y4nf3mkO795wN1dm5NdJyPV22XeV01+8twlQbZzMm6e/Eme27zJe263OLrHCYZwhyAGgTt83eL/ryDVxBH9POmwSrDZTjkcxW1unvy5yd54arK7vvL4yfNdpW2cmfEYupueuE8899XHPTb789AhAkS38c5k/cn6/6XJnG1v0oV0KYRKYxKbM/L9s0d+3Ou9g6dDHKffOZtr4yySq4Fumu1mHz9dppNupAiVHn3u5L2+xna8Dxui2tq5cUKlh9AziYA9tCW7yWeePO37bpww+dvkD8csMzt9uwUpQDCZJX8fv+VWLCGs5fvbvPVtl2ptMegXdbgtQj+QdEokHQLFpFvyjSdP/tygfxrruZ3EQLAzMGRGta6Sbr8eD9yA3frl+KZ0vPGGhi6z2tRaNL/bX0BsQAGNrhJDR5zv/eJ45vvuuP69Pz1JwRkgz86Jko7K7vDkd9MeS5bv7/jq8/S3Ept2Of777uH7OdaDtMJeo/LEADTDgFTbLzImX3x679f9Iab8T/cW/J1kVxOpSbqhu+U+o1t/dvSu1T+pLQ319/se3Rzsc2ROiG5kNcEwRIAEI0kPIXa6n8U7vjqcn1kXAYygsC0yBqlkHfZ7xv969DJuazN6s2v32/u8/3i/m+JLnivZTLrHkyychqCoptmrgYYw36+mi5MkKTiFy+0jSag0PRi6/WT//dDVpt/y/uj+8nr/c9+TUQm5noyx+kqTKqCYRUwoAYOENCtdn7bkDAmdwvBWSIkBtMnhZMmFT2pTV3rr+vv9ZXP0SSquP0ZBOphimATAMKEAGHUy3PVczejUM/yWHmbeGLNKiYpLn9u5Rtg168kf99fjH2KuACe6Pgm4bOgwFmWkCEmxy+eHE8DNrvl2ddYK0jNB0gOn6Q/CTZ1Q4+SqfWZ21PTx33f/ue9Bnrjsjr+asAo7bQts4IA6xdI5wMTVLGyyTW58imCm4MSJKbT7mRrsTIprvzfr9P3l+/n7fTbPM+mMzVcjdEWZoqsJgDCKGD4wUgQAUoTJDaRHeQLgFMA84MTCpvXrHzzir13979279UiuH5UYdpVJYVZRU050EQ1DCDpwZAEUUAybySfjGQld2JJGDTruoLL5ZtF88Pfd8Y9f69RJnXQpyhk9MbbNhIWsymIRxTRdFhiQRRgms4/N2eZxOovOCkOYbudvg+795MIrd/jLH5w7mbb749kmD41Zz1rnrI/KGSw6SK8MpcNCRWAl6EhaL03qf6rONCIIMV9NK5vujs53m7/9M2xPbJzwqIQ9HTE+L37GWU+AzCNJnycV0bQoiGMoEykJDAlXrDMoA2omVJq//fzv1f//e7qemKv+OKujUlP6fwEqHYnWeogKMQxI01VICnr0IK5YxhCepNNSBiT+9dv/zn+/1/vHryY1K+owq1w6jAwDE0wAEhQtE4QuS2oQ4ZRe/w+rOml7lFEIMbTLH25+e9X/PrufX8tB9vooIalIJ4hgCEKDI6HBNEMCONp15WtPBEtFxqR1rShrWMfPz94v3zX//VuzSsaprhIp11pEAMXEEMEpaEWsiaTgyrGlZkkXCAErrR1W0XNaJYKTCg==')
    creation_date: Mapped[DateTime] = Column(DateTime, nullable=False, default=func.now())
    last_updated: Mapped[DateTime] = Column(DateTime, nullable=True)

    email_address: Mapped['Email'] = relationship('Email', uselist=False, backref='user_account', primaryjoin='Account.id==foreign(Email.id)')
    phone_number: Mapped['Phone'] = relationship('Phone', uselist=False, backref='user_account', primaryjoin='Account.id==foreign(Phone.id)')
    balance: Mapped['Wallet'] = relationship('Wallet', uselist=False, backref='user_account', primaryjoin='Account.id==foreign(Wallet.id)')
    name: Mapped['Name'] = relationship('Name', uselist=False, backref='user_account', primaryjoin='Account.id==foreign(Name.id)')
    purchase: Mapped['Purchase'] = relationship('Purchase', uselist=True, backref='user_account', primaryjoin='Account.id==foreign(Purchase.owner)', lazy=True)
    comments: Mapped['Comment'] = relationship('Comment', uselist=True, backref='user_account', primaryjoin='Account.id==foreign(Comment.written_by)', lazy=True)

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
        return bool(session.query(cls.username).filter_by(username = form.username.data).scalar() != None)

    def password_match(form):
        return bool(form.password.data != form.verify_password.data)

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, password={self.password}, creation_date={self.creation_date})"


class Name(MyBase):
    __tablename__ = 'name_list'

    id: Mapped[int] = Column(Integer, primary_key=True, nullable=True)
    first_name: Mapped[str] = Column(String(32), nullable=False)
    last_name: Mapped[str] = Column(String(32), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime, nullable=True)

    __table_args__ = (Index('ix_fullname',first_name,last_name),)

    def __repr__(self) -> str:
        return f"Name(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"


class Email(MyBase):
    __tablename__ = 'email_list'

    id: Mapped[int] = Column(Integer, primary_key=True, nullable=True)
    email_address: Mapped[str] = Column(String(64), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint(email_address),)

    @classmethod
    def unique_email(cls,session,form):
        return bool(session.query(Email.email_address).filter_by(email_address = form.email_address.data).scalar() != None)

    def __repr__(self) -> str:
        return f"Email(id={self.id}, email_address={self.email_address})"


class Phone(MyBase):
    __tablename__ = 'phone_list'

    id: Mapped[int] = Column(Integer, primary_key=True, nullable=True)
    phone_number: Mapped[str] = Column(String(12), nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint(phone_number),CheckConstraint('char_length(phone_number) = 12', name='phone_number_length'))

    @classmethod
    def unique_phone(cls,session,form):
        return bool(session.query(Phone.phone_number).filter_by(phone_number = form.phone_number.data).scalar() != None)

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
    last_updated: Mapped[DateTime] = Column(DateTime, nullable=True)

    comments: Mapped['Comment'] = relationship('Comment', uselist=True, backref='item_comments', primaryjoin='Item.barcode==foreign(Comment.barcode)', lazy=True)
    purchases: Mapped['Purchase'] = relationship('Purchase', uselist=True, backref='item_purchase', primaryjoin='Item.barcode==foreign(Purchase.barcode)', lazy=True)

    __table_args__ = (UniqueConstraint(barcode),)


    def __repr__(self) -> str:
        return f"Item(id={self.id}, name={self.name} price={self.price}, barcode={self.barcode}, stock={self.stock})"


class Purchase(MyBase):
    __tablename__ = 'purchase_list'

    id: Mapped[int] = Column(Integer, primary_key=True)
    count: Mapped[int] = Column(Integer, nullable=False)
    owner: Mapped['int'] = Column(Integer, nullable=False)
    barcode: Mapped[str] = Column(String(length=128), nullable=False)
    date_purchased: Mapped[DateTime] = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self) -> str:
        return f"Purchase(id={self.id}, name={self.name}, name={self.count}, price={self.price}, barcode={self.barcode}, owner={self.owner})"


class Comment(MyBase):
    __tablename__ = 'item_comments_list'
    id: Mapped[int] = Column(Integer, primary_key=True)
    barcode: Mapped[str] = Column(String(length=128), nullable=False)
    written_by: Mapped['int'] = Column(Integer, nullable=False)
    title: Mapped[str] =  Column(String(length=128), nullable=False)
    body: Mapped[str] =  Column(String(length=4096), nullable=False)
    rating: Mapped[float] = Column(Integer, nullable=False)
    last_updated: Mapped[DateTime] = Column(DateTime, nullable=True)
    creation_date: Mapped[DateTime] = Column(DateTime, nullable=False, default=func.now())

    __table_args__ = (CheckConstraint('rating >= 0 AND rating <= 5', name='check_item_rating'),)

    def __repr__(self) -> str:
        return f"Comment(id={self.id}, owner={self.written_by} title={self.title}, creation_date={self.creation_date})"

class Wallet(MyBase):
    __tablename__ = 'wallet_list'
    id: Mapped[int] = Column(Integer, primary_key=True, nullable=True)
    balance: Mapped[Decimal] = Column(DECIMAL(precision=10, scale=2), nullable=False, default=1000)
    last_updated: Mapped[DateTime] = Column(DateTime, nullable=True)
    last_purchase: Mapped[DateTime] = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"Wallet(id={self.id}, balance={self.balance}"


#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@event.listens_for(Item,'after_insert')
def set_barcode(mapper,conn,target):
    target.barcode = func.md5(func.rand())
    conn.execute(Item.__table__.update().where(Item.id == target.id).values(barcode=target.barcode))
