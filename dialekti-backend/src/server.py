from flask import Flask
import os

flaskPort = int(os.environ['FLASK_PORT']) if os.environ['FLASK_PORT'] else 3000

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '.'

@app.route('/')
def home():
    return 'Hello, world!'

@app.route('/version')
def version():
    return 'Dialekti v0.1.0'

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=flaskPort)