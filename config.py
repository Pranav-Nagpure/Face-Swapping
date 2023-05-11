class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'secret'

    DB_NAME = 'production-db'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'password'

    UPLOADS = '/app/static/uploads'
    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = 'development-db'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'password'

    UPLOADS = '/app/static/uploads'
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    DEBUG = True

    DB_NAME = 'development-db'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'password'

    UPLOADS = '/app/static/uploads'
    SESSION_COOKIE_SECURE = False
