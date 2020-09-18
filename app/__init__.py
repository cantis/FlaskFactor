from flask import Flask
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_toastr import Toastr
from flask_login import LoginManager
from app.config import DevConfig

bs = Bootstrap()
fa = FontAwesome()
toastr = Toastr()
login_manager = LoginManager()


def create_app():
    """Create Flask Application."""
    app = Flask(__name__, instance_relative_config=False)

    # Load in configuration
    config = DevConfig()
    app.config.from_object(config)

    # Set up global objects
    bs.init_app(app)
    fa.init_app(app)
    toastr.init_app(app)
    login_manager.init_app(app)

    # Login Configuration
    login_manager.login_view = 'user_bp.login'
    login_manager.login_message = 'Please log in...'
    login_manager.login_message_category = 'info'

    # Database object, declared in the models __init__.py
    # DB Creation is now handled in the seperate ini_data.py file, run this seperately to init the db.
    from .models import db
    db.init_app(app)

    # Import parts of our application (add new 'components' here)
    from .routes import home, users, characters, players, parties

    # Register Blueprints
    app.register_blueprint(parties.party_bp)
    app.register_blueprint(players.player_bp)
    app.register_blueprint(users.user_bp)
    app.register_blueprint(characters.character_bp)
    app.register_blueprint(home.home_bp)

    # Imported User here to avoid the circular, hard to use User when user isn't defined yet
    from app.models.user import User

    # Required by flask_login to be defined and available.
    @login_manager.user_loader
    def load_user(user_id):
        """ Given 'user_id', return the associated user object.
        :param unicode user_id: user_id (email) of user to retrieve
        """
        user = User.query.filter_by(user_id=user_id).first()
        if user is not None:
            return user
        else:
            return None

    # after we're all done, return the application object. It becomes available via flask as app.
    return app
