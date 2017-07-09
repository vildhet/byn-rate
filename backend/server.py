import sys
from os.path import dirname, abspath, join
from flask import Flask, jsonify, abort

from . import data

www_path = join(dirname(abspath(sys.modules['__main__'].__file__)), 'www')
app = Flask(__name__, static_url_path='', static_folder=www_path)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/data/<name>')
def get_data(name):
    collection = data.get_by_name(name)
    if collection:
        return jsonify(collection.get_web())
    else:
        abort(404)

def run():
    app.run()