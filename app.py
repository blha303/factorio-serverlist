#!/usr/bin/env python3
from flask import *
from flask.ext.cache import Cache
import requests

from os import environ
from json import load
from sys import exit

app = Flask(__name__)
cache = Cache(app,config={"CACHE_TYPE": "simple"})
try:
    with open(environ["HOME"] + "/factorio/player-data.json") as f:
        credentials = load(f)
except:
    print("No user credentials. Get the multiplayer dedicated server, put it at {}/factorio, add your user account to its settings and run it once".format(environ["HOME"]))
    exit(1)

@cache.cached(timeout=10)
@app.route("/server/<id>")
def serverinfo(id):
    return jsonify(requests.get("https://multiplayer.factorio.com/get-game-details/{}".format(id)).json())

@cache.cached(timeout=60)
@app.route("/server")
@app.route("/server/")
def serverlist():
    return jsonify(requests.get("https://multiplayer.factorio.com/get-games?username={service-username}&token={service-token}".format(**credentials)).json())

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=24527, host="0.0.0.0")
