import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_sijax

#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.
db = SQLAlchemy()
sjx = flask_sijax.Sijax()

######################################
#### Application Factory Function ####
######################################

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    # The path where you want the extension to create the needed javascript files
    # DON'T put any of your files in this directory, because they'll be deleted!
    app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

    # You need to point Sijax to the json2.js library if you want to support
    # browsers that don't support JSON natively (like IE <= 7)
    app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'

    initialize_extensions(app)
    register_blueprints(app)
    return app


##########################
#### Helper Functions ####
##########################

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    sjx = flask_sijax.Sijax(app)

def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from project.usedcar import usedcar_blueprint
    from project.aptinfo import aptinfo_blueprint


    app.register_blueprint(usedcar_blueprint, url_prefix='/usedcars' )
    app.register_blueprint(aptinfo_blueprint, url_prefix='/aptinfo' )