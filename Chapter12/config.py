import os
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'
    RECAPTCHA_PUBLIC_KEY = "6LdKkQQTAAAAAEH0GFj7NLg5tGicaoOus7G9Q5Uw"
    RECAPTCHA_PRIVATE_KEY = '6LdKkQQTAAAAAMYroksPTJ7pWhobYb88fTAcxcYn'
    POSTS_PER_PAGE = 10

    TWITTER_API_KEY = "XXXX"
    TWITTER_API_SECRET = "XXXX"
    FACEBOOK_CLIENT_ID = "XXX"
    FACEBOOK_CLIENT_SECRET = "XXXX"

    CELERY_BROKER_URL = "amqp://rabbitmq:rabbitmq@localhost//"
    CELERY_BACKEND_URL = "amqp://rabbitmq:rabbitmq@localhost//"

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USER = "@gmail.com"
    MAIL_PASSWORD = "password"
    MAIL_DEFAULT_SENDER = "from@flask.com"

    CELERYBEAT_SCHEDULE = {
        'weekly-digest': {
            'task': 'blog.tasks.digest',
            'schedule': crontab(day_of_week=6, hour='10')
        },
    }


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_PASSWORD = ''
    CACHE_REDIS_DB = '0'


class DevConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    CACHE_TYPE = 'simple'


class TestConfig(Config):

    DEBUG = True
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False

    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
    CELERY_BACKEND_URL = "amqp://guest:guest@localhost:5672//"

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USERNAME = 'username'
    MAIL_PASSWORD = 'password'
