import os
import psycopg2

class Config:
    """Parent Config Class """
    SECRET_KEY = os.urandom(112139)
    SQLALCHEMY_DATABASE_URI ="postgresql+psycopg2://username:aivwilie@localhost/pitches"

     #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "owallabilly@gmail.com"
    MAIL_PASSWORD = "@!vW1lie"

    print(MAIL_USERNAME)
    print(MAIL_PASSWORD)

    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

class ProdConfig(Config):
    """Production Config Class"""


class DevConfig(Config):
    """Developement Config"""
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}