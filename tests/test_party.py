import os
import pytest

from src import create_app, db
from src.models import Character, Player, Party


@pytest.fixture(scope="session")
def app():
    os.environ["ENV"] = "test"
    app = create_app()
    yield app


@pytest.fixture(scope="function")
def client(app):
    with app.app_context():
        # set up the test client and database
        client = app.test_client()
        db.create_all()

        # Set the logged in player
        db.session.add(
            Player(
                first_name="Payton",
                last_name="Young",
                email="someone@noplace.com",
                is_active=True,
            )
        )

        # Add a party to the database
        db.session.add(Party(party_name="Adventure Inc.", is_active=True))
        db.session.commit()

        # Add a character to the database
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

        yield client

        # tear down the database
        db.drop_all()


def test_navigate_to_party_form(client):
    # arrange

    # act
    result = client.get("/party", follow_redirects=True)

    # assert
    assert b"Parties" in result.data


def test_party_listed(client):
    # arrange

    # act
    result = client.get("/party", follow_redirects=True)

    # assert
    assert b"Adventuring Inc." in result.data


# def test_party_add_ok(client, mocker):
#     # arrange
#     # mock form data and the database session
#     mocker.patch(
#         "app.parties.AddPartyForm",
#         Mock(
#             return_value=Mock(
#                 validate_on_submit=Mock(return_value=True),
#                 party_name="Test Party",
#             )
#         ),
#     )
#     mocker.patch("app.views.db.session.add")
#     mocker.patch("app.views.db.session.commit")

#     data = dict(party_name="Mighty Nine")

#     # act
#     response = client.post(
#         url_for("party_bp.add_party"),
#     )

# client.post("/party/add", data=data, follow_redirects=True)

# assert
# party = Party.query.get(2)
# assert party.party_name == "Mighty Nine"
# assert party.is_active is True


def test_party_edit_get_ok(client):
    # arrange

    # act
    response = client.get("party/1", follow_redirects=True)

    # assert
    assert b"Edit Party" in response.data


def test_party_edit_post_ok(client):
    # arrange
    data = dict(party_name="Chaos Co.", is_active="false")

    # act
    client.post("party/1", data=data, follow_redirects=True)

    # assert
    party = Party.query.get(1)
    assert party.party_name == "Chaos Co."
    assert party.is_active is False
