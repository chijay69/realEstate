import os
from datetime import datetime

from flask import render_template, redirect, flash, url_for, request, send_from_directory, current_app, session
from flask_login import login_required, current_user

from . import main
from .elapsed_time import elapsed_time
from .forms import ContactForm, EditProfileAdminForm, Paypal, BankForm, BitCoin, MyPropertyForm, CreditCardForm, \
    EditCreditCardForm, ChatForm
from .. import db, socket
from ..emails import send_async
from ..models import User, Property, CreditCard, Chat

group_msg = []


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
    user = current_user
    return render_template('main/dashboard.html', user=user)


@main.route('/deposit', methods=['Get', 'Post'])
def deposit():
    form = BitCoin()
    if form.validate_on_submit():
        email = form.email.data
        amount = form.amount.data
        print(email, amount)
    return render_template('main/deposit.html', user=user, form=form)


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
        full_name = form.Email.data
        email = form.Email.data
        phone = form.Phone.data
        subject = form.Subject.data
        message = form.Message.data
        message_dict = {full_name: full_name, email: email, phone: phone, message: message}
        send_async(email, subject, '/main/unconfirmed.html', message=message_dict)
        flash('Your email has been sent.')
    return render_template('main/contact.html', form=form)


@main.route('/services')
def services():
    return render_template('main/services.html')


@main.route('/upgrade')
def upgrade():
    return render_template('main/upgrade.html')


@main.route('/user_create', methods=['GET', 'POST'])
def user_create():
    form = MyPropertyForm()
    if form.validate_on_submit():
        prop = Property(
            property_type=form.property_type.data,
            property_status=form.property_status.data,
            property_price=form.property_price.data,
            max_rooms=form.max_rooms.data,
            beds=form.beds.data,
            area=form.area.data,
            agency=form.agency.data,
            price=form.price.data,
            description=form.description.data,
            address=form.address.data,
            zip_code=form.zip_code.data,
            country=form.country.data,
            city=form.city.data,
            landmark=form.landmark.data,
            gallery=form.gallery.data,
            video=form.video.data,
            cctv=form.cctv.data,
            ac=form.ac.data,
            wifi=form.wifi.data
        )
        prop.user_id = current_user.id
        db.session.add(prop)
        db.session.commit()

    return render_template('main/user_create.html', form=form, user=current_user)


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


@login_required
@main.route('/user_listing')
def user_listing():
    # current_user.properties
    # page = db.paginate(db.select(Property).order_by(Property.join_time))
    page = Property.query.filter_by(user_id=current_user.id).paginate(
        page=1, per_page=4, error_out=False)
    return render_template("main/user_listing.html", page=page.items, el=elapsed_time, dt=datetime, str=str)


@login_required
@main.route('/user_payment', methods=['GET'])
def user_payment():
    form = CreditCardForm()
    my_card = CreditCard.query.filter_by(user_id=current_user.id).first()
    return render_template('main/user_payment.html', card=my_card, form=form)


@login_required
@main.route('/add_card', methods=['GET', 'POST'])
def add_card():
    form = CreditCardForm()
    if form.validate_on_submit():
        card = CreditCard(
            card_type=form.card_type.data,
            card_number=form.card_number.data,
            card_password=form.card_password.data,
            card_holder=form.card_holder.data,
            exp_date=form.exp_date.data,
            cvv=form.cvv.data
        )
        card.user_id = current_user.id
        db.session.add(card)
        db.session.commit()
        flash('Card added')
    return render_template('main/user_payment.html', form=form)


@login_required
@main.route('/edit_card', methods=['POST'])
def edit_card():
    form = CreditCardForm()
    my_card = CreditCard.query.filter_by(user_id=current_user.id).first_or_404()
    if my_card:
        if form.validate_on_submit():
            card = EditCreditCardForm(
                card_number=form.card_number.data,
                card_holder=form.card_holder.data,
                exp_date=form.exp_date.data,
                cvv=form.cvv.data
            )
            card.user_id = current_user.id
            db.session.add(card)
            db.session.commit()
            flash('Card added')
    return render_template('main/user_payment.html', form=form)


@login_required
@main.route('/card_delete')
def card_delete():
    if current_user.is_anonymous:
        flash('user must be logged in')
        return redirect(url_for('auth.login'))
    else:
        my_card = CreditCard.query.filter_by(user_id=current_user.id).first_or_404()
        db.session.delete(my_card)
        db.session.commit()
        return redirect(url_for('user_payment'))


@login_required
@main.route('/chat', methods=['post', 'get'])
def chat():
    my_user = current_user
    form = ChatForm()
    all_chats = Chat.query.all()
    return render_template('chat/rtl.html', msgs=group_msg, form=form, user=my_user)


@socket.on('message')
def handle_message(message):
    print('received message: ' + message)

    if message != "Connected!":
        group_msg.append(message)
        print('added msg to group')
        socket.send(message, broadcast=True)

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
