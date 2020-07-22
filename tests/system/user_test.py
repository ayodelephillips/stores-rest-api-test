from models.user import UserModel
from tests.base_test import BaseTest
import json


class userTest(BaseTest):
    def test_register_user(self):
        """ test that we can register the user """
        with self.app() as client:  # client which we use for testing. simulates the testing so it looks like a user making certain requests to the api
            with self.app_context():  # helps us save things to db
                response = client.post('/register', data={'username': 'test', 'password': '1234'})  # test client allows for testing with the specified url.  self.app_context allows for saving. the data sent is sent in the form format. the userregister model is added as a resource in app.py, so we can do client.post
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully'},
                                     json.loads(response.data))  # converts the returned json into a python dictionary
    
    def test_register_and_login(self):
        """ test that the user can log in """
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                auth_response = client.post('/auth', data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})  # /auth endpoint needs to be used with json format. Content-Type tells server what kind of data is being sent
                self.assertIn('access_token', json.loads(auth_response.data).keys())  # asserts that 'access_token' key is in the response
    
    def test_register_duplicate_user(self):
        """ test that when trying to register with an already existing username, it doesn't go through """
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'},
                                     json.loads(response.data))

