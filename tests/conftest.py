import os
import pytest

from src import create_app


@pytest.fixture(scope='session')
def app():
    '''Shared app fixture for the entire test session.'''
    os.environ['ENV'] = 'test'
    app = create_app()
    yield app
