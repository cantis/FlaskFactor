import unittest

from flask.globals import request


from tests.test_base import TestBase
from app.models import db
from app.models.user import User
# from app.models.player import Player
from app.routes.users import LoginForm, hash_password


class TestUserLogin(unittest.TestCase):

    # See: https://stackoverflow.com/questions/37579411/testing-a-post-that-uses-flask-wtf-validate-on-submit

    TESTUSER = 'noplace@comeplace.com'
    TESTPASS = 'password'
    user = User(
        user_id=TESTUSER,
        firstname='test',
        lastname='user',
        password=hash_password(TESTPASS)
        )
    # player = Player(
    #     firstname='Evan',
    #     lastname='Young',
    #     is_active='True',
    # )

    def setUp(self):
        self.app = TestBase.create_test_app()
        self.client = self.app.test_client()
        self.context = self.app.test_request_context()
        self.context.push()

        db.session.add(self.user)
        # db.session.add(self.player)
        db.session.commit()

    def tearDown(self):
        pass

    def request(self, *args, **kwargs):
        return self.app.test_request_context(*args, **kwargs)

    def test_users_can_login(self):
        # arrange
        with self.request(method='POST', data={'user_id': self.TESTUSER, 'password': self.TESTPASS, 'remember_me': False}):
            # act
            form = LoginForm(request.form, csrf_enabled = False)
            response = self.client.post('/login', data=form.data, follow_redirects=False)
            #assert
            self.assertEqual(response.status_code, 302)
    
    def test_login_valid_OK(self):
        #arrange
        with self.request(method='POST', data={'user_id': self.TESTUSER, 'password': self.TESTPASS, 'remember_me': False}):
            # act
            form = LoginForm(request.form, csrf_enabled = False)
            # assert
            self.assertTrue(form.validate_on_submit())

    def test_login_datamissing_fail(self):
        # arrange
        with self.request(method='POST', data={'user_id': self.TESTUSER, 'password': None, 'remember_me': False}):
            # act
            form = LoginForm(request.form, csrf_enabled = False)
            # assert
            self.assertFalse(form.validate_on_submit())

    # def test_login_correct_form(self):
    #     response = self.client.get('/login', content_type='html/text')
    #     self.assertTrue(b'Factor - Login' in response.data)

    # def test_userlist_form(self):
    #     login_user(self.user, remember=False)
    #     response = self.client.get('/user/profile/1', content_type='html/text')
    #     self.assertTrue(b'User - Edit' in response.data)

    # def test_payer_list_correct_form(self):
    #     self.user.is_active = True
    #     login_user(self.user, remember=False)
    #     print(current_user.firstname)

    #     response = self.client.get('/player', content_type='html/text')
    #     self.assertTrue(b'Players' in response.data)

        
            
