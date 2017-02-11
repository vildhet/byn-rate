#!/usr/bin/env python3

from flask import Flask, send_file

app = Flask(__name__, static_url_path='', static_folder='www')

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()