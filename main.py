import os
from flask_migrate import Migrate
from departments_app import create_app, db
from departments_app.models.department import Department
from departments_app.models.employee import Employee

# !!!!! to delete
from departments_app.service.schemas import department_schema, departments_schema, employee_schema, employees_schema
import os
import sys
import click

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='departments_app/*')
    COV.start()

############################################################
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# to enable migrate
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """ enable objects to flask shell """
    return dict(db=db, Department=Department, Employee=Employee,
                department_schema=department_schema, departments_schema=departments_schema,
                employee_schema=employee_schema, employees_schema=employees_schema)


#################################
@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Run tests under code coverage.')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
