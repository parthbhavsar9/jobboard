import requests
from argparse import ArgumentParser
from flask import Flask, Response, request
from flask_cors import CORS

from api.calculation_wip import calculation
from api.parser import cv_parse



def create_app():
    webapp = Flask(__name__)
    CORS(webapp)
    webapp.register_blueprint(calculation)
    webapp.register_blueprint(cv_parse)

    return webapp

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=80, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()
    app.run(host='0.0.0.0',port=port)