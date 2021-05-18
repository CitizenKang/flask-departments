import unittest
from datetime import datetime
from base_unittest import FlaskBasicTest
from departments_app import create_app, db
from departments_app.models.employee import Employee

employee1 = Employee(first_name='John', last_name='Doe', date_of_birth=datetime(1990, 1, 1),
                     phone_number='0970000000', email='john_doe@gmail.com', salary=1000.00, department_id=1)
employee2 = Employee(first_name='Jane', last_name='Doe', date_of_birth=datetime(1970, 10, 15),
                     phone_number='0500000000', email='jane1970@gmail.com', salary=2000.00, department_id=3)

# employee1 = {"first_name":'JohnAsz', "last_name":'Doe'," date_of_birth":"1990-01-01", "phone_number":"0970000000", "email":"john_doe@gmail.com", "salary":1000.00, "department_id"=1}
class DepartmentResourceTestCase(FlaskBasicTest):

    employee1 = Employee(first_name='John', last_name='Doe', date_of_birth=datetime(1990, 1, 1),
                         phone_number='0970000000', email='john_doe@gmail.com', salary=1000.00, department_id=1)
    employee2 = Employee(first_name='Jane', last_name='Doe', date_of_birth=datetime(1970, 10, 15),
                         phone_number='0500000000', email='jane1970@gmail.com', salary=2000.00, department_id=3)

    def add_record(self):
        db.session.add_all([self.employee1, self.employee2])
        db.session.commit()
        print("OK")

    def test_get_collection_code_content(self):
        """ Check GET return status code and content type """
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
#



if __name__ == '__main__':
    unittest.main()
