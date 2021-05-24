from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from . import rest_api
from departments_app.models.department import Department
from departments_app.service.schemas import department_schema, departments_schema
from departments_app import db
from sqlalchemy.exc import IntegrityError
from departments_app.service.services import DepartmentService


class Departments(Resource):
    def get(self, uuid: str = None):
        """
        Process GET request on resource,
        Returns collection of all departments if uuid is not given, and response status code 200
        Returns one department object and status code 200 if uuid is given
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
        Process POST request on resource,
        Returns status code 201 and new resource
        """
        # Check input
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        result, message = DepartmentService.add_one(json_data=json_data)
        if not result:
            return message, 422
        return message, 201

    def put(self, uuid: str):
        """ Process PUT request on resource, updating it """

        # Check input
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        # try:
        #     data = department_schema.load(json_data, partial=("uuid",))
        # except ValidationError as err:
        #     return err.messages, 422
        #
        # # query existing record in not found - return 404
        # db_record = Department.get_by_uuid(uuid)
        # if not db_record:
        #     return {}, 404
        #
        # # update record if there is updated field
        # if name := data.get("name"):
        #     db_record.name = name
        # try:
        #     db.session.commit()
        # except IntegrityError:
        #     return {}, 409
        # return {"message": "resource updated"}, 200
        result = DepartmentService.update_one_department(uuid=uuid, json_data=json_data)



    def delete(self, uuid: str):
        """
        Process DELETE request on resource, deletes record with given uuid.
        Returns status code 204 on successful delete in other case - 404
        """
        db_record = Department.get_by_uuid(uuid)
        if uuid and db_record:
            Department.delete(db_record)
            return {}, 204
        return {}, 404


rest_api.add_resource(Departments, 'department/', 'department/<uuid>', strict_slashes=False)
