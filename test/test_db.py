import unittest
import os

from app.models import base
from app.models import todo
from conf import config


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base.init_db(driver=config.db_driver, db_name=config.db_test_name)

    @classmethod
    def tearDownClass(cls):
        os.remove(config.db_test_name)

    def setUp(self):
        self.TIME_FORMAT = '%Y%m%d%H%M%S'
        self.contents = 'unittest'
        self.priority = '高'

    def tearDown(self):
        base.Session.remove()

    def test_create_get(self):
        """Data create test
        1. create data at wrong timestamp
           -> return False
        2. create data at same timestamp for two times
           <1> create data
               -> return True, one data
           <2> create data at same timestamp
               -> return False(IntegrityError)
        3. get data at it's timestamp

        <Caution!!>
        If one data is created at any timestamp,
        after any data is got at the same timestamp,
        'FlushError' is occured, not IntegrityError.
        you have to call to 'Session.remove()', before created.
        """
        # 1. create at wrong timestamp
        wrong_timestamp = '2020h101000000'
        r = todo.Todo.create(timestamp=wrong_timestamp,
                             contents=self.contents,
                             priority=self.priority)
        self.assertEqual(r, False)

        # 2-<1>. create at correct timestamp
        correct_timestamp = '20200101000000'
        r = todo.Todo.create(timestamp=correct_timestamp,
                             contents=self.contents,
                             priority=self.priority)
        self.assertEqual(r, True)

        # 2-<2>. create at same timestamp
        r = todo.Todo.create(timestamp=correct_timestamp,
                             contents=self.contents,
                             priority=self.priority)
        self.assertEqual(r, False)

        # 3. data get
        todo_data = todo.Todo.get(timestamp=correct_timestamp)
        value = todo_data.values
        self.assertEqual(value['timestamp'], correct_timestamp)
        self.assertEqual(value['contents'], self.contents)
        self.assertEqual(value['priority'], self.priority)

    def test_update(self):
        """Data update test
        1. update data at wrong timestamp
           -> return False
        2. update data at correct timestamp
           <1> create data at crrect timestamp
               -> return True
           <2> update data for it's timestamp
               -> return True
           <3> get updated data
               -> return updated data
           <3> update data for bad timestamp
               -> return False
        """
        # 1. update wrong timestamp
        wrong_timestamp = '2020h101000000'
        r = todo.Todo.update(timestamp=wrong_timestamp,
                             contents=self.contents,
                             priority=self.priority)
        self.assertEqual(r, False)

        # 2-<1>. create correct timestamp
        correct_timestamp = '20200102000000'
        r = todo.Todo.create(timestamp=correct_timestamp,
                             contents=self.contents,
                             priority=self.priority)
        self.assertEqual(r, True)

        # 3-<2>. update at correct timestamp
        r = todo.Todo.update(timestamp=correct_timestamp,
                             contents='unittest_update',
                             priority='低')
        self.assertEqual(r, True)

        # 3-<3>. get updated data
        todo_data = todo.Todo.get(timestamp=correct_timestamp)
        value = todo_data.values
        self.assertEqual(value['timestamp'], correct_timestamp)
        self.assertEqual(value['contents'], 'unittest_update')
        self.assertEqual(value['priority'], '低')

        # 3-<4>. update at bad timestamp
        bad_timestamp = '20200102000001'
        r = todo.Todo.update(timestamp=bad_timestamp,
                             contents=self.contents,
                             priority=self.priority)
        self.assertEqual(r, False)

    def test_delete(self):
        """Data delete test
        1. delete at wrong timestamp
           -> return False
        2. create at correct timestamp
           -> return True
        3. delete at bad timestamp
           -> return False
        4. delete correct timestamp
           -> return True
        5. get data at correct timestamp
           -> None
        """
        # 1. delete at wrong timestamp
        wrong_timestamp = '2020h101000000'
        r = todo.Todo.delete(timestamp=wrong_timestamp)
        self.assertEqual(r, False)

        # 2. create at correct timestamp
        correct_timestamp = '20200103000000'
        r = todo.Todo.create(timestamp=correct_timestamp,
                             contents=self.contents,
                             priority=self.priority)
        self.assertEqual(r, True)

        # 3. delete at bad timestamp
        bad_timestamp = '20200103000001'
        r = todo.Todo.delete(timestamp=bad_timestamp)
        self.assertEqual(r, False)

        # 4. delete at correct timestamp
        r = todo.Todo.delete(timestamp=correct_timestamp)
        self.assertEqual(r, True)

        # 5. get data at correct timestamp
        todo_data = todo.Todo.get(timestamp=correct_timestamp)
        self.assertIsNone(todo_data)
