from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from . import rest_api
from departments_app.models.employee import db, Employee
from departments_app.service.schemas import employee_schema, employees_schema
from sqlalchemy.exc import IntegrityError


class Employees(Resource):
    def get(self, uuid: str = None):
        """
        Process GET request on resource,
        Returns one employee and status code 200 if proper uuid given, otherwise - 404
        Returns all employees if uuid is not given, and status code 200
        """
        # all
        if not uuid:
            result = employees_schema.dump(Employee.query.all())
            return result, 200
        # one
        result = employee_schema.dump(Employee.query.filter_by(uuid=uuid).one())
        if result:
            return result, 200
        return result, 404

    def post(self):
        """
        Process POST request on resource,
        Returns status code 201 and new resource
        """
        # Check input
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            data = employee_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        # Try to add record to db, if records exists it raise IntegrityError
        db.session.add(data)
        try:
            db.session.commit()
        except IntegrityError:
            return {"message": "Such record already exists"}, 422
        return {"message": "Added new department", "uuid": data.uuid}, 201

    def delete(self, uuid: str):
        """
        Process DELETE request on resource, deletes record with given uuid.
        Returns status code 204 on successful delete in other case - 404
        """
        db_record = Employee.query.filter_by(uuid=uuid).first()
        if db_record:
            db.session.delete(db_record)
            db.session.commit()
            return {}, 204
        return {}, 404


rest_api.add_resource(Employees, 'employees/', 'employees/<uuid>', strict_slashes=False)
