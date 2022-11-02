"""Flask configuration."""
from os import environ, path


# from dotenv import load_dotenv

class Config:
    TEMPLATES_FOLDER = 'templates'


class DevConfig(Config):
    TESTING = False
    DEBUG = True
    FLASK_ENV = 'development'


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'