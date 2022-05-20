import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

    database_url = os.getenv('DATABASE_POSTGRESS_URL')

    SQLALCHEMY_DATABASE_URI = database_url
    JSON_SORT_KEYS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    STOP1_TO_STOP2 = os.getenv('STOP1_TO_STOP2')
    STOP2_TO_STOP3 = os.getenv('STOP2_TO_STOP3')
    STOP1_TO_STOP3 = os.getenv('STOP1_TO_STOP3')
    
    AWS_REGION = os.getenv('AWS_REGION')
    AWS_ACCESS_ID = os.getenv('AWS_ACCESS_ID')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    AWS_BUCKET_FOLDER = os.getenv('AWS_BUCKET_FOLDER')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    STOP1_TO_STOP2="$ 3.25"
    STOP2_TO_STOP3="$ 5.50"
    STOP1_TO_STOP3="$ 7.30"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://myuser:mypass@localhost:5432/littlepay_test"


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    staging=StagingConfig,
    production=ProductionConfig
)
