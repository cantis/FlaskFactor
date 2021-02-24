# import pytest

# from flask.globals import request
# from tests.test_base import TestBase
# from app.models import db
# from app.models.player import Player


# class TestPlayerMethods(unittest.TestCase):

#     def setUp(self):
#         self.app = TestBase.create_test_app()
#         self.client = self.app.test_client()
#         self.context = self.app.test_request_context()
#         self.context.push()

#         player = Player(
#             firstname='Evan',
#             lastname='Young',
#             is_active='True',
#             )
#         db.session.add(self.player)
#         db.session.commit

#     def tearDown(self):
#         pass

#     def test_get_player_list(self):
#         # arrange

#         # act
#         response = self.client.get('http://localhost:5000/player')

#         # assert
#         self.assertEqual(response.status_code, 200)
