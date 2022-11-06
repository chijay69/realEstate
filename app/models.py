import enum
from datetime import datetime

from flask import current_app
from flask_login import UserMixin, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class PropertyStatusEnum(enum.Enum):
    rent = 'rent'
    sale = 'sale'


class CardTypeEnum(enum.Enum):
    debit = 'debit card'
    credit = 'credit card'


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    property_type = db.Column(db.String(64), index=True)
    property_status = db.Column(db.Enum(PropertyStatusEnum))
    property_price = db.Column(db.Float)
    max_rooms = db.Column(db.Integer)
    beds = db.Column(db.Integer)
    baths = db.Column(db.Integer)
    area = db.Column(db.BigInteger)
    agency = db.Column(db.String(64))
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    address = db.Column(db.String(128))
    zip_code = db.Column(db.Integer)
    country = db.Column(db.String(64))
    city = db.Column(db.String(64))
    landmark = db.Column(db.Text, nullable=True)
    gallery = db.Column(db.String(64), nullable=True)
    video = db.Column(db.String(64), nullable=True)
    emergency_exit = db.Column(db.Boolean)
    cctv = db.Column(db.Boolean)
    wifi = db.Column(db.Boolean)
    parking = db.Column(db.Boolean)
    ac = db.Column(db.Boolean)
    join_time = db.Column(db.DateTime(), default=datetime.utcnow(), index=True)
    join_date = db.Column(db.DateTime(), default=datetime.utcnow(), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class CreditCard(db.Model):
    __tablename__ = 'credit_cards'
    id = db.Column(db.Integer, primary_key=True)
    card_type = db.Column(db.Enum(CardTypeEnum))
    card_password = db.Column(db.String(128))
    card_number = db.Column(db.BigInteger)
    card_holder = db.Column(db.String(128))
    exp_date = db.Column(db.Date)
    cvv = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)


def check_hash_func(password_hash, password):
    try:
        bcrypt.checkpw(password, password_hash)
    except:
        raise ValueError


class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(150), index=True)
    join_time = db.Column(db.Time(), default=datetime.utcnow(), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    address = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(64), nullable=True)
    password_hash = db.Column(db.String(150))
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow(), index=True)
    properties = db.relationship('Property', backref='user', lazy='dynamic')
    credit_cards = db.relationship('CreditCard', backref=db.backref('user', uselist=False), cascade='all, delete-orphan', uselist=False)
    chat = db.relationship('Chat', backref=db.backref('user', uselist=False), cascade='all, delete-orphan', uselist=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @property
    def is_administrator(self):
        return current_user.email == 'chijay59@gmail.com'

    def __repr__(self):
        return '<User %r>' % self.first_name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
