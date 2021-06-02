import unittest
import uuid
from departments_app import db
from departments_app.models.department import Department
from base_test import BaseServiceTestCase


class DepartmentServiceTestCase(BaseServiceTestCase):

    def test_fetch_one_departments_returns_data(self):
        department = Department.query.filter_by(name="TestDepartment1").one()
        fetched_data = self.department_service.fetch_one(department.uuid)
        self.assertIsInstance(fetched_data, dict)
        self.assertEqual(department.uuid, fetched_data["uuid"], f"Should be {fetched_data.get('uuid')}")
        self.assertEqual(department.name, fetched_data["name"], f"Should be {fetched_data.get('name')}")

    def test_fetch_one_departments_returns_none(self):
        fetched_data = self.department_service.fetch_one(str(uuid.uuid4()))
        self.assertIsNone(fetched_data, "Wrong uuid should return None")

    def test_fetch_all_aggregated(self):
        query_result = self.department_service.fetch_all_departments_aggregated(db.session)
        self.assertIsInstance(query_result, list, "Should be a list")
        self.assertIsInstance(query_result[0], dict, "Should be a dict")
        self.assertEqual(len(query_result), 2, "Should be 2 records")

    def test_fetch_all_aggregated_empty(self):
        pass

    def test_add_one_successful(self):
        data = {"name": "Another Department"}
        result, message = self.department_service.add_one(data)
        self.assertIsNotNone(result, message)
        self.assertIsInstance(message, dict)

    def test_add_one_duplicate(self):
        data = {"name": "Another Department"}
        self.department_service.add_one(data)
        result, message = self.department_service.add_one(data)
        self.assertIsNone(result)
        self.assertIsNotNone(message)
        self.assertIsInstance(message, dict)
        self.assertEqual(message, {"message": "Such record already exists"})

    def test_add_one_not_valid_data(self):
        data = {"names": "Another Department"}
        result, message = self.department_service.add_one(data)
        self.assertIsNotNone(message, result)
        self.assertIsInstance(message, dict)

    def test_update_one_successful(self):
        department_uuid = self.test_department_1.uuid
        data = {"name": "Department"}
        result, message = self.department_service.update_one_department(uuid=department_uuid, data=data)
        self.assertEqual(result, "OK", "Should be 'OK'")
        self.assertEqual(self.test_department_1.name, "Department", "Should be 'Department'")

    def test_update_one_validation_error(self):
        department_uuid = self.test_department_1.uuid
        data = {"Name": "Department"}
        result, message = self.department_service.update_one_department(uuid=department_uuid, data=data)
        self.assertEqual(result, "validation error", "Should be 'validation error'")

    def test_update_one_validation_duplicate(self):
        department_uuid = str(uuid.uuid4())
        data = {"name": "TestDepartment2"}
        result, message = self.department_service.update_one_department(uuid=department_uuid, data=data)
        self.assertEqual(result, "not found", "Should be 'not found'")


if __name__ == '__main__':
    unittest.main()
