import unittest
from departments_app import create_app, db
from departments_app.models.department import Department


class DepartmentResourceTestCase(unittest.TestCase):

    def setUp(self):
        """ Prepare test fixture, create application"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        d1 = Department(name="Test_Department_1", long_name="Test long name department 1")
        d2 = Department(name="Test_Department_2", long_name="Test long name department 2")
        db.session.add_all([d1, d2])
        db.session.commit()
        # store test data records uuid for future tests
        self.test_record_1_uuid = d1.uuid
        self.test_record_2_uuid = d2.uuid
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # GET
    def test_get_all_status_code(self):
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, 200)

    def test_get_all_content_type(self):
        response = self.client.get('/api/departments/')
        self.assertEqual(response.content_type, 'application/json')

    def test_get_all_content(self):
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Test_Department_1' in response.get_data(as_text=True))
        self.assertTrue('Test_Department_2' in response.get_data(as_text=True))

    def test_get_one_content(self):
        db_record = Department.query.filter_by(name='Test_Department_1').first()
        uuid = db_record.uuid
        response = self.client.get(f'/api/departments/{uuid}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Test_Department_1' in response.get_data(as_text=True))
        self.assertFalse('Test_Department_2' in response.get_data(as_text=True))

    def test_get_one_not_found_status_code(self):
        db_record = Department.query.filter_by(name='Test_Department_1').first()
        uuid = db_record.uuid
        self.client.delete(f'/api/departments/{uuid}')
        response = self.client.get(f'/api/departments/{uuid}')
        self.assertEqual(response.status_code, 404)

    # DELETE
    def test_delete_status_code(self):
        """ Checks DELETE return status code """
        db_record = Department.query.filter_by(name='Test_Department_1').first()
        uuid = db_record.uuid
        # delete one record on first response should be 204, on the second 404
        response_first = self.client.delete(f'/api/departments/{uuid}')
        response_second = self.client.delete(f'/api/departments/{uuid}')
        self.assertEqual(response_first.status_code, 204)
        self.assertEqual(response_second.status_code, 404)

    # POST
    def test_post_add_resource_status_code(self):
        """ Check POST return status code on successful resource add """
        data = {"name": "test_name", "long_name": "Test long name"}
        response = self.client.post('/api/departments/', json=data)
        self.assertEqual(response.status_code, 201)

    def test_post_add_same_resource_status_code(self):
        """ Check POST return status code on existing resource add """
        data = {"name": "test_name", "long_name": "Test long name"}
        response = self.client.post('/api/departments/', json=data)
        response = self.client.post('/api/departments/', json=data)
        self.assertEqual(response.status_code, 422)

    def test_post_wrong_data_in_request(self):
        """ Check POST return status code on wrong data in request """
        empty_data = {}
        wrong_data = {"wrong": "wrong", "ong_name": "sdf"}
        response_empty = self.client.post('/api/departments/', json=empty_data)
        response_wrong = self.client.post('/api/departments/', json=wrong_data)
        self.assertEqual(response_empty.status_code, 400)
        self.assertEqual(response_wrong.status_code, 422)

    def test_post_add_resource_new_location(self):
        """ Check if uuid of new resource is returned """
        data = {"name": "test_name", "long_name": "Test long name"}
        response = self.client.post('/api/departments/', json=data)
        self.assertEqual(response.status_code, 201)
        db_record = Department.query.filter_by(name=data["name"]).first()
        uuid = db_record.uuid
        self.assertTrue(uuid in response.get_data(as_text=True))

    # Put
    def test_put_status_code(self):
        """ Check PUT return status code on successful update """
        db_record = Department.query.filter_by(name='Test_Department_1').first()
        uuid = db_record.uuid
        data = {"long_name": "New updated long name "}
        response = self.client.put(f'/api/departments/{uuid}', json=data)
        self.assertEqual(response.status_code, 200)

    def test_put_status_code_2(self):
        """ Check PUT return status code on successful update """
        db_record = Department.query.filter_by(name='Test_Department_1').first()
        uuid = db_record.uuid
        data = {"name": "Test_Department_2"}
        response = self.client.put(f'/api/departments/{uuid}', json=data)
        self.assertEqual(response.status_code, 409)


if __name__ == '__main__':
    unittest.main()
