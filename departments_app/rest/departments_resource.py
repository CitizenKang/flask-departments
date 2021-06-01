from flask import request
from flask_restful import Resource
from . import rest_api
from departments_app.models.department import Department
from departments_app.service.services import DepartmentService
from sqlalchemy.exc import OperationalError, IntegrityError


class Departments(Resource):
    def get(self, uuid: str = None):
        """
        Process GET request on resource. Returns collection of all departments if uuid is not given,
        and response status code 200 Returns one department object and status code 200 if uuid is given
        In other cases returns response code - 404
        """
        # all
        if not uuid:
            return DepartmentService.fetch_all(), 200
        # one
        result = DepartmentService.fetch_one(uuid=uuid)
        if result:
            return result, 200
        return result, 404

    def post(self):
        """
        Process POST request on resource. Returns status code 201 and new resource if succeeded
        or status code and error message
        """
        # Check input
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        result, message = DepartmentService.add_one(json_data=json_data)
        if not result:
            return message, 409 if message.get("message") == "Such record already exists" else 422
        return message, 201

    def put(self, uuid: str):
        """ Process PUT request on resource, updating it """
        # Check input
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        result, message = DepartmentService.update_one_department(uuid=uuid, data=json_data)
        if result == 'validation error':
            return message, 422
        if result == "not found":
            return message, 404
        if result == "duplicate":
            return message, 409

        return message, 200

    def delete(self, uuid: str):
        """
        Process DELETE request on resource, deletes record with given uuid.
        Returns status code 204 on successful delete in other case - 404
        """
        db_record = Department.get_by_uuid(uuid)
        if uuid and db_record:
            try:
                Department.delete(db_record)
            except IntegrityError:
                return {}, 404

            return {}, 204
        return {}, 404


rest_api.add_resource(Departments, 'department/', 'department/<uuid>', strict_slashes=False)
