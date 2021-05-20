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
        self.test_department_1 = Department(name="TestDepartment1")
        self.test_department_2 = Department(name="TestDepartment2")
        # adding employee
        self.test_employee = Employee(first_name="testJohn", last_name="testDoe",
                                      date_of_birth=datetime(1990, 10, 10), phone_number="0970000000",
                                      email="test@gmail.com",
                                      salary=1000.00, department_id=1)

        db.session.add_all([self.test_department_1, self.test_department_2, self.test_employee])
        db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # GET

    def test_get_all_employees(self):
        """ Check GET response status code and content-type on collection """
        response = self.client.get("/api/employee")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_get_one_employee(self):
        """ Check GET response status code and content-type on one item """
        uuid = self.test_employee.uuid
        response = self.client.get(f"/api/employee/{uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_get_one_wrong_uuid_(self):
        """ Check GET returns 404 on wrong uuid """
        uuid = self.test_employee.uuid
        db.session.delete(self.test_employee)
        db.session.commit()
        response = self.client.get(f"/api/employee/{uuid}")
        self.assertEqual(response.status_code, 404)

    # POST
    def test_post_add_resource_status_code(self):
        """ Check POST return status code, returns uuid on successful resource add """

        test_data = {"first_name": 'TestName',
                     "last_name": 'TestLastName',
                     # "date_of_birth": 1990-10-13, ???
                     "phone_number": "0970000000",
                     "email": "TestName@gmail.com",
                     "salary": 100000.00,
                     "department": {"uuid": self.test_department_1.uuid, "name": self.test_department_1.name}}

        response = self.client.post(f'/api/employee', json=test_data)
        self.assertEqual(response.status_code, 201)

        db_record = Employee.query.filter_by(first_name=test_data["first_name"]).first()
        uuid = db_record.uuid
        self.assertTrue(uuid in response.get_data(as_text=True))

    def test_post_wrong_data_in_request(self):
        """ Check POST return status code on wrong data in request """
        empty_data = {}
        test_data_no_department = {"first_name": 'Te2stName',
                                   "last_name": 'TestL3astName',
                                   # "date_of_birth": 1990-10-13, ???
                                   "phone_number": "0970000000",
                                   "email": "TestName@gmail.com",
                                   "salary": 100000.00, }
        test_data_with_mistakes = {"firwst_name": 'TestName',
                                   "last_name": 'TestLastName',
                                   # "date_of_birth": 1990-10-13, ???
                                   "phone_number": "0970000000",
                                   "email": "TestName@gmail.com",
                                   "salary": 100000.00,
                                   "department": {"uuid": self.test_department_1.uuid,
                                                  "name": self.test_department_1.name}}

        response_empty = self.client.post('/api/employee/', json=empty_data)
        response_wrong1 = self.client.post('/api/employee/', json=test_data_no_department)
        response_wrong2 = self.client.post('/api/employee/', json=test_data_with_mistakes)

        self.assertEqual(response_empty.status_code, 400)
        self.assertEqual(response_wrong1.status_code, 422)
        self.assertEqual(response_wrong2.status_code, 422)

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

    # DELETE
    def test_delete_status_code(self):
        """ Checks DELETE return correct status codes (204, 404) """
        uuid = self.test_employee.uuid
        # delete one record on first response should be 204, on the second 404
        response_first = self.client.delete(f'/api/employee/{uuid}')
        response_second = self.client.delete(f'/api/employee/{uuid}')
        self.assertEqual(response_first.status_code, 204)
        self.assertEqual(response_second.status_code, 404)


if __name__ == '__main__':
    unittest.main()
