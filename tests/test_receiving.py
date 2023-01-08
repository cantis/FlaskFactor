import pytest

from config import TestConfig
from src import create_app, db
from src.models import Character, Player, Party


@pytest.fixture(scope='session')
def app():
    app = create_app()
    config = TestConfig()
    app.config.from_object(config)
    return app


@pytest.fixture(scope='function')
def client(app):
    with app.app_context():
        client = app.test_client()
        db.create_all()

        db.session.add(Player(
            first_name='Payton',
            last_name='Young',
            email='someone@noplace.com',
            is_active=True)
        )

        db.session.add(Party(
            party_name='Adventure Inc',
            is_active=True
            )
        )

        db.session.add(Character(
            character_name='Milo Thorngage',
            character_class='Investigator',
            is_active=True,
            is_dead=False,
            player_id=1,
            party_id=1
        ))
        db.session.commit()

        yield client
        db.drop_all()


def test_navigate_to_receiving_form(client):
    # arrange

    # act
    result = client.get('/receiving', follow_redirects=True)

    # assert
    assert b'Receiving' in result.data
