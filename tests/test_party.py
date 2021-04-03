import pytest


from config import TestConfig
from web import create_app, db
from web.models import Character, Player, Party


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
            party_name='Adventure Inc.',
            is_active=True
            )
        )
        db.session.commit()

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


def test_navigate_to_party_form(client):
    # arrange

    # act
    result = client.get('/party', follow_redirects=True)

    # assert
    assert b'Parties' in result.data


def test_party_listed(client):
    # arrange

    # act
    result = client.get('/party', follow_redirects=True)

    # assert
    assert b'Adventuring Inc.' in result.data


def test_party_add_ok(client):
    # arrange
    data = dict(party_name='Mighty Nine')

    # act
    client.post('/party/add', data=data, follow_redirects=True)

    # assert
    party = Party.query.get(2)
    assert party.party_name == 'Mighty Nine'
    assert party.is_active is True


def test_party_edit_get_ok(client):
    # arrange

    # act
    response = client.get('party/1', follow_redirects=True)

    # assert
    assert b'Edit Party' in response.data


def test_party_edit_post_ok(client):
    # arrange
    data = dict(party_name='Chaos Co.', is_active='false')

    # act
    client.post('party/1', data=data, follow_redirects=True)

    # assert
    party = Party.query.get(1)
    assert party.party_name == 'Chaos Co.'
    assert party.is_active is False

