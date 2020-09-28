import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_toastr import Toastr
from flask_login import LoginManager
from app.config import TestConfig
import unittest

bs = Bootstrap()
fa = FontAwesome()
toastr = Toastr()
login_manager = LoginManager()


class TestBase(unittest.TestCase):
    """ A base test case for Factor """

    def create_test_app():
        print(__file__)
        app = Flask(__name__, template_folder='c:\\Users\\Evan Young\\Source\\FlaskHW\\app\\templates')

        # Load in configuration
        app.config.from_object(TestConfig())

        # Set up global objects
        bs.init_app(app)
        fa.init_app(app)
        toastr.init_app(app)
        login_manager.init_app(app)

        # Login Configuration
        login_manager.login_view = 'user_bp.login'
        login_manager.login_message = 'Please log in...'
        login_manager.login_message_category = 'info'

        # Create the DB and it's initial lookups
        from app.models import db
        from app.models.item_type import Item_Type

        db.init_app(app)
        with app.app_context():
            db.create_all()

            # Load lookup values
            db.session.add(Item_Type(item_type='Ammunition'))
            db.session.add(Item_Type(item_type='Armour'))
            db.session.add(Item_Type(item_type='Equipment'))
            db.session.add(Item_Type(item_type='Melee'))
            db.session.add(Item_Type(item_type='Misc Magic'))
            db.session.add(Item_Type(item_type='Potion'))
            db.session.add(Item_Type(item_type='Ranged'))
            db.session.add(Item_Type(item_type='Ring'))
            db.session.add(Item_Type(item_type='Scroll'))
            db.session.add(Item_Type(item_type='Wand'))
            db.session.add(Item_Type(item_type='Treasure'))
            db.session.commit()

        # Import parts of our application (add new 'components' here)
        from app.routes import home, users, characters, players, parties

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
