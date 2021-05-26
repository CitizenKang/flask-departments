import unittest
from datetime import datetime
from departments_app import create_app, db
from departments_app.models.department import Department
from departments_app.models.employee import Employee

EMPLOYEE = {"first_name": 'JohnAsz',
            "last_name": 'Doe',
            "date_of_birth": "1990-01-01",
            "phone_number": "0970000000",
            "email": "john_doe@gmail.com",
            "salary": 1000.00}

DEPARTMENT = {"name": "TestDepartment"}


class DepartmentModelTestCase(unittest.TestCase):

    def setUp(self):
        """ Prepare test fixture, create application"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.employee = Employee(**EMPLOYEE)

        self.department_record = Department(**DEPARTMENT).create()  # Create department record for relationship

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_data(self):
        self.assertEqual(self.employee.first_name, EMPLOYEE.get("first_name"))
        self.assertEqual(self.employee.last_name, EMPLOYEE.get("last_name"))
        self.assertEqual(self.employee.date_of_birth, EMPLOYEE.get("date_of_birth"))
        self.assertEqual(self.employee.phone_number, EMPLOYEE.get("phone_number"))
        self.assertEqual(self.employee.email, EMPLOYEE.get("email"))
        self.assertEqual(self.employee.salary, EMPLOYEE.get("salary"))

    def test_repr_method(self):
        self.assertEqual(self.employee.__repr__(),
                         f"[{self.employee.uuid}] {self.employee.first_name} {self.employee.last_name},"
                         f" D.O.B.: {self.employee.date_of_birth}")

    def test_uuid_created(self):
        self.assertIsNotNone(self.employee.uuid)

    def test_create_method(self):
        self.employee.department_id = self.department_record.id
        self.department_record.create()

    def test_getbyid_method(self):
        self.employee.department_id = self.department_record.id
        self.department_record.create()
        uuid = self.employee.uuid
        query_record = Employee.get_by_uuid(uuid)
        # self.assertIsNotNone(query_record)
        self.assertEqual(query_record.first_name, self.employee.first_name)


if __name__ == '__main__':
    unittest.main()
