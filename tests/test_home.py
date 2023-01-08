import pytest

from src import create_app, db
from config import TestConfig
from src.models import Party, Setting


@pytest.fixture(scope='session')
def app():
    ''' Application Ficture '''
    app = create_app()
    config = TestConfig()
    app.config.from_object(config)
    return app


@pytest.fixture(scope='function')
def client(app):
    ''' Fixture with sample data '''
    with app.app_context():
        client = app.test_client()
        db.create_all()

        db.session.add(Party(party_name='Adventure Inc.', is_active=True))
        db.session.add(Party(party_name='Dragon Company', is_active=True))
        db.session.commit()

        yield client
        db.drop_all()


@pytest.fixture(scope='function')
def empty_client(app):
    ''' Empty Fixture '''
    with app.app_context():
        empty_client = app.test_client()
        db.create_all()

        yield empty_client
        db.drop_all()


def test_navigate_to_home(client):
    # arrange

    # act
    result = client.get('/', follow_redirects=True)

    # assert
    assert b'Welcome to the Factor Program<' in result.data


def test_nav_select_party(client):
    # arrange

    # act
    page_result = client.get('/nav_select_party/2', follow_redirects=True)

    # assert
    setting_result = Setting.query.filter_by(name='current_party').first()
    assert setting_result.value == '2'
    assert b'Current Party: Dragon Company' in page_result.data
    assert b'Current Party: Adventure Inc.' not in page_result.data
