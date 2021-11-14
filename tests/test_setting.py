""" Tests for setting utility """
import pytest

from config import TestConfig
from web import create_app, db
from web.models import Setting, Party
from web.utility.setting import get_setting, save_setting, save_common_setting, get_common_setting


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

        db.session.add(Party(id=0, party_name='<common>', is_active=False))
        db.session.add(Party(id=1, party_name='Adventure Inc.', is_active=True))
        db.session.add(Party(id=2, party_name='International Rescue', is_active=True))
        db.session.add(Setting(id=1, party_id=1, name='test_session', value='1'))
        db.session.commit()

        yield client
        db.drop_all()


def test_get_setting(client):
    """ Test that we can get a setting """
    # arrange

    # act
    with client.application.test_request_context('/'):
        result = get_setting(party_id=1, setting_name='test_session')

        # assert
        assert result == '1'


def test_save_setting(client):
    """ Test that we can save a setting """
    # arrange

    # act
    with client.application.test_request_context('/'):
        save_setting(party_id=1, setting_name='warp_flux', value='21')

    # assert
    result = Setting.query.filter_by(party_id=1, name='warp_flux').first()
    assert result.value == '21'


def test_update_setting(client):
    """ Test that we can update a setting """
    # arrange
    with client.application.test_request_context('/'):
        save_setting(party_id=1, setting_name='third_setting', value='Alpha')

    # act
        save_setting(party_id=1, setting_name='third_setting', value='Beta')

    # assert
        assert get_setting(party_id=1, setting_name='third_setting') == 'Beta'


def test_get_a_setting_not_found_default(client):
    """ Test that we can get a default value for a setting """
    # arrange

    # act
    with client.application.test_request_context('/'):
        result = get_setting(party_id=1, setting_name='warp_factor', default='4')

    # assert
        assert result == '4'


def test_get_setting_not_found_no_default(client):
    """ Test that we can get a default value for a setting """
    # arrange

    # act
    with client.application.test_request_context('/'):
        result = get_setting(party_id=1, setting_name='not found')

    # assert
        assert result is None


def test_get_correct_party_setting(client):
    """ Test that we can get a setting for a specific party """
    with client.application.test_request_context('/'):
        # arrange
        save_setting(party_id=1, setting_name='third_setting', value='Alpha')
        save_setting(party_id=2, setting_name='third_setting', value='Beta')

        # act
        result = get_setting(party_id=2, setting_name='third_setting')

        # assert
        assert result == 'Beta'


def test_update_correct_party_setting(client):
    """ Test that we can update a setting for a specific party """
    with client.application.test_request_context('/'):
        # arrange
        save_setting(party_id=1, setting_name='third_setting', value='Alpha')
        save_setting(party_id=2, setting_name='third_setting', value='Beta')

        # act
        save_setting(party_id=2, setting_name='third_setting', value='Gamma')

        # assert
        assert get_setting(party_id=2, setting_name='third_setting') == 'Gamma'


def test_save_common_setting(client):
    """ Test that we can save a setting """
    # arrange

    # act
    with client.application.test_request_context('/'):
        save_common_setting(setting_name='warp_flux', value='21')

    # assert
    result = Setting.query.filter_by(party_id=0, name='warp_flux').first()
    assert result.value == '21'


def test_get_common_setting(client):
    """ Test that we can get a shared  setting """
    # arrange
    db.session.add(Setting(party_id=0, name='theme', value='dark'))
    db.session.commit()
    # act
    with client.application.test_request_context('/'):
        result = get_common_setting(setting_name='theme')

    # assert
        assert result == 'dark'
