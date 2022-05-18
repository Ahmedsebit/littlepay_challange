import os

from dotenv import load_dotenv

load_dotenv()

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    
    database_url=os.getenv('DATABASE_POSTGRESS_URL')
    
    SQLALCHEMY_DATABASE_URI = database_url
    JSON_SORT_KEYS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI ="postgresql://myuser:mypass@localhost:5432/littlepay"


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = dict(
    development = DevelopmentConfig,
    testing = TestingConfig,
    staging = StagingConfig,
    production = ProductionConfig
)
    