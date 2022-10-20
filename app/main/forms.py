from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FloatField, IntegerField, DateField, BooleanField, \
    SelectField
from wtforms.validators import Length, Email, DataRequired
from .read import get_country_dict


class ContactForm(FlaskForm):
    First_name = StringField('First Name', validators=[Length(0, 64)])
    Last_name = StringField('Last Name', validators=[Length(0, 64)])
    Email = StringField('Email', validators=[Length(1, 64), Email()])
    Subject = StringField('Subject', validators=[Length(1, 64)])
    Message = TextAreaField('Messages')
    submit = SubmitField('Send Message')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    btc_balance = FloatField('BTC BALANCE')
    cash_balance = FloatField('CASH BALANCE')
    level = StringField('Level', validators=[DataRequired()])
    submit = SubmitField('Submit')


class BankForm(FlaskForm):
    name = StringField('Account Name', validators=[DataRequired(), Length(1, 128)])
    bank_name = StringField('BankName', validators=[DataRequired(), Length(1, 128)])
    account_no = IntegerField('Account Number')
    submit = SubmitField('Withdraw')


class Paypal(FlaskForm):
    name = StringField('FullName', validators=[Length(1, 128)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Withdraw')


class BitCoin(FlaskForm):
    name = StringField('FullName', validators=[DataRequired(), Length(1, 128)])
    address = StringField('Address', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Withdraw')


class MyPersonId(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    displayname = StringField('Display Name', validators=[DataRequired()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    DOB = DateField('Date Of Birth', validators=None)
    DP = BooleanField('Use full name for display', default=False)


class MyAddress(FlaskForm):
    address_one = StringField('Address Line 1', validators=[DataRequired()])
    address_two = StringField('Address Line 2', validators=None)
    state = IntegerField('State', validators=[DataRequired()])
    country = SelectField('Country', validators=[DataRequired()], choices=get_country_dict())


class MyPropertyForm(FlaskForm):
    property_type = StringField('Property type')
    property_status = SelectField('Property status', validators=[DataRequired()],
                                  choices=[('rent', 'rent'), ('sale', 'sale')])
    property_price = FloatField('Property price')
    max_rooms = IntegerField('Max rooms')
    beds = IntegerField('Beds')
    baths = IntegerField('Baths')
    area = IntegerField('Area')
    agency = StringField('Agency')
    price = FloatField('Price')
    description = StringField('Description')
    address = StringField('Address')
    zip_code = IntegerField('Zip Code')
    country = StringField('Country')
    city = StringField('City')
    landmark = StringField('Landmark')
    gallery = StringField('Gallery')
    video = StringField('Video')
    cctv = BooleanField('cctv')
    ac = BooleanField('ac')
    wifi = BooleanField('wifi')




