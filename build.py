"""Build dist/index.html (+ places.json) from the pipeline outputs.

usage: python3 build.py            (expects the pipeline scratch dir in $FEB_SP)
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.environ.get("FEB_SP")
if not SP:
    sys.exit("set FEB_SP to the pipeline scratch dir")
OSM = os.path.join(SP, "osm")
PIPE = os.path.join(SP, "pipeline")
VER = os.path.join(SP, "verify")
DIST = os.path.join(HERE, "dist")
os.makedirs(DIST, exist_ok=True)

st_json = os.path.join(SP, "stations_build.json")
subprocess.run([sys.executable, os.path.join(PIPE, "build_stations.py"), OSM, VER, st_json], check=True)
places_json = os.path.join(DIST, "places.json")
if "--skip-places" not in sys.argv or not os.path.exists(places_json):
    subprocess.run([sys.executable, os.path.join(PIPE, "build_places.py"), OSM, places_json], check=True)

data = json.load(open(st_json))
places = json.load(open(places_json))
# example destination shown on first load
example = None
for p in places["p"]:
    if p[0] == "Södersjukhuset" and places["cats"][p[1]] == "Sjukhus":
        example = {"name": p[0], "cat": "Sjukhus", "sub": p[5] or "Sjukhusbacken 10, Stockholm",
                   "lat": round(places["lat0"] + p[2] / 1e5, 5), "lon": round(places["lon0"] + p[3] / 1e5, 5)}
        break
data["example"] = example
data["placesUrl"] = "places.json"
blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

src = open(os.path.join(HERE, "src", "app.html"), encoding="utf-8").read()
assert "/*__STATIONS__*/" in src
page = src.replace("/*__STATIONS__*/", blob)
open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(page)
# local preview wrapper (the artifact host adds its own skeleton)
local = ('<!doctype html><html lang="sv"><head><meta charset="utf-8">'
         '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>' + page + "</body></html>")
open(os.path.join(DIST, "local.html"), "w", encoding="utf-8").write(local)
print("index.html", os.path.getsize(os.path.join(DIST, "index.html")) // 1024, "KB; places.json", os.path.getsize(places_json) // 1024, "KB")
