from flask import Flask
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_toastr import Toastr
from flask_login import LoginManager

bs = Bootstrap()
fa = FontAwesome()
toastr = Toastr()
login_manager = LoginManager()


def create_app():
    """Create Flask Application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('app.config.DevConfig')

    # Set up global objects
    bs.init_app(app)
    fa.init_app(app)
    toastr.init_app(app)
    login_manager.init_app(app)

    # Database object, declared in the models __init__.py
    from .models import db
    db.init_app(app)

    # Import parts of our application (add new 'components' here)
    from .home import home
    from .users import users
    from .characters import characters
    from .players import players

    # Register Blueprints
    app.register_blueprint(home.home_bp)
    app.register_blueprint(users.user_bp)
    app.register_blueprint(characters.character_bp)
    app.register_blueprint(players.player_bp)

    with app.app_context():
        db.create_all()

    # Imported User here to avoid the circular, hard to use User when user isn't defined yet
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        """ Given 'user_id', return the associated user object.
        :param unicode user_id: user_id (email) of user to retrieve
        """
        user = User.get(user_id)
        if user is not None:
            return user
        else:
            return None

    return app
