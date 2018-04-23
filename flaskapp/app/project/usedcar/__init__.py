from flask import Blueprint
usedcar_blueprint = Blueprint('usedcar', __name__, url_prefix='/usedcars')

from . import routes
