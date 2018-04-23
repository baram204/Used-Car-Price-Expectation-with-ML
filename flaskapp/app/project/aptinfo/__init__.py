from flask import Blueprint
aptinfo_blueprint = Blueprint('aptinfo', __name__, url_prefix='/aptinfo', template_folder='templates',
    static_folder='static', static_url_path='/static')

from . import routes
