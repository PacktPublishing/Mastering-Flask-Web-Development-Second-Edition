# Used for AWS ElasticBeanstalk deploy

import os
from webapp import create_app
from webapp.cli import register
from dotenv import load_dotenv

# Patch for elasticbeanstalk not loading env vars
EB_ENV_FILE='/opt/python/current/env'
if os.path.isfile(EB_ENV_FILE):
    load_dotenv(EB_ENV_FILE)

env = os.environ.get('WEBAPP_ENV', 'dev')
application = create_app('config.%sConfig' % env.capitalize())
register(application)
