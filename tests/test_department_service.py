import unittest
import uuid
from datetime import datetime
from departments_app import create_app, db
from departments_app.service.services import DepartmentService
from departments_app.models.department import Department
from departments_app.models.employee import Employee
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
        self.assertIsNotNone(fetched_data)


if __name__ == '__main__':
    unittest.main()
