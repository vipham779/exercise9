'''
'''


import requests
import ast
import geojson


pymi_lat, pymi_lng = 10.8162109, 106.6941154
radius = 2000
type = "restaurant"
API_key = 'AIzaSyAnSkQYiHpykhKvkeBA1vbuQzSUEHrc4lQ'

def request(pagetoken=None):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": "{},{}".format(pymi_lat, pymi_lng),
        "radius": radius,
        "type": type,
        "pagetoken": pagetoken,
        "key": API_key,
    }
    return requests.get(url, params=params).json()


def restaurants(pagetoken=None):
    data = request(pagetoken)
    features = []
    for elem in data['results']:
        temp = {}
        temp.update({'type': 'Feature'})
        temp.update({'geometry': {'type': 'Point','coordinates' : ast.literal_eval('[{}, {}]'.format(elem['geometry']['location']['lat'],elem['geometry']['location']['lng']))}})
        temp.update({'properties': {'name': elem['name'], 'address': elem['vicinity']}})
        features.append(temp)
    return features


def n_restaurants(n):
    token1=None
    features = []
    for _ in range(n//20):
        resp = request(token1)
        features.extend(restaurants(token1))
        if 'next_page_token' in resp.keys():
            token1 = resp['next_page_token']
    result = {'type': 'FeatureCollection', 'features': features}
    return result

if __name__ == '__main__':
    with open('pymi_beer.geojson', 'w', encoding='utf-8') as f:
        geojson.dump(n_restaurants(40), f, ensure_ascii=False, indent=4)



