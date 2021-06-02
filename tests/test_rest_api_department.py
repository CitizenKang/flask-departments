import unittest
import uuid
from departments_app.models.department import Department
from base_test import BaseServiceTestCase


class DepartmentResourceTestCase(BaseServiceTestCase):

    # GET
    def test_get_all_status_code_content_type(self):
        response = self.client.get('/api/department/')
        self.assertEqual(response.status_code, 200, "Should be 200")
        self.assertEqual(response.content_type, 'application/json')

    def test_get_all_content(self):
        response = self.client.get('/api/department/')
        self.assertTrue(self.test_department_1.name in response.get_data(as_text=True))
        self.assertTrue(self.test_department_2.name in response.get_data(as_text=True))
        self.assertEqual(response.content_type, "application/json")

    def test_get_one_content(self):
        department_uuid = self.test_department_1.uuid
        response = self.client.get(f'/api/department/{department_uuid}')
        self.assertEqual(response.status_code, 200, "Should be 200")
        self.assertTrue(self.test_department_1.name in response.get_data(as_text=True))
        self.assertFalse(self.test_department_2.name in response.get_data(as_text=True))
        self.assertEqual(response.content_type, "application/json")

    def test_get_one_not_found_status_code(self):
        department_uuid = str(uuid.uuid4())
        response = self.client.get(f'/api/department/{department_uuid}')
        self.assertEqual(response.status_code, 404, "Should be 404")
        self.assertEqual(response.content_type, "application/json")

    # DELETE
    def test_delete_status_code_not_cascade(self):
        department_uuid = self.test_department_2.uuid
        response = self.client.delete(f'/api/department/{department_uuid}')
        self.assertEqual(response.status_code, 404, "Should be 404")
        self.assertEqual(response.content_type, "application/json")

    def test_delete_status_code(self):
        # Delete related employees
        self.test_employee1.delete()
        self.test_employee2.delete()
        dep_uuid1, dep_uuid2 = self.test_department_1.uuid, self.test_department_2.uuid

        # delete 2 records on 1st, 2nd response should be 204, on the 3rd - 404
        response_1 = self.client.delete(f'/api/department/{dep_uuid1}')
        response_2 = self.client.delete(f'/api/department/{dep_uuid2}')
        response_3 = self.client.delete(f'/api/department/{dep_uuid2}')
        self.assertEqual(response_1.status_code, 204, "Should be 204")
        self.assertEqual(response_2.status_code, 204, "Should be 204")
        self.assertEqual(response_3.status_code, 404, "Should be 404")

    # POST
    def test_post_add_resource_status_code(self):
        data = {"name": "test_name"}
        response = self.client.post('/api/department/', json=data)
        self.assertEqual(response.status_code, 201, "Should be 201")
        self.assertEqual(response.content_type, "application/json")

    def test_post_add_same_resource_status_code(self):
        data = {"name": "test_name"}
        response = self.client.post('/api/department/', json=data)
        response = self.client.post('/api/department/', json=data)
        self.assertEqual(response.status_code, 409, "Should be 409")
        self.assertEqual(response.content_type, "application/json")

    def test_post_wrong_data_in_request(self):
        empty_data = {}
        wrong_data = {"wrong": "wrong", "ong_name": "sdf"}
        response_empty = self.client.post('/api/department/', json=empty_data)
        response_wrong = self.client.post('/api/department/', json=wrong_data)
        self.assertEqual(response_empty.status_code, 400, "Should be 400")
        self.assertEqual(response_wrong.status_code, 422, "Should be 422")
        self.assertEqual(response_empty.content_type, "application/json")
        self.assertEqual(response_wrong.content_type, "application/json")

    def test_post_add_resource_new_location(self):
        data = {"name": "test_name"}
        response = self.client.post('/api/department/', json=data)
        self.assertEqual(response.status_code, 201, "Should be 201")
        db_uuid = Department.query.filter_by(name=data.get("name")).one().uuid
        self.assertTrue(db_uuid in response.get_data(as_text=True))
        self.assertEqual(response.content_type, "application/json")

    # PUT
    def test_put_status_code(self):
        department_uuid = self.test_department_1.uuid
        data = {"name": "Test"}
        response = self.client.put(f'/api/department/{department_uuid}', json=data)
        self.assertEqual(response.status_code, 200, "Should be 200")
        new_db_record = Department.query.filter_by(name='Test').first()
        self.assertEqual(new_db_record.name, data.get("name"))
        self.assertEqual(response.content_type, "application/json")

    def test_put_empty_data_code(self):
        department_uuid = self.test_department_1.uuid
        data = {}
        response = self.client.put(f'/api/department/{department_uuid}', json=data)
        self.assertEqual(response.status_code, 400, "Should be 400")
        self.assertEqual(response.content_type, "application/json")

    def test_put_status_code_not_found(self):
        department_uuid = str(uuid.uuid4())
        data = {"name": "Department2"}
        response = self.client.put(f'/api/department/{department_uuid}', json=data)
        self.assertEqual(response.status_code, 404, "Should be 404")
        self.assertEqual(response.content_type, "application/json")

    def test_put_status_code_not_duplicate(self):
        department_uuid = self.test_department_1.uuid
        data = {"name": self.test_department_2.name}
        response = self.client.put(f'/api/department/{department_uuid}', json=data)
        self.assertEqual(response.status_code, 409, "Should be 409")
        self.assertEqual(response.content_type, "application/json")


if __name__ == '__main__':
    unittest.main()
