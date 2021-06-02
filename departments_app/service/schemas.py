from departments_app import ma
from departments_app.models.department import Department
from departments_app.models.employee import Employee
from marshmallow import post_load


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        exclude = ['id']


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        exclude = ['id', "department_id"]
        dump_only = ("uuid",)
        include_fk = True

    department = ma.Nested(DepartmentSchema)

    @post_load
    def modify_input(self, data, **kwargs):
        """
        Modify loaded data return tuple of dictionary
        for Employee model and uuid for related Department
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
