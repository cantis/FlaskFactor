''' Save settings to the setting table and make them available to the application
    supports caching settings '''
from flask import session

from src import db
from src.models import Setting


def get_setting(setting_name, default='none'):
    ''' Get the get a setting from cache or database '''

    # Try to get the setting from the cache
    if session.get(setting_name):
        return session[setting_name]

    # Try to get the setting from the database
    setting = Setting.query.filter_by(name=setting_name).first()

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


def save_setting(setting_name, value):
    ''' Add or update a setting to the cache and database '''
    setting = Setting.query.filter_by(name=setting_name).first()
    if not setting:
        setting = Setting(
            name=setting_name,
            value=value
        )
        db.session.add(setting)
    else:
        setting.value = value
    db.session.commit()
    session[setting_name] = value


def clear_setting_cache():
    ''' Clear the setting cache. '''
    for key in session.keys():
        session.pop(key)
