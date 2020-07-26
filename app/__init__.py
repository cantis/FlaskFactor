from flask import Flask
from flask_fontawesome import FontAwesome
from flask_bootstrap import Bootstrap

bs = Bootstrap()
fa = FontAwesome()


def create_app():
    """Create Flask Application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('app.config.DevConfig')

    # Set up global objects
    bs.init_app(app)
    fa.init_app(app)

    # Database object, declared in the models __init__.py
    from .models import db
    db.init_app(app)

    # Import parts of our application (add new 'components' here)
    from .home import home
    from .users import users
    from .characters import characters

    # Register Blueprints
    app.register_blueprint(home.home_bp)
    app.register_blueprint(users.user_bp)
    app.register_blueprint(characters.character_bp)

    with app.app_context():
        db.create_all()
        return app
