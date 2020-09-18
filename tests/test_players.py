import unittest

from app import create_app


class TestPlayerMethods(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config['TESTING']
        self.app = app.test_client()

    # def login(self, user_id, password):
    #     return self.app.post(
    #         '/login',
    #         data=dict(user_id=user_id, password=password),
    #         follow_redirects=True
    #     )

    def test_get_player_list_login_redirect(self):
        # arrange

        # act
        response = self.app.get('http://localhost:5000/player')

        # assert
        self.assertEqual(response.status_code, 302)

    def test_get_player_list(self):
        # arrange
        self.login(user_id='cantis@gmail.com', password='password')

        # act
        response = self.app.get('http://localhost:5000/player')

        # assert
        self.assertEqual(response.status_code, 200)
