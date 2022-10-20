import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ngozikama@19'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'chichindundu@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'qivecvaguacbtlub')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN', 'chijay69@outlook.com')
    SSL_REDIRECT = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'templates\main')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 3

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://njsogkdqorabqa:992c92f0512d5a7bd15d566488689f1360b6684c09d5b64bd12d3c9a65ef4244@ec2-44-195-132-31.compute-1.amazonaws.com:5432/db6nsvc880h875'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False
    SSL_REDIRECT = True
    # vbwngulfddcpal IS THE OWNER SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or
    # 'postgresql://fccmgxakoiktbg:e890e52e36c2e4861997175923d3ae74aaae43006a092521b6cff2b7090d3895@ec2-184-73-243
    # -101.compute-1.amazonaws.com:5432/dfimbmmvq1ug8d' old database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://njsogkdqorabqa:992c92f0512d5a7bd15d566488689f1360b6684c09d5b64bd12d3c9a65ef4244@ec2-44-195-132-31.compute-1.amazonaws.com:5432/db6nsvc880h875'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
