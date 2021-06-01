from departments_app import db


class BaseDBOperationMixin:
    """
    Mixin class extends db Models with some basic operations
    """

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
