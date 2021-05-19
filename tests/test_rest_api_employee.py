import unittest
from datetime import datetime
from departments_app import create_app, db
from departments_app.models.department import Department
from departments_app.models.employee import Employee


class EmployeesResourceTestCase(unittest.TestCase):

    def setUp(self):
        """ Prepare test fixture, create application"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # adding departments
        d1 = Department(name="TestDepartment1", long_name="Test long name department 1")
        d2 = Department(name="TestDepartment2", long_name="Test long name department 2")

        e1 = Employee(first_name="JohnAsz", last_name="Doe",
                      date_of_birth=datetime(1990, 10, 10), phone_number="0970000000",
                      email="john_doe@gmail.com",
                      salary=1000.00, department_id=1)

        db.session.add_all([d1, d2, e1])
        db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # GET

    def test_get_all_department_employees(self):
        """ Check GET returns 204 on empty collection """
        department_uuid = Department.query.filter_by(name="TestDepartment1").one().uuid
        response = self.client.get(f"/api/department/{department_uuid}/employee")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    # POST
    def test_post_add_resource_status_code(self):
        """ Check POST return status code on successful resource add """
        test_data = {"first_name": 'TestName',
                     "last_name": 'TestLastName',
                     "date_of_birth": "2000-01-01",
                     "phone_number": "0970000000",
                     "email": "TestName@gmail.com",
                     "salary": 100000.00}
        department_uuid = Department.query.filter_by(name="TestDepartment1").one().uuid
        response = self.client.post(f'/api/department/{department_uuid}/employee', json=test_data)
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
