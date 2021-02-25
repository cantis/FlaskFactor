import pytest
from flask.globals import request

from config import TestConfig
from web import create_app, db
from web.models import Player


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
        db.session.commit

        yield client
        db.drop_all()


def test_get_player_list(client):
    # arrange

    # act
    response = client.get('http://localhost:5000/player')

    # assert
    assert response.status_code == 200
    result = client.get('/player', follow_redirects=True)
    assert b'Players' in result.data
