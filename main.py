import os
from departments_app import create_app, db
from flask_migrate import Migrate
from departments_app.models import Departments

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# to enable migrate
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Departments=Departments)
