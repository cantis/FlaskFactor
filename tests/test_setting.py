""" Tests for setting utility """
import pytest

from config import TestConfig
from src import create_app, db
from src.models import Setting
from src.utility.setting import get_setting, save_setting


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

        # Add settings
        db.session.add(Setting(id=1, name='test_session', value='1'))
        db.session.commit()

        yield client
        db.drop_all()


def test_get_setting(client):
    # arrange

    # act
    with client.application.test_request_context('/'):
        result = get_setting('test_session')

        # assert
        assert result == '1'


def test_save_setting(client):
    # arrange

    # act
    with client.application.test_request_context('/'):
        save_setting('warp_flux', '21')

    # assert
    result = Setting.query.filter_by(name='warp_flux').first()
    assert result.value == '21'


def test_update_setting(client):
    # arrange
    with client.application.test_request_context('/'):
        save_setting('third_setting', 'Alpha')

    # act
        save_setting('third_setting', 'Beta')

    # assert
        assert get_setting('third_setting') == 'Beta'


def test_get_a_setting_default(client):
    """ Test that we can get a default value for a setting """
    # arrange

    # act
    with client.application.test_request_context('/'):
        result = get_setting('warp_factor', '4')

    # assert
        assert result == '4'
