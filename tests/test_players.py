import pytest

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
        db.session.commit()

        yield client
        db.drop_all()


def test_navigate_to_player_list(client):
    # arrange

    # act
    result = client.get('/player', follow_redirects=True)

    # assert
    assert b'Players' in result.data


def test_player_listed(client):
    """ See if our test player is listed """
    # arrange

    # act
    result = client.get('/player', follow_redirects=True)

    # assert
    assert b'Payton' in result.data


def test_add_player(client):
    # arrange
    data = dict(first_name='Adam', last_name='Alpha', email='noone@escape.ca', is_active='true')

    # act
    client.post('/player/add', data=data, follow_redirects=True)

    # assert
    player = Player.query.get(2)
    assert player.first_name == 'Adam'
    assert player.last_name == 'Alpha'
    assert player.email == 'noone@escape.ca'
    assert player.is_active is True


def test_edit_player(client):
    # arrange
    # Note: https://github.com/wtforms/wtforms/issues/290
    data = dict(id=1, first_name='Betty', last_name='Beta', email='bbeta@noplace.com', is_active='false')

    # act
    result = client.post('/player/1', data=data, follow_redirects=True)

    # assert
    player = Player.query.get(1)
    assert player.first_name == 'Betty'
    assert player.last_name == 'Beta'
    assert player.email == 'bbeta@noplace.com'
    assert player.is_active is False
    assert b'Add Player' in result.data


def test_show_player_form(client):
    # arrange

    # act
    result = client.get('/player', follow_redirects=True)

    # assert
    assert b'Add Player' in result.data


def test_show_player_edit_form(client):
    # arrange

    # action
    result = client.get('/player/1', follow_redirects=True)

    # assert
    assert b'Edit Player' in result.data