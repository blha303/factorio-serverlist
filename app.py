#!/usr/bin/env python3
from flask import *
import requests
import requests_cache

from os import environ
from json import load
from sys import exit

app = Flask(__name__)
requests_cache.install_cache(backend='sqlite', expire_after=180)
try:
    with open(environ["HOME"] + "/factorio/player-data.json") as f:
        credentials = load(f)
except:
    print("No user credentials. Get the multiplayer dedicated server, put it at {}/factorio, add your user account to its settings and run it once".format(environ["HOME"] if "HOME" in environ else "{user directory}"))
    exit(1)

@app.route("/api/server/<id>")
def infojson(id):
    return jsonify(requests.get("https://multiplayer.factorio.com/get-game-details/{}".format(id)).json())

@app.route("/api/list")
def serverlist():
    data = requests.get("https://multiplayer.factorio.com/get-games?username={service-username}&token={service-token}".format(**credentials)).json()
    for d in data:
        d["has_password"] = True if d["has_password"] == "true" else False
    return jsonify(data)

@app.route("/info/<id>")
def infohtml(id):
    data = requests.get("https://multiplayer.factorio.com/get-game-details/{}".format(id)).json()
    return render_template("info.html", d=data, title=data["name"])

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=24527, host="0.0.0.0")
