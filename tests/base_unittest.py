import unittest
from datetime import datetime
from departments_app import create_app, db
from departments_app.models.employee import Employee


class FlaskBasicTest(unittest.TestCase):
    # employee1 = Employee(first_name='John', last_name='Doe', date_of_birth=datetime(1990, 1, 1),
    #                      phone_number='0970000000',
    #                      email='john_doe@gmail.com', salary=1000.00, department_id=1)
    # employee2 = Employee(first_name='Jane', last_name='Doe', date_of_birth=datetime(1970, 10, 15),
    #                      phone_number='0500000000',
    #                      email='jane1970@gmail.com', salary=2000.00, department_id=3)
    # db.session.add_all([employee1, employee2])
    # db.session.commit()

    def setUp(self):
        """ Prepare test fixture, create application"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean-up db, remove application context"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()
