# -*- coding: utf-8 -*-

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    guest = request.args.get('name', 'World')
    return 'Hello, %s!' % guest

if __name__ == "__main__":
    app.run(debug=True)
