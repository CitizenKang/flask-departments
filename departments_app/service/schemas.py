from departments_app import ma
from departments_app.models.department import Department
from departments_app.models.employee import Employee
from departments_app import db
from marshmallow import post_load, pre_dump, pre_load
from marshmallow import ValidationError


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        # load_instance = True
        exclude = ['id']


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        # load_instance = True
        exclude = ['id', "department_id"]
        dump_only = ("uuid",)
        include_fk = True

    department = ma.Nested(DepartmentSchema)

    @post_load
    def modify_input(self, data, **kwargs):
        """
        After data loaded process output and return tuple
        of dictionary for Employee model and uuid for Department
         """
        try:
            department_uuid = data.pop("department").get("uuid")
        except KeyError:
            department_uuid = None
        employee_dict = data
        return employee_dict, department_uuid


# Init schemas

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)

employee_schema = EmployeeSchema(load_instance=False)
employees_schema = EmployeeSchema(many=True)
