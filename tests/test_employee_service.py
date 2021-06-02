import unittest
import uuid
from departments_app.service.services import EmployeeService
from departments_app.models.employee import Employee
from base_test import BaseServiceTestCase


class DepartmentServiceTestCase(BaseServiceTestCase):

    def test_fetch_one_returns_data(self):
        employee = Employee.query.filter_by(first_name="John").one()
        fetched_data = self.employee_service.fetch_one(employee.uuid)
        self.assertIsInstance(fetched_data, dict)
        self.assertEqual(employee.uuid, fetched_data["uuid"], f"Should be {fetched_data.get('uuid')}")
        self.assertEqual(employee.first_name, fetched_data["first_name"], f"Should be {fetched_data.get('first_name')}")
        self.assertEqual(employee.salary, fetched_data["salary"], f"Should be {fetched_data.get('salary')}")

    def test_fetch_one_employee_returns_none(self):
        fetched_data = self.employee_service.fetch_one(str(uuid.uuid4()))
        self.assertIsNone(fetched_data, "Should be None")

    def test_fetch_all_returns_data(self):
        fetched_data = self.employee_service.fetch_all()
        self.assertIsInstance(fetched_data, list, "Should be list type")
        self.assertIsInstance(fetched_data[0], dict, "Should be dict type")
        self.assertEqual(len(fetched_data), 2, "Should be 2 records")

    def test_fetch_all_of_department_returns_data(self):
        department_uuid = self.test_department_1.uuid
        fetched_data = self.employee_service.fetch_all_of_department(department_uuid)
        employees, department = fetched_data
        self.assertIsInstance(fetched_data, tuple, "Should be tuple type")
        self.assertIsInstance(employees, list, "Should be list type")
        self.assertIsInstance(department, str, "Should be str type")
        self.assertEqual(department, self.test_department_1.name, f"Should be {self.test_department_1.name}")

    def test_add_one(self):
        data = {"first_name": "test",
                "last_name": "test",
                "date_of_birth": '1990-10-10',
                "phone_number": "0660000000",
                "email": "test@gmail.com",
                "salary": 2000.00,
                "department": {"uuid": self.test_department_1.uuid}}
        result = self.employee_service.add_one(data)
        obj_uuid, message = result
        new_obj_uuid = Employee.query.filter_by(first_name="test").first().uuid
        self.assertIsInstance(result, tuple, "Should be tuple type")
        self.assertIsNotNone(obj_uuid)
        self.assertEqual(obj_uuid, new_obj_uuid, f"Should be {new_obj_uuid}")
        self.assertEqual(message, {"message": "Added new employee", "uuid": f"{new_obj_uuid}"})

    def test_add_one_no_department(self):
        data = {"first_name": "test",
                "last_name": "test",
                "date_of_birth": '1990-10-10',
                "phone_number": "0660000000",
                "email": "test@gmail.com",
                "salary": 2000.00}
        result = self.employee_service.add_one(data)
        obj_uuid, message = result
        self.assertIsInstance(result, tuple, "Should be tuple type")
        self.assertIsNone(obj_uuid)
        self.assertEqual(message, {"message:": "department uuid not provided"})

    def test_add_one_invalid_data(self):
        data = {"firswt_name": "test",
                "last_name": "test",
                "date_of_birth": '1990-10-10',
                "phone_number": "0660000000",
                "email": "test@gmail.com",
                "salary": 2000.00}
        result = self.employee_service.add_one(data)
        obj_uuid, message = result
        self.assertIsInstance(result, tuple, "Should be tuple type")
        self.assertIsNone(obj_uuid)

    def test_update_one_successfull(self):
        data = {"first_name": "test"}
        employee_uuid = self.test_employee1.uuid
        result, message = EmployeeService.update_one(uuid=employee_uuid, data=data)
        self.assertEqual(message, {"message": "resource updated"})
        self.assertEqual(result, "OK")
        self.assertEqual(self.test_employee1.first_name, data.get("first_name"))

    def test_update_one_not_found(self):
        data = {"first_name": "test"}
        employee_uuid = str(uuid.uuid4())
        result, message = EmployeeService.update_one(uuid=employee_uuid, data=data)
        self.assertEqual(result, "not found")

    def test_update_one_not_valid_data(self):
        data = {"name": "test"}
        employee_uuid = self.test_employee1.uuid
        result, message = EmployeeService.update_one(uuid=employee_uuid, data=data)
        self.assertEqual(result, "validation error")


if __name__ == '__main__':
    unittest.main()
