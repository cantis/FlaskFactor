import pytest

# from src import create_app, db
from src import db
from src.models import Character, Player, Party


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


def test_navigate_to_character_form(client):
    # arrange

    # act
    result = client.get('/character', follow_redirects=True)

    # assert
    assert b'Characters' in result.data


def test_character_listed(client):
    # arrange

    # act
    result = client.get('/character', follow_redirects=True)

    # assert
    assert b'Milo Thorngage' in result.data
    assert b'Investigator' in result.data


def test_character_add_ok(client):
    # arrange
    data = dict(
        character_name='Barbog',
        character_class='Barbarian',
        party_id=1,
        player_id=1
        )

    # act
    client.post('/character/add', data=data, follow_redirects=True)

    # assert
    character = Character.query.get(2)
    assert character.character_name == 'Barbog'
    assert character.character_class == 'Barbarian'
    assert character.player_id == 1
    assert character.party_id == 1
    assert character.is_active is True
    assert character.is_dead is False


def test_character_edit_get_ok(client):
    # arrange

    # act
    result = client.get('/character/1', follow_redirects=True)

    # assert
    assert b'Edit Character' in result.data


def test_charcter_edit_post_ok(client):
    # arrange
    data = dict(
            id=1,
            character_name='John',
            character_class='Smith',
            is_active='false',
            is_dead='true',
            player_id=1,
            party_id=1
    )

    # act
    result = client.post('/character/1', data=data, follow_redirects=True)

    # assert
    character = Character.query.get(1)
    assert character.character_name == 'John'
    assert character.character_class == 'Smith'
    assert character.is_active is False
    assert character.is_dead is True
    assert character.player_id == 1
    assert character.party_id == 1
    assert b'Add Character' in result.data
