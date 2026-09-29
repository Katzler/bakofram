"""Turn dist/index.html (artifact-style fragment) into a standalone site folder with icons + manifest."""
import json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
page = open(os.path.join(HERE, "dist", "index.html"), encoding="utf-8").read()
i = page.index('<div class="wrap">')
head_extra = """<link rel="icon" type="image/png" sizes="32x32" href="icons/icon-32.png?v=2">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png?v=2">
<link rel="manifest" href="manifest.webmanifest">
<meta name="apple-mobile-web-app-title" content="Fram/bak">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
"""
out = ('<!doctype html>\n<html lang="sv">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + page[:i] + head_extra + '</head>\n<body>\n' + page[i:] + '\n</body>\n</html>\n')
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(out)
shutil.copy(os.path.join(HERE, "dist", "places.json"), OUT)
os.makedirs(os.path.join(OUT, "icons"), exist_ok=True)
for src, dst in [("i180", "apple-touch-icon"), ("i32", "icon-32"), ("i192", "icon-192"), ("i512", "icon-512"), ("m512", "icon-maskable-512")]:
    shutil.copy(os.path.join(HERE, "icons", src + ".png"), os.path.join(OUT, "icons", dst + ".png"))
json.dump({"name": "Fram eller bak?", "short_name": "Fram/bak", "start_url": "./", "scope": "./", "display": "standalone",
           "background_color": "#0d131c", "theme_color": "#0d131c", "lang": "sv",
           "icons": [{"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                     {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
                     {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]},
          open(os.path.join(OUT, "manifest.webmanifest"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
shutil.copy(os.path.join(HERE, "src", "app.html"), os.path.join(OUT, "src", "app.html"))
print("site written to", OUT)
