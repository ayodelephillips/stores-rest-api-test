from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test', 'abcd')

            self.assertIsNone(UserModel.find_by_username('test'), 'The username {} is found, even though not saved to the db'.format('test'))
            self.assertIsNone(UserModel.find_by_id(1), 'The user with id {} is found, even though not yet saved to the db'.format(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('test'), 'The username {} is not found, even though  saved to the db'.format('test'))
            self.assertIsNotNone(UserModel.find_by_id(1), 'The user with id {} is not found, even though saved to the db'.format(1))
            
    def test_read(self):
        pass    
