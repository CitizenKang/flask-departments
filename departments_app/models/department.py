import uuid
from departments_app import db


class Department(db.Model):
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

    def create(self):
        """ Creates record"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """ Deletes record """
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def get_by_uuid(cls, uuid: str):
        """Fetch one record dy uuid"""
        return cls.query.filter_by(uuid=uuid).first()
