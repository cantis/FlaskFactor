from flask import Flask
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy
# from flask_toastr import Toastr
from flask_login import LoginManager
from flask_migrate import Migrate


from config import DevConfig

# create global objects
db = SQLAlchemy()
bs = Bootstrap()
fa = FontAwesome()
migrate = Migrate()
# toastr = Toastr()
login_manager = LoginManager()


def create_app():
    """Set up flask app and init global objects"""
    app = Flask(__name__)

    # Load in configuration
    app.config.from_object(DevConfig())

    # initalize global objects
    db.init_app(app)
    bs.init_app(app)
    migrate.init_app(app, db)
    fa.init_app(app)
    # toastr.init_app(app)

    # Login Configuration
    # login_manager.init_app(app)
    # login_manager.login_view = 'auth_bp.login'
    # login_manager.login_message = 'Please log in...'
    # login_manager.login_message_category = 'info'

    # Import parts of our application (add new 'components' here)
    from web.routes import home, users, characters, players, parties, auth

    # Register Blueprints
    app.register_blueprint(home.home_bp)
    app.register_blueprint(auth.auth_bp)
    # app.register_blueprint(parties.party_bp)
    # app.register_blueprint(players.player_bp)
    # app.register_blueprint(users.user_bp)
    # app.register_blueprint(characters.character_bp)

    # after we're all done, return the application object. It becomes available via flask as app.
    return app
