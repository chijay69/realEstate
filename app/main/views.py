import os

from flask import render_template, redirect, flash, url_for, request, send_from_directory, current_app
from flask_login import login_required, current_user

from . import main
from .forms import ContactForm, EditProfileAdminForm, Paypal, BankForm, BitCoin, MyPersonId, MyAddress
from .. import db
from ..emails import send_async
from ..models import User


@main.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = 0
    return r


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/user')
@main.route('/user/<name>')
def user(name):
    user = User.query.filter_by(first_name=name).first_or_404()
    return render_template('main/dashboard.html', user=user)


@main.route('/deposit')
def deposit():
    return render_template('main/deposit.html', user=user)


@main.route('/about')
def about():
    return render_template('main/about.html')


@main.route('/pricing')
def pricing():
    return render_template('main/pricing.html')


@main.route('/shopping-cart')
def shopping_cart():
    return render_template('main/shopping-cart.html')


@main.route('/shopping-checkout')
def shopping_checkout():
    return render_template('main/shopping-checkout.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.Email.data
        subject = form.Subject.data
        message = form.Message.data
        send_async(email, subject, '/main/unconfirmed.html', message=message)
        flash('Your email has been sent.')
    return render_template('main/contact.html', form=form)


@main.route('/services')
def services():
    return render_template('main/services.html')


@main.route('/upgrade')
def upgrade():
    return render_template('main/upgrade.html')


@main.route('/user_create')
def user_create():
    return render_template('main/user_create.html')


@main.route('/user_create')
def user_listing():
    return render_template('main/user_listing.html')


@main.route('/profile')
def profile():
    return render_template('main/profile.html')


@main.route('/team')
def team():
    return render_template('main/display.html')


@main.route('/faq')
def faq():
    return render_template('main/faq.html')


@main.route('/agency')
def agency():
    return render_template('main/agency.html')


@main.route('/blog')
def blog():
    return render_template('main/blog-list-mix-left-sidebar.html')


@main.route('/terms-of-services')
def terms():
    return render_template('main/terms-of-services.html')


# renders team
@main.route('/display')
def display():
    return render_template('main/team.html')


@main.route('/withdraw')
def withdraw():
    send_async(current_user.email, 'Withdrawal by user', '/main/about_to_withdrawl.html', user=current_user)
    return render_template('main/withdrawpage.html')


@main.route('/bank', methods=['GET', 'POST'])
def bank():
    form = BankForm()
    if form.validate_on_submit():
        flash('Success')
        return redirect(url_for('main.upgrade'))
    return render_template('main/bank.html', form=form)


@main.route('/paypal', methods=['GET', 'POST'])
def paypal():
    form = Paypal()
    if form.validate_on_submit():
        flash('Success')
        return redirect(url_for('main.upgrade'))
    return render_template('main/paypal.html', form=form)


@main.route('/bitcoin', methods=['GET', 'POST'])
def bitcoin():
    form = BitCoin()
    if form.validate_on_submit():
        flash('Success')
        return redirect(url_for('main.upgrade'))
    return render_template('main/bitcoin.html', form=form)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile_admin():
    form = EditProfileAdminForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if form.validate_on_submit():
            user.btc_balance = form.btc_balance.data
            user.cash_balance = form.cash_balance.data
            user.level = form.level.data
        db.session.add(user)
        db.session.commit()
        flash('The user profile has been updated.')
        return redirect(url_for('.index'))
    return render_template('main/edit_profile.html', form=form)


@main.route('/buy')
def buy():
    flash('''contact the admin via the chat box on how to upgrade
    or copy this address to your wallet
    3PicVwPbw8v7pvqWMNFeZmJP4RLy7XMeBG
    ''')
    return render_template('main/upgrade.html')


@main.route('/referral')
def referral():
    flash('''Admin has not activated referral bonuses
    ''')
    return redirect(url_for('main.user', name=current_user.first_name))


@main.route('/uploads/<filename>')
def upload(filename):
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(current_app.root_path, 'templates/main')
    # Returning file from appended path
    return send_from_directory(directory=uploads, filename=filename)

#
# @main.route('/profile')
# @login_required
# def profile():
#     user = User.query.filter_by(email=current_user.email).first_or_404()
#     address_form = MyAddress()
#     persona_form = MyPersonId()
#     return render_template('main/profile.html', persona_form=persona_form, address_form=address_form, user=user)
#
#
# @main.route('/persona', methods=['POST'])
# def persona():
#     address_form = MyAddress()
#     persona_form = MyPersonId()
#
#     if persona_form.validate_on_submit():
#         pass
#         ...  # handle the register form
#     # render the same template to pass the error message
#     # or pass `form.errors` with `flash()` or `session` then redirect to /
#     return render_template('profile.html', persona_form=persona_form, address_form=address_form)
#
#
# @main.route('/address', methods=['POST'])
# def address():
#     address_form = MyAddress()
#     persona_form = MyPersonId()
#     if address_form.validate_on_submit():
#         pass
#         ...  # handle the login form
#     # render the same template to pass the error message
#     # or pass `form.errors` with `flash()` or `session` then redirect to /
#     return render_template('profile.html', persona_form=persona_form, address_form=address_form)
