from departments_app import ma
from departments_app.models.department import Department
from departments_app.models.employee import Employee
from departments_app import db


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        load_instance = True
        exclude = ['id']
        # dump_only = ("uuid",)


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        load_instance = True
        exclude = ['id']
        dump_only = ("uuid", "department_id")
        include_fk = True

    department = ma.Nested(DepartmentSchema)
    # department = ma.Nested(DepartmentSchema, only=("uuid", "name",))


# Init schemas

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)

employee_schema = EmployeeSchema(load_instance=False)
employees_schema = EmployeeSchema(many=True)
