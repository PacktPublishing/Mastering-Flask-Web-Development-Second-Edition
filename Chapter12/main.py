import os
from webapp import create_app
from webapp.cli import register

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())
register(app)

if __name__ == '__main__':
    app.run()
