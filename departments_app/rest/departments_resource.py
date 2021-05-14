from flask_restful import Resource
from . import rest_api


class Departments(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


rest_api.add_resource(Departments, 'departments/', '/<uuid>', strict_slashes=False)
