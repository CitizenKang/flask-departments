from departments_app import ma
from models.department import Department
from models.employee import Employee
from marshmallow import fields
from marshmallow_sqlalchemy import auto_field


class DepartmentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Department
        # Fields to expose
        fields = ("uuid", "name", "long_name")


class EmployeeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Employee
        include_fk = True
        # Fields to expose
        # fields = ("uuid", "first_name", "last_name", "date_of_birth", "phone_number", "email", "salary")

    uuid = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    date_of_birth = ma.auto_field()
    phone_number = ma.auto_field()
    email = ma.auto_field()
    salary = ma.auto_field()
    department_id = ma.auto_field()

# Init schemas

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
