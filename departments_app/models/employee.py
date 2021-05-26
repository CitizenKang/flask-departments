import uuid
from departments_app import db
from departments_app.service.db_models_mixin import BaseDBOperationMixin


class Employee(BaseDBOperationMixin, db.Model):
    """
    Class describes employees table
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    first_name = db.Column(db.String(30), index=True, nullable=False)
    last_name = db.Column(db.String(30), index=True, nullable=False)
    date_of_birth = db.Column(db.Date)
    phone_number = db.Column(db.String(13), nullable=True)
    email = db.Column(db.String(254), nullable=True)
    salary = db.Column(db.Float, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=False)
    department = db.relationship("Department", lazy=True, backref=db.backref("department", lazy=True))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"[{self.uuid}] {self.first_name} {self.last_name}, D.O.B.: {self.date_of_birth}"
