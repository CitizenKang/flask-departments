import unittest
import uuid
from datetime import datetime
from departments_app import create_app, db
from departments_app.models.department import Department
from departments_app.models.employee import Employee
from base_test import BaseServiceTestCase


class EmployeesResourceTestCase(BaseServiceTestCase):

    # GET
    def test_get_all_status_code_content_type(self):
        response = self.client.get("/api/employee")
        self.assertEqual(response.status_code, 200, "Should be 200")
        self.assertEqual(response.content_type, "application/json")

    def test_get_all_content(self):
        response = self.client.get("/api/employee")
        self.assertTrue(self.test_employee1.first_name in response.get_data(as_text=True))
        self.assertTrue(self.test_employee2.first_name in response.get_data(as_text=True))

    def test_get_one_employee(self):
        employee_uuid = self.test_employee1.uuid
        response = self.client.get(f"/api/employee/{employee_uuid}")
        self.assertEqual(response.status_code, 200, "Should be 200")
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(self.test_employee1.first_name in response.get_data(as_text=True))
        self.assertTrue(self.test_employee2.first_name not in response.get_data(as_text=True))

    def test_get_one_wrong_uuid(self):
        employee_uuid = str(uuid.uuid4())
        response = self.client.get(f"/api/employee/{employee_uuid}")
        self.assertEqual(response.status_code, 404, "Should be 404")
        self.assertEqual(response.content_type, "application/json")

    # DELETE
    def test_delete_status_code_success_delete(self):
        employee_uuid = self.test_employee2.uuid
        response = self.client.delete(f'/api/employee/{employee_uuid}')
        self.assertEqual(response.status_code, 204, "Should be 204")
        self.assertEqual(response.content_type, "application/json")

    def test_delete_status_code_no_delete(self):
        employee_uuid = self.test_employee2.uuid
        response_first = self.client.delete(f'/api/employee/{employee_uuid}')
        response = self.client.delete(f'/api/employee/{employee_uuid}')
        self.assertEqual(response.status_code, 404, "Should be 404")
        self.assertEqual(response.content_type, "application/json")

    # POST
    def test_post_add_resource_success(self):
        data = {"first_name": 'TestName',
                "last_name": 'TestLastName',
                "phone_number": "0970000000",
                "email": "TestName@gmail.com",
                "salary": 100000.00,
                "department": {"uuid": self.test_department_1.uuid}}
        response = self.client.post(f'/api/employee', json=data)
        self.assertEqual(response.status_code, 201, "Should be 201")
        self.assertEqual(response.content_type, "application/json")

    def test_post_add_resource_no_success(self):
        data = {"first_name": 'TestName',
                "last_name": 'TestLastName',
                "phone_number": "0970000000",
                "email": "TestName@gmail.com",
                "salary": 100000.00}
        response = self.client.post(f'/api/employee', json=data)
        self.assertEqual(response.status_code, 422, "Should be 422")
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue("department uuid not provided" in response.get_data(as_text=True))

    def test_post_add_resource_no_data(self):
        data = {}
        response = self.client.post(f'/api/employee', json=data)
        self.assertEqual(response.status_code, 400, "Should be 400")
        self.assertEqual(response.content_type, "application/json")

    def test_post_add_resource_wrong_data_fields(self):
        data = {"f_name": 'TestName',
                "name": 'TestLastName',
                "phone_number": "0970000000",
                "email": "TestName@gmail.com",
                "salary": 100000.00}
        response = self.client.post(f'/api/employee', json=data)
        self.assertEqual(response.status_code, 422, "Should be 422")
        self.assertEqual(response.content_type, "application/json")

    # PUT
    def test_put_successful(self):
        employee_uuid = self.test_employee1.uuid
        data = {"first_name": "Updated_name"}
        response = self.client.put(f'/api/employee/{employee_uuid}', json=data)
        self.assertEqual(response.status_code, 200, "Should be 200")
        self.assertEqual(response.content_type, "application/json")

    def test_put_no_data(self):
        employee_uuid = self.test_employee1.uuid
        data = {}
        response = self.client.put(f'/api/employee/{employee_uuid}', json=data)
        self.assertEqual(response.status_code, 400, "Should be 400")
        self.assertEqual(response.content_type, "application/json")

    def test_put_no_found_resource(self):
        employee_uuid = str(uuid.uuid4)
        data = {"first_name": "Updated_name"}
        response = self.client.put(f'/api/employee/{employee_uuid}', json=data)
        self.assertEqual(response.status_code, 404, "Should be 404")
        self.assertEqual(response.content_type, "application/json")

    def test_put_wrong_data(self):
        employee_uuid = str(uuid.uuid4)
        data = {"name": "Updated_name"}
        response = self.client.put(f'/api/employee/{employee_uuid}', json=data)
        self.assertEqual(response.status_code, 422, "Should be 422")
        self.assertEqual(response.content_type, "application/json")


if __name__ == '__main__':
    unittest.main()
