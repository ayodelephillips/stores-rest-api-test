from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):

    def setUp(self):
        super(ItemTest, self).setUp()  # use the previous set up method defined in BaseTest
        with self.app() as client:
            with self.app_context():
                UserModel('test','1234').save_to_db()
                auth_request = client.post('/auth',
                                         data=json.dumps({'username': 'test', 'password': '1234'}),
                                         headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'  # flask jwt reerquires the string is in this format

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)  # no authorization header is found for this

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})  # pass in the authorization header when making the request
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        """ get item when there is authorisation """
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('/item/test', headers={'Authorization': self.access_token})  # pass in the authorization header when making the request
                self.assertEqual(resp.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.delete('/item/test')  # authorization header is not needed here because there's no  '@jwt_required()' on top of delete in item resources
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test', data={'price': 19.99, 'store_id': 1})  
                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.post('/item/test', data={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'test' already exists."}, json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', data={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(resp.data))

    def test_put_update_item(self):
        """ put an item when the item already exists """
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()
                resp = client.put('/item/test', data={'price': 19.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 19.99}]}, json.loads(resp.data))
   