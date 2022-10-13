import threading

from flask import render_template, copy_current_request_context
from flask_mail import Message

from app import mail


def send_async(to, subject, template, **kwargs):
    msg = Message(subject, sender='chichindundu@gmail.com', recipients=[to])
    msg.html = render_template(template, **kwargs)

    @copy_current_request_context
    def send_email(msg):
        mail.send(msg)

    sender = threading.Thread(target=send_email, args=(msg,))
    sender.start()
