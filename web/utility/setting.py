''' Save settings to the setting table and make them available to the application
    supports caching settings '''
from flask import session

from web import db
from web.models import Setting


def get_setting(party_id: int, setting_name: str, default='none') -> str:
    ''' Get the get a setting from cache or database '''

    # Try to get the setting from the cache
    if session.get(setting_name):
        return session[setting_name]

    # Try to get the setting from the database
    setting = Setting.query.filter_by(party_id=party_id, name=setting_name).first()

    # found it in the database
    if setting:
        session[setting_name] = setting.value
        return setting.value

    # not found, return the default value
    if not setting and default != 'none':
        return default

    # not found and no default, return None
    if not setting and default == 'none':
        return None


def save_setting(party_id: int, setting_name: str, value: str) -> None:
    ''' Add or update a setting to the cache and database '''
    setting = Setting.query.filter_by(party_id=party_id, name=setting_name).first()
    if not setting:
        setting = Setting(
            party_id=party_id,
            name=setting_name,
            value=value
        )
        db.session.add(setting)
    else:
        setting.value = value
    db.session.commit()
    session[setting_name] = value


def save_common_setting(setting_name: str, value: str) -> None:
    ''' Add or update a setting to the common cache and database'''
    common_party_id = 0
    save_setting(common_party_id, setting_name, value)


def get_common_setting(setting_name: str, default='none') -> str:
    ''' Get the get a setting from the common cache or database '''
    common_party_id = 0
    return get_setting(common_party_id, setting_name, default)


def clear_setting_cache() -> None:
    ''' Clear the setting cache. '''
    for key in session.keys():
        session.pop(key)
