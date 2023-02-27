""" Tests for setting utility """
import pytest

from src import db
from src.models import Setting
from src.utility.setting import get_setting, save_setting


@pytest.fixture(scope='function')
def dbclient(app):
    '''fixture with some settings in the database'''
    with app.app_context():
        client = app.test_client()
        db.create_all()

        # Add settings
        db.session.add(Setting(id=1, name='test_session', value='1'))
        db.session.commit()

        yield client
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    '''fixture with empty database'''
    with app.app_context():
        client = app.test_client()
        yield client


def test_get_setting(dbclient):
    # arrange


    # act
    with dbclient.application.test_request_context('/'):
        result = get_setting('test_session')

        # assert
        assert result == '1'


def test_save_setting(dbclient):
    # arrange

    # act
    with dbclient.application.test_request_context('/'):
        save_setting('warp_flux', '21')

    # assert
    result = Setting.query.filter_by(name='warp_flux').first()
    assert result.value == '21'


def test_update_setting(dbclient):
    # arrange
    with dbclient.application.test_request_context('/'):
        save_setting('third_setting', 'Alpha')

    # act
        save_setting('third_setting', 'Beta')

    # assert
        assert get_setting('third_setting') == 'Beta'


def test_get_a_setting_default(dbclient):
    """ Test that we can get a default value for a setting """
    # arrange

    # act
    with dbclient.application.test_request_context('/'):
        result = get_setting('warp_factor', '4')

    # assert
        assert result == '4'
