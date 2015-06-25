#!/usr/bin/env python

from flask import Flask, jsonify, session, request
import zerodb

try:
    import simplejson as json
except:
    import json

PORT = 2015
HOST = "127.0.0.1"
DEBUG = True
DEV_SECRET_KEY = "development key"

app = Flask(__name__)
dbs = {}


@app.route("/_connect", methods=["GET", "POST"])
def connnect():
    if request.method == "GET":
        req = request.args
    elif request.method == "POST":
        req = request.form
    else:
        return jsonify(ok=0)

    username = req.get("username")
    passphrase = req.get("passphrase")
    host = req.get("host")
    port = req.get("port")

    if not (username and passphrase and host and port):
        return jsonify(ok=0, message="Incomplete login information")

    try:
        print host, port, username, passphrase
        db = zerodb.DB((host, port), username=username, password=passphrase)
    except Exception, e:
        return jsonify(ok=0, message=str(e), error_type=e.__class__.__name__)

    session["username"] = username
    dbs[username] = db

    return jsonify(ok=1)


@app.route("/<table_name>/_find")
def find(table_name):
    if request.method == "GET":
        req = request.args
    elif request.method == "POST":
        req = request.form
    else:
        return jsonify(ok=0)

    criteria = json.loads(req.get("criteria"))

    skip = req.get("skip")
    if skip:
        skip = int(skip)
    limit = req.get("limit")
    if limit:
        limit = int(limit)

    return jsonify(hello="world")


@app.route("/_disconnect")
def disconnect():
    if "username" in session:
        username = session.pop("username")
        if username in dbs:
            del dbs[username]
    return jsonify(ok=1)


if __name__ == "__main__":
    app.config["SECRET_KEY"] = DEV_SECRET_KEY
    app.run(host=HOST, port=PORT, debug=DEBUG)
