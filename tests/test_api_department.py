import unittest
from flask import create_app
from departments_app import create_app, db
from test_base import BaseTestCase


class DepartmentsResourceTestCase(BaseTestCase):

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Stranger' in response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
