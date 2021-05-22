from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import rest_api
from departments_app.models.employee import db, Employee
from departments_app.models.department import Department
from departments_app.service.schemas import employee_schema, employees_schema, department_schema, departments_schema


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
        result = Employee.get_by_uuid(uuid=uuid)
        if result:
            return employee_schema.dump(result), 200
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
        Process POST request on resource,
        Returns status code 201 and new resource
        """
        # Check input
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        # Validate input
        try:
            data = employee_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        if not data[1]:
            return {"message:": "department uuid not provided"}, 422

        employee, department_uuid = data
        department_id = Department.get_by_uuid(department_uuid).id
        new_record = Employee(department_id=department_id, **employee)

        # Try to add record to db, if records exists it raise IntegrityError
        db.session.add(new_record)
        try:
            db.session.commit()
        except IntegrityError:
            return {"message": "Such record already exists"}, 422

        return {"message": "Added new employee", "uuid": new_record.uuid}, 201

    def put(self, uuid: str):
        """ Process PUT request on resource, updating it """

        # Check input
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        # Validate and deserialize input
        try:
            data = employee_schema.load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422

        # query existing record in not found - return 404
        db_record = Employee.get_by_uuid(uuid)
        if not db_record:
            return {}, 404

        employee, department_uuid = data
        # update record if there is updated field
        if first_name := employee.get("first_name"):
            db_record.first_name = first_name
        if last_name := employee.get("last_name"):
            db_record.last_name = last_name
        if date_of_birth := employee.get("date_of_birth"):
            db_record.date_of_birth = date_of_birth
        if phone_number := employee.get("phone_number"):
            db_record.phone_number = phone_number
        if email := employee.get("email"):
            db_record.email = email
        if salary := employee.get("salary"):
            db_record.salary = salary

        # update if uuid of department was given
        if department_uuid:
            department_id = Department.get_by_uuid(uuid=data[1].get("uuid"))
            if department_id:
                db_record.department_id = department_id

        try:
            db.session.commit()
        except IntegrityError:
            return {}, 409
        return {"message": "resource updated"}, 200


rest_api.add_resource(Employees, 'employee/', 'employee/<uuid>', strict_slashes=False)
