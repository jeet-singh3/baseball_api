import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    PORT = 8443
    DEBUG = False
    TESTING = False


class Production(Config):
    DEBUG = False
    TESTING = False


class QA(Config):
    DEBUG = True
    TESTING = False


class Development(Config):
    DEBUG = True
    TESTING = False


class Testing(Config):
    DEBUG = True
    TESTING = True


def get_config_by_env(env=None):
    configs = {
        'development': Development,
        'production': Production,
        'qa': QA,
        'testing': Testing
    }
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')

    return configs[env]