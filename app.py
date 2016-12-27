#!/usr/bin/env python3
from flask import *
import requests
import requests_cache
app = Flask(__name__)
requests_cache.install_cache(backend='sqlite', expire_after=180)

import os
import json
import sys
try:
    with open(os.environ["HOME"] + "/factorio/player-data.json") as f:
        credentials = json.load(f)
except:
    print("No user credentials. Get the multiplayer dedicated server, put it at {}/factorio, add your user account to its settings and run it once".format(environ["HOME"] if "HOME" in environ else "{user directory}"), file=sys.stderr)
    sys.exit(1)

import pygeoip
geoip = {}
if os.path.isfile("GeoIP.dat"):                    # http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
    geoip["c"] = pygeoip.GeoIP("GeoIP.dat")
if os.path.isfile("GeoIPASNum.dat"):               # http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz
    geoip["asn"] = pygeoip.GeoIP("GeoIPASNum.dat")

def serverinfo(id):
    data = requests.get("https://multiplayer.factorio.com/get-game-details/{}".format(id)).json()
    if "c" in geoip:
        data["country"] = geoip["c"].country_code_by_addr(data["host_address"].split(":")[0]).lower()
    if "asn" in geoip:
        data["asn"] = geoip["asn"].org_by_addr(data["host_address"].split(":")[0])
    return data

@app.route("/flags/<path:path>")
def send_flag(path):
    return send_from_directory("flags", path)

@app.route("/api/getmod/<slug>")
@app.route("/api/getmod/<slug>/<version>")
def getmod(slug, version="latest"):
    if slug == "base":
        return redirect(request.referrer)
    data = requests.get("https://mods.factorio.com/api/mods/{}".format(slug)).json()
    if data.get("detail", None) == "Not found.":
        return jsonify({"error":"Can't find that mod"})
    if version == "latest":
        return redirect("https://mods.factorio.com" + data["releases"][0]["download_url"])
    else:
        for file in data["releases"]:
            if file["version"] == version:
                return redirect("https://mods.factorio.com" + file["download_url"])

@app.route("/api/server/<id>")
def info_json(id):
    return jsonify(serverinfo(id))

@app.route("/api/list")
def serverlist():
    data = requests.get("https://multiplayer.factorio.com/get-games?username={service-username}&token={service-token}".format(**credentials)).json()
    if not data:
        with requests_cache.disabled():
            data = requests.get("https://multiplayer.factorio.com/get-games?username={service-username}&token={service-token}".format(**credentials)).json()
    for d in data:
        d["has_password"] = True if d["has_password"] == "true" else False
    return jsonify(data)

@app.route("/info/<id>")
def info_html(id):
    data = serverinfo(id)
    return render_template("info.html", d=data, title=data["name"])

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=24527, host="0.0.0.0")
