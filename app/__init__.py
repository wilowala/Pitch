from flask import Flask
from flask_bootstrap import Bootstrap
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_simplemde import SimpleMDE
from flask_moment import Moment
from  dateutil.parser import *


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
simple = SimpleMDE()
moment = Moment()


def create_app(production):

    app = Flask(__name__)

    #app configurations
    app.config.from_object(config_options[production])

    # Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    simple.init_app(app)
    moment.init_app(app)

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.template_filter('strftime')
    def _jinja2_filter_datetime(date, fmt=None):
        date = parse(str(date))
        native = date.replace(tzinfo=None)
        format='%d %m %Y'
        return native.strftime(format)

    return app