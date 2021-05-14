import os
from departments_app import create_app, db
from flask_migrate import Migrate
from models.department import Department
from models.employee import Employee

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# to enable migrate
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Department=Department, Employee=Employee)
