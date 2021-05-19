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
        result = employee_schema.dump(Employee.query.filter_by(uuid=uuid).one())
        if result:
            return result, 200
        return result, 404

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


class DepartmentEmployees(Resource):
    def get(self, department_uuid: str, employee_uuid: str = None):
        """
        Process GET request on resource,
        Returns collection of employees if employee_uuid is not given, and status code 200
        Returns one employee and status code 200 if proper employee_uuid is given,
        In other cases return response with code - 404
        """
        # Fetch all employees in department
        if not employee_uuid:
            query_result = db.session.query(Employee).join(Department).filter(Department.uuid == department_uuid).all()
            result = employees_schema.dump(query_result)
            if not result:
                return {}, 204  # No employees in department
            return result, 200

        # Fetch one employee
        query_result = db.session.query(Employee).join(Department).filter(Department.uuid == department_uuid,
                                                                          Employee.uuid == employee_uuid).one()
        result = employee_schema.dump(query_result)
        if result:
            return result, 200
        return result, 404

    def post(self, department_uuid: str, ):
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
        # Add department_id
        data.department_id = Department.query.filter_by(uuid=department_uuid).one().id
        # Try to add record to db, if records exists it raise IntegrityError
        db.session.add(data)
        try:
            db.session.commit()
        except IntegrityError:
            return {"message": "Such record already exists"}, 422
        return {"message": "Added new employee", "uuid": data.uuid}, 201

    def put(self, department_uuid: str, employee_uuid: str):
        """ Process PUT request on resource, updating it """

        # Check input
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        # Validate and deserialize input
        try:
            data = employee_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        # query existing record in not found - return 404
        db_record = Employee.query.filter_by(uuid=data.uuid).one()
        if not db_record:
            return {}, 404

        # update record if there is updated field
        if data.first_name:
            db_record.first_name = data.first_name
        if data.last_name:
            db_record.last_name = data.last_name
        if data.date_of_birth:
            db_record.date_of_birth = data.date_of_birth
        if data.phone_number:
            db_record.phone_number = data.phone_number
        if data.email:
            db_record.email = data.email
        if data.salary:
            db_record.salary = data.salary
        # update if another department
        if data.name:
            db_record.name = data.name
        if data.long_name:
            db_record.long_name = data.long_name

        try:
            db.session.commit()
        except IntegrityError:
            return {}, 409
        return {"message": "resource updated"}, 200

    def delete(self, department_uuid: str, employee_uuid: str):
        """
        Process DELETE Returns status code 204 on successful delete in other case - 404
        """
        db_record = db.session.query(Employee).join(Department).filter(Department.uuid == department_uuid,
                                                                       Employee.uuid == employee_uuid).one()
        if db_record:
            db.session.delete(db_record)
            db.session.commit()
            return {}, 204
        return {}, 404


rest_api.add_resource(Employees, 'employee/', 'employee/<uuid>', strict_slashes=False)
rest_api.add_resource(DepartmentEmployees, 'department/<department_uuid>/employee',
                      'department/<department_uuid>/employee/<employee_uuid>',
                      strict_slashes=False)
