import unittest

from werkzeug.security import check_password_hash

from app.users.users import hash_password


class TestUserMethods(unittest.TestCase):

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
