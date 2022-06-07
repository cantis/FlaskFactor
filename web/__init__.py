from flask import Flask
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy
# from flask_toastr import Toastr
from flask_login import LoginManager
from flask_migrate import Migrate
import os

from config import DevConfig, StageConfig

# create global objects
db = SQLAlchemy()
bs = Bootstrap()
fa = FontAwesome()
migrate = Migrate()
# toastr = Toastr()
login_manager = LoginManager()


def create_app() -> Flask:
    """Set up flask app and init global objects"""
    app = Flask(__name__)

    # Load in configuration
    environment = os.getenv('ENV')

    if environment == 'debug':
        app.config.from_object(DevConfig())

    if environment == 'stage':
        app.config.from_object(StageConfig())

    # initalize global objects
    db.init_app(app)
    bs.init_app(app)
    migrate.init_app(app, db)
    fa.init_app(app)
    # toastr.init_app(app)

    # Login Configuration
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    # login_manager.login_message = 'Please log in...'
    # login_manager.login_message_category = 'info'

    # Import parts of our application (add new 'components' here)
    from web.routes import home, characters, players, parties, auth, errors, receiving

    # Register Blueprints
    app.register_blueprint(home.home_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(players.player_bp)
    app.register_blueprint(characters.character_bp)
    app.register_blueprint(parties.party_bp)
    app.register_blueprint(errors.error_bp)
    app.register_blueprint(receiving.receiving_bp)

    # after we're all done, return the application object. It becomes available via flask as app.
    return app


def seed():
    """ Seed the database with sample data """
    # Item Types

    from web.models import db, ItemType
    db.session.add(ItemType(id=1, item_type='Melee'))
    db.session.add(ItemType(id=2, item_type='Ranged'))
    db.session.add(ItemType(id=3, item_type='Armour'))
    db.session.add(ItemType(id=4, item_type='Ammunition'))
    db.session.add(ItemType(id=5, item_type='Equipment'))
    db.session.add(ItemType(id=6, item_type='Potion'))
    db.session.add(ItemType(id=7, item_type='Wand'))
    db.session.add(ItemType(id=8, item_type='Ring'))
    db.session.add(ItemType(id=9, item_type='Scroll'))
    db.session.add(ItemType(id=10, item_type='Misc Magic'))
    db.session.add(ItemType(id=11, item_type='Treasure'))
    db.session.add(ItemType(id=12, item_type='Consumable'))
    db.session.commit()
