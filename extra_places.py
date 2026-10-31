"""Curated additions to places.json: well-known places missing from OSM extract + extra search aliases.

usage: python3 extra_places.py [places.json]   (idempotent; run after build_places.py)
"""
import json, sys, statistics

# name, category, lat, lon, address, aliases (";"-separated)
ADD = [
    ("Medeltidsmuseet", "Museum", 59.3283, 18.0712, "Strömparterren 3", "Stockholms medeltidsmuseum;Medieval Museum"),
    ("Thielska galleriet", "Museum", 59.3242, 18.1347, "Sjötullsbacken 8", "Thielska;Thiel Gallery"),
    ("Prins Eugens Waldemarsudde", "Museum", 59.3236, 18.1083, "Prins Eugens väg 6", "Waldemarsudde"),
    ("Magasin III", "Galleri", 59.3423, 18.1166, "Frihamnen", "Magasin 3"),
    ("Kaknästornet", "Sevärdhet", 59.3351, 18.1273, "Mörka kroken 28", "Kaknäs tower"),
    ("Artipelag", "Museum", 59.3063, 18.3477, "Artipelagstigen 1, Gustavsberg", ""),
    ("Rosendals trädgård", "Park", 59.3262, 18.1147, "Rosendalsterrassen 12", "Rosendals trädgårdskafé;Rosendal Garden"),
    ("Rosendals slott", "Sevärdhet", 59.3266, 18.1096, "", "Rosendal Palace"),
    ("Djurgårdsbrunn", "Område", 59.3327, 18.1310, "", "Djurgårdsbrunns värdshus"),
    ("Sturegallerian", "Köpcentrum", 59.3360, 18.0738, "Stureplan 4", ""),
    ("Sturebadet", "Badhus", 59.3362, 18.0741, "Sturegallerian 36", ""),
    ("Brunogallerian", "Köpcentrum", 59.3163, 18.0718, "Götgatan 36", "Bruno"),
    ("Skinnarviksberget", "Utsiktsplats", 59.3197, 18.0447, "", "Skinnarviksparken"),
    ("Lill-Jansskogen", "Park", 59.3515, 18.0660, "", "Lill-Jans"),
    ("Hammarbyskogen", "Park", 59.2905, 18.1055, "", ""),
    ("Beckholmen", "Ö", 59.3207, 18.1030, "", ""),
    ("Kvarnholmen", "Område", 59.3195, 18.1355, "", ""),
    ("Henriksdalsberget", "Område", 59.3115, 18.1105, "", ""),
    ("Globen City", "Område", 59.2948, 18.0795, "", "Globen Shopping"),
    ("Älta", "Område", 59.2580, 18.1790, "", "Älta centrum"),
    ("Tyresö centrum", "Köpcentrum", 59.2437, 18.2289, "", "Tyresö;Bollmora"),
    ("Tyresö slott", "Sevärdhet", 59.2272, 18.3013, "", ""),
    ("Tyresta nationalpark", "Naturreservat", 59.1800, 18.2950, "", "Tyresta;Tyresta by"),
    ("Gustavsberg", "Område", 59.3255, 18.3880, "", "Gustavsbergs hamn;Gustavsbergs porslinsfabrik"),
    ("Bosön", "Idrottsanläggning", 59.3786, 18.1925, "", "Bosön idrottsfolkhögskola"),
    ("Värtaterminalen", "Båt", 59.3505, 18.1085, "Värtahamnen", "Värtahamnen;Tallink Silja;Silja Line;Tallink"),
    ("Viking Line-terminalen", "Båt", 59.3165, 18.0920, "Stadsgårdskajen", "Stadsgårdsterminalen;Viking Line;Stadsgården;Stadsgårdskajen"),
    ("Ersta sjukhus", "Sjukhus", 59.3149, 18.0840, "Fjällgatan 44", "Ersta"),
    ("Boulevardteatern", "Teater", 59.3114, 18.0746, "Götgatan 73", ""),
    ("Fylkingen", "Kulturhus", 59.3164, 18.0588, "Torkel Knutssonsgatan 26", ""),
    ("Café Saturnus", "Kafé", 59.3393, 18.0700, "Eriksbergsgatan 6", "Saturnus"),
    ("Oaxen Krog", "Restaurang", 59.3215, 18.1015, "Beckholmsvägen 26", "Oaxen;Oaxen Slip"),
    ("Mood Stockholm", "Köpcentrum", 59.3350, 18.0705, "Regeringsgatan 48", "Mood;Mood gallerian"),
    ("Polishuset Kronoberg", "Polis", 59.3328, 18.0425, "Kungsholmsgatan 43", "Polishuset;Polisen Kronoberg;Kungsholmens polisstation"),
]

# (name, category[, area]) of an existing place -> aliases to add
ALIAS = {
    ("Sankt Görans sjukhus", "Sjukhus"): "Capio S:t Göran;S:t Göran;Capio Sankt Görans sjukhus",
    ("Karolinska universitetssjukhuset", "Sjukhus"): "Nya Karolinska;NKS",
    ("Karolinska Universitetssjukhuset Solna Barnakuten", "Sjukhus"): "Astrid Lindgrens barnsjukhus;ALB",
    ("Sankt Eriks ögonsjukhus", None): "S:t Eriks ögonsjukhus;S:t Eriks",
    ("Gustaf Vasa kyrka", "Kyrka"): "Gustav Vasa kyrka",
    ("Stockholms katolska domkyrka", "Kyrka"): "Sankt Eriks katolska domkyrka;Katolska domkyrkan",
    ("Forsgrenska", "Idrottsanläggning"): "Forsgrénska badet;Forsgrénska",
    ("Liljeholmsbadet", None): "Liljeholmens simhall",
    ("Västertorps sim- och idrottshall", None): "Västertorpsbadet;Västertorps simhall",
    ("Stockholms gamla observatorium", "Historisk plats"): "Observatoriet;Observatoriemuseet",
    ("Långholmen", "Hotell"): "Långholmens fängelse;Långholmen Hotell & Vandrarhem",
    ("Zinkensdamm", "Hotell"): "Zinkensdamms vandrarhem;STF Zinkensdamm",
    ("Radiohuset", "Byggnad"): "Sveriges Radio;SR",
    ("Waterfront Hotel", "Hotell"): "Radisson Waterfront;Radisson Collection Waterfront",
    ("Stockholmsmässan", "Mässa"): "Victoriahallen;Stockholm International Fairs;Älvsjömässan",
    ("Ersta Sköndal högskola", "Högskola"): "Marie Cederschiöld högskola;Ersta Sköndal Bräcke högskola",
    ("Handelshögskolan", "Universitet"): "Stockholm School of Economics;SSE;Handels",
    ("Moderna museet", None): "Museum of Modern Art;Moderna",
    ("Riksdagshuset", None): "Parliament;Swedish Parliament;Riksdagen",
    ("Kista", "Område"): "Kista Science City",
    ("Cirkus", "Teater"): "Cirkus Arena;Cirkus Djurgården",
    ("Riksidrottsmuseum", "Museum"): "Riksidrottsmuseet",
    ("Gröna Lund", "Nöjespark"): "Gröna Lunds tivoli",
    ("Skycity", "Flygplats"): "Arlanda flygplats;Stockholm Arlanda Airport;Arlanda Airport;ARN",
    ("Bromma flygplats", "Flygplats"): "Stockholm Bromma Airport;BMA",
    ("IKEA", "Möbler", "Jakobsberg"): "IKEA Barkarby;Barkarby handelsplats",
}
FIX = {"tockholm School of Economics": None}  # broken alias from the OSM extract


def main(path):
    d = json.load(open(path, encoding="utf-8"))
    cats, P = d["cats"], d["p"]
    lat0, lon0 = d["lat0"], d["lon0"]
    wcat = {}
    for p in P:
        wcat.setdefault(p[1], []).append(p[7])

    def add_alias(p, extra):
        cur = [a for a in (p[6] or "").split(";") if a and a not in FIX]
        for a in extra.split(";"):
            if a and a not in cur and a != p[0]:
                cur.append(a)
        p[6] = ";".join(cur)

    n_alias = 0
    for key, extra in ALIAS.items():
        name, cat, area = (key + (None,))[:3]
        hit = False
        for p in P:
            if p[0] == name and (cat is None or cats[p[1]] == cat) and (area is None or (p[4] >= 0 and d["areas"][p[4]] == area)):
                add_alias(p, extra); hit = True
        if hit:
            n_alias += 1
        else:
            print("alias target not found:", name, cat, file=sys.stderr)
    for p in P:
        if p[6] and any(f in p[6].split(";") for f in FIX):
            add_alias(p, "")

    have = {(p[0], cats[p[1]]) for p in P}
    n_add = 0
    for name, cat, lat, lon, addr, al in ADD:
        if (name, cat) in have:
            continue
        if cat not in cats:
            cats.append(cat)
        ci = cats.index(cat)
        la, lo = round((lat - lat0) * 1e5), round((lon - lon0) * 1e5)
        near = min(P, key=lambda p: (p[2] - la) ** 2 + ((p[3] - lo) * 0.5) ** 2)
        w = round(statistics.median(wcat.get(ci, [50])))
        P.append([name, ci, la, lo, near[4], addr, al, w])
        n_add += 1
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"extra_places: +{n_add} places, aliases on {n_alias} targets")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "places.json")
