import sys
from os.path import dirname, abspath, join
from flask import Flask

www_path = join(dirname(abspath(sys.modules['__main__'].__file__)), 'www')
app = Flask(__name__, static_url_path='', static_folder=www_path)

@app.route('/')
def index():
    return app.send_static_file('index.html')

def run():
    app.run()