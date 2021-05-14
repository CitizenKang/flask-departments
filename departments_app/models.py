import uuid
from departments_app import db, ma
from marshmallow import fields
from marshmallow_sqlalchemy import auto_field


class Departments(db.Model):
    """
    Class describes departments table
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    name = db.Column(db.String(30), index=True, nullable=False)
    long_name = db.Column(db.String(200), nullable=False)
    employees = db.relationship('Employees', backref='role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"{self.name} ({self.long_name}) [{self.uuid}]"


class Employees(db.Model):
    """
    Class describes employees table
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    first_name = db.Column(db.String(30), index=True, nullable=False)
    last_name = db.Column(db.String(30), index=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(13), nullable=True)
    email = db.Column(db.String(254), nullable=True)
    salary = db.Column(db.Float, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"[{self.uuid}] {self.first_name} {self.last_name}, D.O.B.: {self.date_of_birth}"
