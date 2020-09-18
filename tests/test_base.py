from flask.ext.testing import TestCase

from app import create_app
from app.models.user import db


class BaseTestCase(TestCase):
    """ A base test case for Factor """ 

    