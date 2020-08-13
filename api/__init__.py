import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv(dotenv_path='../.env')

# POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
# POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
# POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
# POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
# POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
