import os
import psycopg2

class Config:
    """Parent Config Class """
    SECRET_KEY = os.urandom(112139)
    SQLALCHEMY_DATABASE_URI = "postgresql://nzkxvkskpjicmo:1b06c694733fa527e7398f05bc4804d8f8d08302bad21d9c61bad3947b404777@ec2-52-4-104-184.compute-1.amazonaws.com:5432/d4bhl24qmjig4g"
                            #    postgresql://lvehippqxcsvwi:ac06666772ef8cb519ff557ec4222c24b552f70dd58e46c4a9d6f1956f28076f@ec2-54-172-175-251.compute-1.amazonaws.com:5432/d9bkvog34oualq
    # "postgresql+psycopg2://username:aivwilie@localhost/pitches"

     #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "billyowalla@gmail.com"
    MAIL_PASSWORD = "Aivw12345"

    print(MAIL_USERNAME)
    print(MAIL_PASSWORD)

    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

class ProdConfig(Config):
    """Production Config Class"""

    SQLALCHEMY_DATABASE_URI = "postgresql://nzkxvkskpjicmo:1b06c694733fa527e7398f05bc4804d8f8d08302bad21d9c61bad3947b404777@ec2-52-4-104-184.compute-1.amazonaws.com:5432/d4bhl24qmjig4g"
    # postgres://nzkxvkskpjicmo:1b06c694733fa527e7398f05bc4804d8f8d08302bad21d9c61bad3947b404777@ec2-52-4-104-184.compute-1.amazonaws.com:5432/d4bhl24qmjig4g

class DevConfig(Config):
    """Developement Config"""
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}