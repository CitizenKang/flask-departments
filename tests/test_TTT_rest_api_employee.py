import unittest
from datetime import datetime
from departments_app import create_app, db
from departments_app.models.employee import Employee


class DepartmentResourceTestCase(unittest.TestCase):


    def setUp(self):
        """ Prepare test fixture, create application"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        employee1 = Employee(first_name='John', last_name='Doe', date_of_birth=datetime(1990, 1, 1),
                             phone_number='0970000000',
                             email='john_doe@gmail.com', salary=1000.00, department_id=1)
        employee2 = Employee(first_name='Jane', last_name='Doe', date_of_birth=datetime(1970, 10, 15),
                             phone_number='0500000000',
                             email='jane1970@gmail.com', salary=2000.00, department_id=3)
        db.session.add_all([employee1, employee2])
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # GET
    def test_get_collection_code_content(self):
        """ Check GET return status code and content type """
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_get_collection_code_content_empty_db(self):
        """ Check GET return status code and content type """
        db.session.delete_all()
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, 'application/json')

    def test_get_object_code_content_content(self):
        """ Check GET return status code and content type """
        db_record = Employee.query.filter_by(first_name="John", last_name="Doe").first()
        uuid = db_record.uuid
        response = self.client.get(f'/api/employees/{uuid}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')


    def test_get_all_content(self):
        """ Check GET content on all employees """
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('John' in response.get_data(as_text=True))
        self.assertTrue('Jane' in response.get_data(as_text=True))

    def test_get_one_content(self):
        """ Check GET content on one employee """
        db_record = Employee.query.filter_by(first_name="John", last_name="Doe").first()
        uuid = db_record.uuid
        response = self.client.get(f'/api/employees/{uuid}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("John" in response.get_data(as_text=True))
        self.assertFalse("Jane" in response.get_data(as_text=True))

    def test_get_one_not_found_status_code(self):
        """ Check GET return status code on nor existed data """
        db_record = Employee.query.filter_by(first_name="John", last_name="Doe").first()
        uuid = db_record.uuid
        self.client.delete(f'/api/departments/{uuid}')
        response = self.client.get(f'/api/departments/{uuid}')
        self.assertEqual(response.status_code, 404)

    # DELETE
    def test_delete_status_code(self):
        """ Checks DELETE return status code """
        db_record = Employee.query.filter_by(first_name='John').first()
        uuid = db_record.uuid
        # delete one record on first response should be 204, on the second 404
        response_first = self.client.delete(f'/api/employees/{uuid}')
        response_second = self.client.delete(f'/api/employees/{uuid}')
        self.assertEqual(response_first.status_code, 204)
        self.assertEqual(response_second.status_code, 404)

    # POST
    def test_post_add_resource_status_code(self):
        """ Check POST return status code on successful resource add """
        data = {'email': 'xx@xz@gmail.com', 'first_name': 'Ivan', 'department_id': 1, 'date_of_birth': '1900-01-01',
                'last_name': 'Ivanov', 'salary': 100000.0, 'phone_number': '0630000000'}
        response = self.client.post('/api/employees/', json=data)
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

    # def test_post_add_resource_new_location(self):
    #     """ Check if uuid of new resource is returned """
    #     data = {"name": "test_name", "long_name": "Test long name"}
    #     response = self.client.post('/api/departments/', json=data)
    #     self.assertEqual(response.status_code, 201)
    #     db_record = Department.query.filter_by(name=data["name"]).first()
    #     uuid = db_record.uuid
    #     self.assertTrue(uuid in response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
