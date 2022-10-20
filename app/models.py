from datetime import datetime, date, time
from flask import current_app
from flask_login import UserMixin, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

import enum


class PropertyStatusEnum(enum.Enum):
    rent = 'rent'
    sale = 'sale'


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    property_type = db.Column(db.String(64), index=True)
    property_status = employment_status = db.Column(db.Enum(PropertyStatusEnum), default=PropertyStatusEnum.rent, nullable=True),
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
    join_time = db.Column(db.DateTime(), default=datetime.now())
    join_date = db.Column(db.DateTime(), default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    address = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(64), nullable=True)
    password_hash = db.Column(db.String(128))
    properties = db.relationship('Property', backref='user', lazy='dynamic')

    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     if self.btc_balance is None:
    #         self.btc_balance = 0.0
    #     if self.cash_balance is None:
    #         self.cash_balance = 0.0
    #     if self.level is None:
    #         self.level = 'Starter'

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



