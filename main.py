import os
from departments_app import create_app, db
from flask_migrate import Migrate
from departments_app.models.department import Department
from departments_app.models.employee import Employee

# !!!!! to delete
from departments_app.service.schemas import department_schema, departments_schema, employee_schema, employees_schema

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# to enable migrate
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Department=Department, Employee=Employee,
                department_schema=department_schema, departments_schema=departments_schema,
                employee_schema=employee_schema, employees_schema=employees_schema)

