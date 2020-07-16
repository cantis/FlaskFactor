from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
from flask_bootstrap import Bootstrap

bs = Bootstrap()
fa = FontAwesome()
db = SQLAlchemy()


def create_app():
    """Create Flask Application."""
    app = app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    # Set up global objects
    bs.init_app(app)
    fa.init_app(app)
    db.init_app(app)

    # Import parts of our application (add new 'components' here)
    from .home import home
    # from .users import user
    from .characters import characters

    # Register Blueprints
    app.register_blueprint(home.home_bp)
    # app.register_blueprint(user.user_bp)
    app.register_blueprint(characters.character_bp)

    with app.app_context():
        return app
