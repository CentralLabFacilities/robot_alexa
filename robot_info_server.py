#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


pepper=dict()
tobi=dict()


class _tobi(Resource):
    @staticmethod
    def get(key):
        try:
            return tobi[key]
        except KeyError:
            return {}, 404

    @staticmethod
    def put(key):
        global tobi
        ret = request.get_json(force=True)

        try:
            if tobi[key]:
                tobi[key] = ret
            return "update "+key+": "+tobi[key]
        except KeyError:
            tobi[key] = request.get_json(force=True)
            return "init "+key+": "+tobi[key]


class _pepper(Resource):
    @staticmethod
    def get(key):
        try:
            return pepper[key]
        except KeyError:
            return ""

    @staticmethod
    def put(key):
        global pepper
        ret = request.get_json(force=True)

        try:
            if pepper[key]:
                pepper[key] = ret
            return "update "+key+": "+pepper[key]
        except KeyError:
            pepper[key] = request.get_json(force=True)
            return "init "+key+": "+pepper[key]

class _clear(Resource):
    @staticmethod
    def get():
        pepper = dict()
        tobi = dict()
        return "cleared"

    @staticmethod
    def put():
        pepper = dict()
        tobi = dict()
        return "cleared"

api.add_resource(_pepper, '/pepper/<string:key>')
api.add_resource(_tobi, '/tobi/<string:key>')
api.add_resource(_clear, '/clear')

@app.route("/help")
def _help():
    return "<head><title>Help Page</title></head>" \
           "<body>" \
           "  <h1>Help:</h1>" \
           "  <p>set location for pepper (analog for tobi), location can be dynamically replaced by any key:" \
           "    <pre>$ curl -i -H 'Content-Type: application/json' -X PUT -d '\"kitchen\"' http://localhost:5000/pepper/location<pre>" \
           "  </p>" \
           "  <p>Ask the server if job exists and return its state:" \
           "    <pre>$ curl -i -X GET http://localhost:5000/pepper/location<pre>" \
           "  </p>" \
           "  <p>Push a new state for an existing job eg. <i>request job exec</i> (<b>you must send all attributes!</b>):" \
           "    <pre>$ curl -i -H 'Content-Type: application/json' -X PUT -d '{\"requested\": \"true\", \"started\": \"false\", \"stopped\": \"false\"}' http://localhost:5000/state/blubb<pre>" \
           "  </p>" \
           "  <p>Reset joblist" \
           "    <pre>$ curl -i -X GET http://localhost:5000/reset<pre>" \
           "  </p>" \
           "</body>"


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')