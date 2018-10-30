from flask import Flask
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

# Changed to show the git diff command
@app.route('/')
def home():
    return '<h1>Hello world</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
