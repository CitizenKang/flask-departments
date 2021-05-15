from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from . import rest_api
from departments_app.models.department import db, Department
from departments_app.service.schemas import department_schema, departments_schema
from sqlalchemy.exc import IntegrityError


class Departments(Resource):
    def get(self, uuid: str = None):
        """
        Process GET request on resource,
        Returns one departments and status code 200 if proper uuid given, otherwise - 404
        Returns all departments if uuid is not given, and status code 200
        """
        # one
        if not uuid:
            result = departments_schema.dump(Department.query.all())
            return result, 200
        # all
        result = department_schema.dump(Department.query.filter_by(uuid=uuid).first())
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
            data = department_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        except KeyError as err:
            return err, 422

        # Try to add record to db, if records exists it raise IntegrityError
        record = Department(**data)
        db.session.add(record)
        try:
            db.session.commit()
        except IntegrityError:
            return {}, 422
        return {"message": "Added new department", "uuid": record.uuid}

    def put(self):
        pass

    def delete(self, uuid: str):
        """
        Process DELETE request on resource, deletes record with given uuid.
        Returns status code 204 on successful delete in other case - 404
        """
        db_record = Department.query.filter_by(uuid=uuid).first()
        if uuid and db_record:
            db.session.delete(db_record)
            db.session.commit()
            return {}, 204
        return {}, 404


rest_api.add_resource(Departments, 'departments/', 'departments/<uuid>', strict_slashes=False)
