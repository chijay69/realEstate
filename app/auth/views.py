from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from . import auth
from .forms import LoginForm, RegistrationForm, ForgotForm, ResetPasswordForm, ChangePasswordForm, ChangeEmailForm, \
    ProfileForm
from .. import db
from ..emails import send_async
from ..models import User


@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, first_name=form.firstname.data, last_name=form.lastname.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.user', name=current_user.first_name)
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_async(current_user.email, 'Confirm Your Account', 'auth/email/confirm.html', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/forgot', methods=["GET", "POST"])
def forgot():
    if current_user.is_authenticated:
        flash('Log out to reset password')
        return redirect(url_for('main.index'))
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user.password_hash = generate_password_hash('cat')
            flash('just added password')
            db.session.commit()
            flash('Password Reset Complete, login.')
            return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form)


@auth.route('/reset', methods=["GET", "POST"])
def reset():
    if current_user.is_authenticated:
        flash('Log out to reset password')
        return redirect(url_for('main.index'))
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            send_async(user.email, 'Password reset requested', 'auth/email/recover.html', token=token)
            flash('An email has been set on how to reset your password')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset.html', form=form)


@auth.route('/reset/<token>', methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        flash('Log out to reset password')
        return redirect(url_for('main.index'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('Expired or invalid token', 'warning')
        return redirect(url_for('auth.reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        password_hash = generate_password_hash(password)
        user.password_hash = password_hash
        flash('just added password')
        db.session.commit()
        flash('Password Reset Complete, login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_with_token.html', form=form, token=token)


@auth.route('/profile')
@login_required
def profile():
    password_form = ChangePasswordForm()
    email_form = ChangeEmailForm()
    profile_form = ProfileForm()
    return render_template('auth/profile.html', email_form=email_form, password_form=password_form, profile_form=profile_form)


@login_required
@auth.route('/email', methods=['POST'])
def email():
    password_form = ChangePasswordForm()
    email_form = ChangeEmailForm()

    if email_form.validate_on_submit():
        u = User.query.filter_by(email=email_form.email.data).first()
        u.email = email_form.email2.data
        db.session.add(u)
        db.session.commit()
        flash('Profile updated successfully')
        # handle the register form
    # render the same template to pass the error message
    # or pass `form.errors` with `flash()` or `session` then redirect to /
    return render_template('auth/profile.html', email_form=email_form, password_form=password_form)


@login_required
@auth.route('/passwd', methods=['POST'])
def passwd():
    password_form = ChangePasswordForm()
    email_form = ChangeEmailForm()

    if password_form.validate_on_submit():
        u = User.query.filter_by(email=current_user.email).first()
        u.password_hash = password_form.password2.data
        db.session.add(u)
        db.session.commit()
        flash('Profile updated successfully')
        # handle the login form
    # render the same template to pass the error message
    # or pass `form.errors` with `flash()` or `session` then redirect to /
    return render_template('auth/profile.html', email_form=email_form, password_form=password_form)


@login_required
@auth.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if current_user.is_authenticated:
        profile_form = ProfileForm()
        if profile_form.validate_on_submit():
            user = User.query.filter_by(email=current_user.email).first()
            if user:
                user.first_name = profile_form.first_name
                user.last_name = profile_form.last_name
                user.address = profile_form.address
                user.city = profile_form.city
                user.state = profile_form.state
                db.session.add(user)
                db.session.commit()
                flash('Profile updated successfully')
            else:
                flash('Users does not exist')
        else:
            flash('Fill form correctly')
    else:
        flash('User must be logged in')

