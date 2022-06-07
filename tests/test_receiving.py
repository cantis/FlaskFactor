""" Tests for receiving """
import pytest

from config import TestConfig
from web import create_app, db
from web.models import Party, Receiving, Item_Type
from web.routes.receiving import next_receiving_id
from web.utility.setting import save_common_setting


# Test Fixtures
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

        db.session.add(Item_Type(id='1', item_type='Melee'))

        db.session.add(Party(
            party_name='Adventure Inc.',
            is_active=True
            )
        )

        db.session.commit()

        yield client
        db.drop_all()


# Base Route Tests
def test_navigate_to_receiving_list(client):
    # arrange

    with client.application.test_request_context():
        # act
        response = client.get('/receiving')

        # assert
        assert response.status_code == 200
        assert b'Receiving - Item List' in response.data


def test_navigate_to_receiving_add(client):
    # arrange

    with client.application.test_request_context():
        # act
        response = client.get('/receiving/add')

        # assert
        assert response.status_code == 200
        assert b'Receiving - Add Item' in response.data


def test_navigate_to_receiving_edit(client):
    # arrange
    db.session.add(Receiving(
            receipt_id=1,
            session_id=1,
            party_id=1,
            Item_Type_id='1',
            quantity=4,
            isCommitted=False,
            item='Short Sword',
            purchase_price=10.00
        ))
    db.session.commit()

    with client.application.test_request_context():
        # act
        response = client.get('/receiving/edit/1')

        # assert
        assert response.status_code == 200
        assert b'Receiving - Edit Item' in response.data


# Add Item Tests
def test_add_receiving_item_valid_data_ok(client):
    # arrange
    with client.application.test_request_context():
        save_common_setting(setting_name='current_party', value='1')

        # act
        response = client.post('/receiving/add', data={
            'session': 1,
            'item_name': 'Short Sword',
            'item_type_id': 1,
            'quantity': 4,
            'value': 10.00,
            'saleValue': 10.00,
            'add_another': True
        }
        )
        # assert
        assert response.status_code == 200


def test_add_receiving_item_invalid_data_fails(client):
    pass


def test_add_receiving_item_with_no_party_fails(client):
    # arrange

    with client.application.test_request_context():
        # act
        response = client.post('/receiving/add', data={
            'session': 1,
            'item_name': 'Short Sword',
            'type': 'Melee',
            'quantity': 4,
            'value': 10.00,
            'saleValue': 10.00,
            'add_another': True
        }
        )
        # assert
        assert response.status_code == 200
        assert b'Please select a party' in response.data

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
            Item_Type_id='1',
            quantity=4,
            isCommitted=False,
            item='Short Sword',
            purchase_price=10.00
        ))
        db.session.commit()

        # act
        next_receiving_number = next_receiving_id(selected_party_id=1)

        # assert
        assert next_receiving_number == 2
