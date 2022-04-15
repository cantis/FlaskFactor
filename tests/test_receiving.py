""" Tests for receiving """
import pytest

from config import TestConfig
from web import create_app, db
from web.models import Party, Receiving, ItemType
from web.routes.receiving import next_receiving_id


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

        db.session.add(ItemType(id='1', name='Melee'))

        db.session.add(Party(
            party_name='Adventure Inc.',
            is_active=True
            )
        )

        yield client
        db.drop_all()


# Route Tests
def test_navigate_to_receiving(client):
    # arrange

    with client.application.test_request_context():
        # act
        response = client.get('/receiving')

        # assert
        assert response.status_code == 200


# Utility Tests
def test_next_receiving_number_returns_one_when_empty(client):
    # arrange

    with client.application.test_request_context():
        # act
        next_receiving_number = next_receiving_id(selected_party_id=1)

        # assert
        assert next_receiving_number == 1


def test_next_receiving_number_returns_next_number(client):

    with client.application.test_request_context():
        # arrange
        db.session.add(Receiving(
            receipt_id=1,
            session_id=1,
            party_id=1,
            item_type_id='1',
            quantity=4,
            item_name='sword',
            isCommitted=False,
            item='Short Sword',
            purchase_price=10.00
        ))
        db.session.commit()

        # act
        next_receiving_number = next_receiving_id(selected_party_id=1)

        # assert
        assert next_receiving_number == 2
