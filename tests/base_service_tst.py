import unittest
from datetime import datetime
from departments_app import create_app, db
from departments_app.service.services import DepartmentService, EmployeeService
from departments_app.models.department import Department
from departments_app.models.employee import Employee


class BaseServiceTestCase(unittest.TestCase):
    """
    Contains set up and teardown methods for service test modules
    """

    def setUp(self):
        """ Prepare test fixture, create application"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # adding departments
        self.test_department_1 = Department(name="TestDepartment1")
        self.test_department_2 = Department(name="TestDepartment2")
        # adding employee
        self.test_employee1 = Employee(first_name="John",
                                       last_name="Doe",
                                       date_of_birth=datetime(1990, 10, 10),
                                       phone_number="0970000000",
                                       email="JohnDoe@gmail.com",
                                       salary=1000.00,
                                       department_id=1)
        self.test_employee2 = Employee(first_name="Jane",
                                       last_name="Doe",
                                       date_of_birth=datetime(1990, 10, 10),
                                       phone_number="0660000000",
                                       email="test@gmail.com",
                                       salary=2000.00,
                                       department_id=2)

        db.session.add_all([self.test_department_1, self.test_department_2, self.test_employee1, self.test_employee2])
        db.session.commit()
        self.department_service = DepartmentService()
        self.employee_service = EmployeeService()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()
