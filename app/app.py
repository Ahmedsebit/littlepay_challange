import os
import logging
from config import app_config
from flask import jsonify
from flask_api import FlaskAPI
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint


db = SQLAlchemy()
migrate = Migrate(db)

### swagger specific ###
SWAGGER_URL = '/api/littlepay/swagger'
API_URL = '/static/swagger.json'
URL_PREFIX = '/api/littlepay'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "littlepay"
    }
)

logger = logging.getLogger(__name__)


def create_app(config_name):
    '''
    Wraps the creation of a new Flask object, and returns it after it's loaded up
    with configuration settings using app.config and connected to the DB using
    '''
    
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    migrate.init_app(app, db)
    
    app.app_context().push()
    log_level = logging.INFO
    app.logger.setLevel(log_level)
    
    import app.controllers.trips as api_v1
    
    db.init_app(app)
    
    app.register_blueprint(api_v1.littlepay_bp, url_prefix=URL_PREFIX)
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    
    @app.teardown_request
    def teardown_request(exception):
        if exception:
            db.session.rollback()
        db.session.remove()

    return app
