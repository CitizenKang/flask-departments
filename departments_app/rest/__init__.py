from flask import Blueprint
from flask_restful import Api

rest_api_bp = Blueprint('rest', __name__, url_prefix='/api')
rest_api = Api(rest_api_bp)

from . import departments_resource, employees_resource
