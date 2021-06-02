from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import rest_api
from departments_app.models.employee import db, Employee
from departments_app.models.department import Department
from departments_app.service.schemas import employee_schema, employees_schema
from departments_app.service.services import EmployeeService


class Employees(Resource):
    def get(self, uuid: str = None):
        """
        Process GET request on resource,
        Returns one employee and status code 200 if proper uuid given, otherwise - 404
        Returns all employees if uuid is not given, and status code 200
        """
        # all
        if not uuid:
            return EmployeeService.fetch_all(), 200
        # one
        result = EmployeeService.fetch_one(uuid=uuid)
        if result:
            return result, 200
        return {}, 404

    def delete(self, uuid: str):
        """
        Process DELETE request on resource, deletes record with given uuid.
        Returns status code 204 on successful delete in other case - 404
        """
        db_record = Employee.get_by_uuid(uuid)
        if db_record:
            db.session.delete(db_record)
            db.session.commit()
            return {}, 204

        return {}, 404

    def post(self):
        """
        Process POST request on resource, returns status code 201 and new resource
        If new resource hasn't been added returns error message and 422 code
        """
        # Check input
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        result, message = EmployeeService.add_one(data=json_data)
        if not result:
            return message, 422
        return message, 201

    def put(self, uuid: str):
        """ Process PUT request on resource, updating it """
        # Check input
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        result, message = EmployeeService.update_one(uuid=uuid, data=json_data)
        if result == 'validation error':
            return message, 422
        if result == "not found":
            return message, 404
        if result == "duplicate":
            return message, 409
        return message, 200


rest_api.add_resource(Employees, 'employee/', 'employee/<uuid>', strict_slashes=False)
