import unittest
from datetime import datetime
from departments_app import create_app, db
from departments_app.models.department import Department


class DepartmentModelTestCase(unittest.TestCase):

    def setUp(self):
        """ Prepare test fixture, create application"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_departments(self):
        d1 = Department(name="Department_1", long_name="Test department long name No 1")
        d2 = Department(name="Department_2", long_name="Test department long name No 2")
        db.session.add(d1)
        db.session.add(d2)
        db.session.commit()
        #
        # assert d1 in db.session
        # assert d2 in db.session
        #
        # self.assertEqual(d1.name, "Department_1")
        # self.assertEqual(d2.name, "Department_2")
        #
        # self.assertEqual(d1.long_name, "Test department long name No 1")
        # self.assertEqual(d2.long_name, "Test department long name No 2")
        #
        # self.assertNotEqual(d1.uuid, d2.uuid)
        #
        # self.assertTrue(hasattr(d1, "uuid"))
        # self.assertTrue(hasattr(d1, "name"))
        # self.assertTrue(hasattr(d1, "long_name"))
        # self.assertTrue(hasattr(d1, "id"))
        #
        # # __repr__ test
        # # Production(Production)[e9a48f4f - 3002 - 4
        # # f37 - abe9 - 41e50
        # # ea7be6f]
        # # repr()
        r = repr(d1)
        self.assertEqual(f"{d1.name} ({d1.long_name}) [{d1.uuid}]", r)


if __name__ == '__main__':
    unittest.main()
