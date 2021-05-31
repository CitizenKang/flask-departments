import unittest
import uuid
from departments_app import db
from departments_app.models.department import Department
from base_service_tst import BaseServiceTestCase


class DepartmentServiceTestCase(BaseServiceTestCase):

    def test_fetch_one_departments_returns_data(self):
        department = Department.query.filter_by(name="TestDepartment1").one()
        fetched_data = self.service.fetch_one(department.uuid)
        self.assertIsInstance(fetched_data, dict)
        self.assertEqual(department.uuid, fetched_data["uuid"], f"Should be {fetched_data.get('uuid')}")
        self.assertEqual(department.name, fetched_data["name"], f"Should be {fetched_data.get('uuid')}")

    def test_fetch_one_departments_returns_none(self):
        fetched_data = self.service.fetch_one(str(uuid.uuid4()))
        self.assertIsNotNone(fetched_data, "Wrong uuid should return None")

    def test_fetch_all_aggregated(self):
        query_result = self.service.fetch_all_departments_aggregated(db.session)
        self.assertIsInstance(query_result, list, "Should be a list")
        self.assertIsInstance(query_result[0], dict, "Should be a dict")
        self.assertEqual(len(query_result), 2, "Should be 2 records")

    def test_fetch_all_aggregated_empty(self):
        pass

    def test_add_one_successful(self):
        data = {"name": "Another Department"}
        result, message = self.service.add_one(data)
        self.assertIsNotNone(result, message)
        self.assertIsInstance(message, dict)

    def test_add_one_duplicate(self):
        data = {"name": "Another Department"}
        self.service.add_one(data)
        result, message = self.service.add_one(data)
        self.assertIsNone(result)
        self.assertIsNotNone(message)
        self.assertIsInstance(message, dict)
        self.assertEqual(message, {"message": "Such record already exists"})

    def test_add_one_not_valid_data(self):
        data = {"names": "Another Department"}
        result, message = self.service.add_one(data)
        self.assertIsNotNone(message, result)
        self.assertIsInstance(message, dict)

    def test_update_one(self):
        pass


if __name__ == '__main__':
    unittest.main()
