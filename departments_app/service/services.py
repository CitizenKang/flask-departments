from departments_app.models.department import Department
from departments_app.models.employee import Employee
from sqlalchemy.sql import func
from departments_app import db
from departments_app.service.schemas import department_schema, departments_schema
from departments_app.service.schemas import employee_schema, employees_schema
from sqlalchemy.exc import IntegrityError, NoResultFound
from marshmallow import ValidationError


class DepartmentService:

    @staticmethod
    def fetch_all_departments_avg_salary_num_employees(session):
        """
        returns result of query Department name, department uuid and
        average salary of all employees of each department
        number of employees of each department

        """
        result = session.query(Department.name, Department.uuid, func.avg(Employee.salary),
                               func.count(Employee.first_name)).outerjoin(Employee).group_by(Department.name).all()
        return result

    @staticmethod
    def fetch_all():
        """
        returns serialised data for collection of Departments
        """
        query_result = Department.query.all()
        return departments_schema.dump(query_result)

    @staticmethod
    def fetch_one(uuid):
        """
        returns serialised data for one Departments object
        """
        try:
            query_result = Department.query.filter_by(uuid=uuid).one()
        except NoResultFound:
            return None
        return department_schema.dump(query_result)

    @staticmethod
    def add_one(json_data):
        """
        takes json data, deserialize it and add to database
        returns tuple of uuid of new object and message if success
        or None and error message
        """
        # Validate and deserialize input
        try:
            data = department_schema.load(json_data, partial=("uuid",))
        except ValidationError as err:
            return None, err.messages

        # Try to add record to db, if records exists it raise IntegrityError
        new_record = Department(**data)
        try:
            new_record.create()
        except IntegrityError:
            return None, {"message": "Such record already exists"}

        return new_record.uuid, {"message": "Added new department", "uuid": new_record.uuid}

    @staticmethod
    def update_one_department(uuid, json_data):
        """
         
        """
        try:
            data = department_schema.load(json_data, partial=("uuid",))
        except ValidationError as err:
            return 'validation error', err.messages

        # query existing record in not found - return 404
        db_record = Department.get_by_uuid(uuid)
        if not db_record:
            return 'not found', 404

        # update record if there is updated field
        if name := data.get("name"):
            db_record.name = name
        try:
            db.session.commit()
        except IntegrityError:
            return {}, 409

        return {"message": "resource updated"}, 200


class EmployeeService:
    @staticmethod
    def fetch_all_department_employees(department_uuid: str):
        """
        return tuple
        first element list of dictionaries af all employees of given department uuid
        second element string name of department
        """
        department_id = Department.get_by_uuid(department_uuid).id
        department_name = Department.get_by_uuid(department_uuid).name
        if department_id:
            result = Employee.query.filter_by(department_id=department_id).all()
            return employees_schema.dump(result), department_name

    @staticmethod
    def fetch_all_employees():
        """
        return first element list of dictionaries af all employees
        """
        result = Employee.query.all()
        return employees_schema.dump(result)
