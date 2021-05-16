import unittest
from departments_app import create_app, db
from departments_app.models.department import Department


class DepartmentResourceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        d1 = Department(name="Test_Department_1", long_name="Test long name department 1")
        d2 = Department(name="Test_Department_2", long_name="Test long name department 2")
        db.session.add_all([d1, d2])
        db.session.commit()
        self.client = self.app.test_client(use_cookies=True)

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
        db_record = Department.query.filter_by(name='Test_Department_1').first()
        uuid = db_record.uuid
        # delete one record on first response should be 204, on the second 404
        response_first = self.client.delete(f'/api/departments/{uuid}')
        response_second = self.client.delete(f'/api/departments/{uuid}')
        self.assertEqual(response_first.status_code, 204)
        self.assertEqual(response_second.status_code, 404)

    # POST
    def test_put_add_resource_status_code(self):
        data = {"name": "test_name", "long_name": "Test long name"}
        response = self.client.post(f'/api/departments/', json=data)
        self.assertEqual(response.status_code, 201)

    def test_put_add_resource_new_location(self):
        """ Check if uuid of new resource is returned """
        data = {"name": "test_name", "long_name": "Test long name"}
        response = self.client.post(f'/api/departments/', json=data)
        self.assertEqual(response.status_code, 201)
        db_record = Department.query.filter_by(name=data["name"]).first()
        uuid = db_record.uuid
        self.assertTrue(uuid in response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
