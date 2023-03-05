import os
from flask import Flask
import pytest

from src import db
from src.models import Character, Item_Type, Party, Player

from src import create_app


@pytest.fixture(scope='session')
def app():
    '''Shared app fixture for the entire test session.'''
    os.environ['ENV'] = 'test'
    app = create_app()
    yield app


# Bit of an experiment here. I'm not sure if this is the best way to do this.
# I'm trying to create a shared base client fixture that will create the
# database and populate it with some test data.
@pytest.fixture(scope='function')
def client_two(app: Flask):
    '''Shared client fixture for the entire test session.'''

    with app.app_context():
        # set up the test client and database
        client = app.test_client()
        db.create_all()

        # Player
        db.session.add(
            Player(
                first_name="Payton",
                last_name="Young",
                email="someone@noplace.com",
                is_active=True,
            )
        )
        db.session.commit()

        # Party
        db.session.add(
            Party(
                party_name="Adventure Inc.",
                is_active=True))
        db.session.commit()

        # Character
        db.session.add(
            Character(
                character_name="Milo Thorngage",
                character_class="Investigator",
                is_active=True,
                is_dead=False,
                player_id=1,
                party_id=1,
            )
        )
        db.session.commit()

        # Item_Types
        Item_Types = [
            'melee',
            'ranged',
            'armour',
            'shield',
            'potion',
            'scroll',
            'wand',
            'treasure',
            'misc_magic',
        ]
        for item_type in Item_Types:
            db.session.add(
                Item_Type(
                    item_type=item_type,
                )
            )
        db.session.commit()

        yield client

        # tear down the database
        db.drop_all()
