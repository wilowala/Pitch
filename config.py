class Config:
    """Parent Config Class """
    

class ProdConfig(Config):
    """Production Config Class"""


class DevConfig(Config):
    """Developement Config"""
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}