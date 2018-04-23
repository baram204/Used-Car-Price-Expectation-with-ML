from project import create_app

# for flat flask.. not uwsgi
# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/flask.cfg
app = create_app('flask.cfg')
