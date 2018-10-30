import os

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


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
