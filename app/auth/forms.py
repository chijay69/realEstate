from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField
from wtforms.validators import Email, DataRequired, Length, ValidationError, EqualTo

from app.models import User


class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Account')

    @staticmethod
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered')


class LoginForm(FlaskForm):
    email = StringField('Your Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Login')


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('This account does not Exist')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Current password', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must '
                                                                                                   'match.')])
    password2 = PasswordField('Confirm your password', validators=[DataRequired()])
    submit = SubmitField('Save changes')


class ChangeEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    email1 = StringField('Email', validators=[DataRequired(), Email(), EqualTo('email2', message='Emails must match')])
    email2 = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save changes')


class ProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    submit = SubmitField('Save changes')
