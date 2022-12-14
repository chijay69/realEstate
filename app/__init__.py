from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
socket = SocketIO()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify()
        sslify.init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    socket.init_app(app, cors_allowed_origins="*")
    db.init_app(app)
    login_manager.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
