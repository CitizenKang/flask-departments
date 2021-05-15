from departments_app import ma
from departments_app.models.employee import Employee


class DepartmentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("uuid", "name", "long_name")


class EmployeeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Employee
        include_fk = True

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
