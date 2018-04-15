from flask import Blueprint
usedcar_blueprint = Blueprint('usedcar', __name__, template_folder='templates')

from . import routes
