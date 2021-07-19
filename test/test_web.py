import unittest
from unittest.mock import patch
import time
import os

from app.controllers import web
from app.models import base
from conf import config


class TestWebserver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base.init_db(driver=config.db_driver, db_name=config.db_test_name)

    @classmethod
    def tearDownClass(cls):
        os.remove(config.db_test_name)

    def setUp(self):
        self.TIME_FORMAT = '%Y%m%d%H%M%S'
        self.timestamp = ''
        self.contents = 'unittest'
        self.priority = '低'
        self.updated_contents = 'unittest_update'
        self.updated_priority = '高'

    def test_todo_api(self):
        with web.app.test_client() as client:
            """todo_api test
            1. Test each CURD methods
               <1> access on GET method(first)
                   -> return None([])
               <2> access on POST method
                   -> return timestamp(year, month, day, hour, minute, second)
               <3> access on GET method(second)
                   -> return list of created json and timestamp.
               <4> access on PUT method
                   -> return return successfull message
               <5> access on GET method(third)
                   -> return list of updated json and timestamp
               <6> access on DELETE method
                   -> return successfull message
               <7> access on GET method(last)
                   -> return None([])
            2. Error Test
               <1> wrong timestamp test:
                   access to database on self.created_json at wrong timestamp,
                   each return error messages,
                   because there is not a 'second' part string in the timestamp
               <2> POST error test:
                   two times, resister data at correct timestamp.
                   one time returns the timestamp, two times return error message,
                   because of trying to resister it at the same timestamp
               <3> PUT error test:
                   try to update data at no timestamp in database.
                   return error message
               <4> DELETE error test:
                   try to delete data at bad timestamp,
                   return error message
            """
            # 1-<1> first GET
            todo_list = client.get('/todo').get_json()
            self.assertEqual(todo_list['todo'], [])

            # 1-<2> POST
            # timestamp has temporarily saved
            self.timestamp = time.strftime(self.TIME_FORMAT)
            json = {'contents': self.contents, 'priority': self.priority}

            res_post = client.post('/todo', json=json).get_json()
            self.assertEqual(res_post['timestamp'], self.timestamp)

            # 1-<3> second GET
            todo_list = client.get('/todo').get_json()
            for todo in todo_list['todo']:
                self.assertEqual(todo['contents'], self.contents)
                self.assertEqual(todo['priority'], self.priority)
                self.assertEqual(todo['timestamp'], self.timestamp)

            # 1-<4> PUT
            json = {
                'timestamp': self.timestamp, 'contents': self.updated_contents,
                'priority': self.updated_priority}

            res_put = client.put('/todo', json=json).get_json()
            self.assertEqual(res_put['message'], 'Update complete')

            # 1-<5> third GET
            todo_list = client.get('/todo').get_json()
            for todo in todo_list['todo']:
                self.assertEqual(todo['contents'], self.updated_contents)
                self.assertEqual(todo['priority'], self.updated_priority)
                self.assertEqual(todo['timestamp'], self.timestamp)

            # 1-<6> DELETE
            json = {'timestamp': self.timestamp}

            res_delete = client.delete('/todo', json=json).get_json()
            self.assertEqual(res_delete['message'], 'Delete complete')

            # 1-<7> last GET
            todo_list = client.get('/todo').get_json()
            self.assertEqual(todo_list['todo'], [])

            with patch('app.controllers.web.time.strftime') as mock_strftime:
                # 2-<1> wrong timestamp test(no second)
                wrong_timestamp = '202001010000'
                self.timestamp = wrong_timestamp

                # mock set
                mock_strftime.return_value = self.timestamp

                post_json = {
                    'contents': self.contents, 'priority': self.priority}
                put_json = {
                    'timestamp': self.timestamp, 'contents': self.updated_contents,
                    'priority': self.updated_priority}
                delete_json = {'timestamp': self.timestamp}

                res_post = client.post('/todo', json=post_json).get_json()
                res_put = client.put('/todo', json=put_json).get_json()
                res_delete = client.delete('/todo', json=delete_json).get_json()

                self.assertEqual(res_post['error'], 'Data Created Error!!')
                self.assertEqual(res_put['error'], 'Updata error')
                self.assertEqual(res_delete['error'], 'Delete error')

                # 2-<2> POST error test(create data at same timestamp, two times)
                correct_timestamp = '20200101000000'
                self.timestamp = correct_timestamp

                # mock set
                mock_strftime.return_value = self.timestamp

                post_json = {
                    'contents': self.contents, 'priority': self.priority}

                # one time
                res_post = client.post('/todo', json=post_json).get_json()
                self.assertEqual(res_post['timestamp'], self.timestamp)

                # two times(error)
                res_post = client.post('/todo', json=post_json).get_json()
                self.assertEqual(res_post['error'], 'Data Created Error!!')

                # 2-<3> PUT error test(update data at no timestamp in database)
                bad_timestamp = '20200101000001'
                self.timestamp = bad_timestamp

                put_json = {
                    'timestamp': self.timestamp, 'contents': self.updated_contents,
                    'priority': self.updated_priority}
                res_put = client.put('/todo', json=put_json).get_json()

                self.assertEqual(res_put['error'], 'Updata error')

                # 2-<4> DELETE error test(delete data at no timestamp in database)
                delete_json = {'timestamp': self.timestamp}

                res_delete = client.delete('/todo', json=delete_json).get_json()
                self.assertEqual(res_delete['error'], 'Delete error')
