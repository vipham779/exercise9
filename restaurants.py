"""
This script returns a json file containing the locations of restaurants around
a given address
Command line: python3 restaurants [INTEGER]
If you want to return 30 restaurants, please input python3 restaurants 30
"""


import requests
import ast
import geojson
import time
import sys


pymi_lat, pymi_lng = 10.8162109, 106.6941154
radius = 2000
type = "restaurant"
API_key = key


def request(token=None):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": "{},{}".format(pymi_lat, pymi_lng),
        "radius": radius,
        "type": type,
        "token": token,
        "key": API_key,
    }
    return requests.get(url, params=params).json()


def restaurants(resp):
    features = []
    for elem in resp["results"]:
        temp = {}
        temp.update({"type": "Feature"})
        temp.update(
            {
                "geometry": {
                    "type": "Point",
                    "coordinates": ast.literal_eval(
                        "[{}, {}]".format(
                            elem["geometry"]["location"]["lng"],
                            elem["geometry"]["location"]["lat"],
                        )
                    ),
                }
            }
        )
        temp.update({"properties": {"name": elem["name"], "address": elem["vicinity"]}})
        features.append(temp)
    return features


def n_restaurants(n):
    token = None
    features = []
    for _ in range(int(n) // 20 + 1):
        resp = request(token)
        time.sleep(1)
        features.extend(restaurants(resp))
        if "next_page_token" in resp.keys():
            token = resp["next_page_token"]
    result = {"type": "FeatureCollection", "features": features[: int(n)]}
    return result


def main():
    if len(sys.argv) < 2:
        print("Please input with the format: python3 restaurants.py [INTEGER]")
        sys.exit()
    else:
        n = sys.argv[1]
        with open("restaurants.geojson", "w", encoding="utf-8") as f:
            geojson.dump(n_restaurants(n), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
