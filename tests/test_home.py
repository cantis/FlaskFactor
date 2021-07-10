import pytest

from web import create_app, db
from config import TestConfig


@pytest.fixture(scope='session')
def app():
    ''' Application Ficture '''
    app = create_app()
    config = TestConfig()
    app.config.from_object(config)
    return app


@pytest.fixture(scope='function')
def client(app):
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
