import unittest
from datetime import datetime
from departments_app import create_app, db
from departments_app.models.department import Department
from departments_app.models.employee import Employee


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
        d1 = Department(name="Test_name_1")
        d2 = Department(name="Test_name_2")

        Department.create(d1)
        Department.create(d2)

        self.assertIn(d1, db.session)
        self.assertIn(d2, db.session)

        Department.delete(d1)
        Department.delete(d2)

        self.assertNotIn(d1, db.session)
        self.assertNotIn(d2, db.session)


if __name__ == '__main__':
    unittest.main()
