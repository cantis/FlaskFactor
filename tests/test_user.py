import unittest
from werkzeug.security import check_password_hash

from app import create_app
from app.routes.users import hash_password
from app.models.user import User


class TestUserMethods(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING']

    def test_user_add_form_display(self):
        client = self.app.test_client(self)
        response = client.get('/user/add', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_form_display(self):
        client = self.app.test_client(self)
        response = client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_form_shown_correct(self):
        client = self.app.test_client(self)
        response = client.get('/login', content_type='html/text')
        self.assertTrue(b'Factor - Login' in response.data)

    def test_login_form_login(self, app):
        with app.test_client(self) as client:
            user = User(user_id='cantis@gmail.com', password='password')
            form = app.route.users.LoginForm(formdata=None, obj=user)
            with client.session_transaction() as sess:
                sess['user_id'] = 'cantis@gmail.com'
                sess['password'] = 'password'
                response = client.post('/login', data=form.data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_hash_password_password_hashed(self):
        # arrange

        # act
        hashed_password = hash_password('ThisIsATest')

        # assert
        self.assertTrue(len(hashed_password) > 0, 'hashed password zero lengh')

    def test_hash_password_expected_hash(self):
        # arrange
        hashed_password = hash_password('ThisIsATest')

        # act
        result = check_password_hash(hashed_password, 'ThisIsATest')

        # assert
        self.assertTrue(result, 'Hash as expected')

    def test_hash_password_bad_password(self):
        # arrange
        hashed_password = hash_password('ThisIsATest')

        # act
        result = check_password_hash(hashed_password, 'BadPassword')

        # assert
        self.assertFalse(result, 'Check should have failed.')
