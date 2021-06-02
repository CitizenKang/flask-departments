import unittest
from datetime import datetime
from departments_app import create_app, db
from departments_app.models.department import Department
from departments_app.models.employee import Employee


class ModelsTestCase(unittest.TestCase):

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
        self.assertEqual(d1.__repr__(), f"[{d1.uuid}] {d1.name}")

        Department.delete(d1)
        Department.delete(d2)

        self.assertNotIn(d1, db.session)
        self.assertNotIn(d2, db.session)

    def test_employees(self):
        d1 = Department(name="Test_name_1")
        Department.create(d1)

        e1 = Employee(first_name="John",
                      last_name="Doe",
                      date_of_birth=datetime(1990, 11, 10),
                      phone_number="0970000000",
                      email="JohnDoe@gmail.com",
                      salary=1000.00,
                      department_id=1)

        e2 = Employee(first_name="Jane",
                      last_name="Does",
                      date_of_birth=datetime(1970, 10, 5),
                      phone_number="0970000000",
                      email="JohnDoe@gmail.com",
                      salary=2000.00,
                      department_id=1)
        Employee.create(e1)
        Employee.create(e2)

        self.assertIn(e1, db.session)
        self.assertIn(e2, db.session)

        self.assertEqual(e1.__repr__(), f"[{e1.uuid}] {e1.first_name} {e1.last_name}, D.O.B.: {e1.date_of_birth}")
        self.assertEqual(e2.__repr__(), f"[{e2.uuid}] {e2.first_name} {e2.last_name}, D.O.B.: {e2.date_of_birth}")

        Employee.delete(e1)
        Employee.delete(e2)

        self.assertNotIn(e1, db.session)
        self.assertNotIn(e2, db.session)


if __name__ == '__main__':
    unittest.main()
