import uuid
from departments_app import db
from departments_app.service.db_models_mixin import BaseDBOperationMixin


class Department(BaseDBOperationMixin, db.Model):
    """
    Class describes departments table
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    name = db.Column(db.String(30), unique=True, index=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"[{self.uuid}] {self.name}"
