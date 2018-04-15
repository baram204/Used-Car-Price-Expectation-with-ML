#################
#### imports ####
#################

from flask import render_template
from . import usedcar_blueprint

################
#### routes ####
################

@usedcar_blueprint.route('/')
def usedcar_index():
    return render_template('index.html')