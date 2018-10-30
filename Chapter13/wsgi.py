import os
from webapp import create_app
from webapp.cli import register

env = os.environ.get('WEBAPP_ENV', 'dev')
application = create_app('config.%sConfig' % env.capitalize())
register(application)
