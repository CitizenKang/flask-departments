import unittest
import uuid
from datetime import datetime
from departments_app import create_app, db
from departments_app.service.services import DepartmentService
from departments_app.models.department import Department
from departments_app.models.employee import Employee


class EmployeesResourceTestCase(unittest.TestCase):

    def setUp(self):
        """ Prepare test fixture, create application"""
        self.app = create_app('development')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # adding departments
        self.test_department_1 = Department(name="TestDepartment1")
        self.test_department_2 = Department(name="TestDepartment2")
        # adding employee
        self.test_employee1 = Employee(first_name="testJohn",
                                       last_name="testDoe",
                                       date_of_birth=datetime(1990, 10, 10),
                                       phone_number="0970000000",
                                       email="test@gmail.com",
                                       salary=1000.00,
                                       department_id=1)
        self.test_employee2 = Employee(first_name="testJohn",
                                       last_name="testDoe",
                                       date_of_birth=datetime(1990, 10, 10),
                                       phone_number="0970000000",
                                       email="test@gmail.com",
                                       salary=1000.00,
                                       department_id=1)
        db.session.add_all([self.test_department_1, self.test_department_2, self.test_employee1, self.test_employee2])
        db.session.commit()
        self.service = DepartmentService()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_fetch_one_departments_returns_data(self):
        department = Department.query.filter_by(name="TestDepartment1").one()
        fetched_data = self.service.fetch_one(department.uuid)
        self.assertIsInstance(fetched_data, dict)
        self.assertEqual(department.uuid, fetched_data['uuid'])
        self.assertEqual(department.name, fetched_data['name'])

    def test_fetch_one_departments_returns_none(self):
        fetched_data = self.service.fetch_one(str(uuid.uuid4()))
        self.assertIsNotNone(fetched_data)


if __name__ == '__main__':
    unittest.main()
