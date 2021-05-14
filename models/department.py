import uuid
from departments_app import db, ma


class Department(db.Model):
    """
    Class describes departments table
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    name = db.Column(db.String(30), index=True, nullable=False)
    long_name = db.Column(db.String(200), nullable=False)
    employees = db.relationship('Employee', backref='role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"{self.name} ({self.long_name}) [{self.uuid}]"
