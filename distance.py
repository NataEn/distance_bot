from math import radians, cos, sin, asin, sqrt
import typing, requests, collections, copy
from pprint import pprint

BASE = "https://nominatim.openstreetmap.org/search"
params = {
    'q': '',
    'format': 'json',
    'limit': 1,
}
ADDRESS1 = 'hifa'


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def geocode(name: str) -> typing.Tuple[float, float]:
    params['q'] = name
    r = requests.get(BASE, params)
    data = r.json()
    print(float(data[0]['lon']), float(data[0]['lat']))
    return (float(data[0]['lon']), float(data[0]['lat']))


def get_distance_from_hifa(toA, fromA=ADDRESS1):
    address1 = geocode(toA)
    address2 = geocode(fromA)
    distance = haversine(*address1, *address2)
    return f'your distance is: {distance:.2f} km'


print(get_distance_from_hifa('aaaaaa'))

base = 'https://en.wikipedia.org/wiki/'
user = 'Chuck_Norris'


def get_age(name: str) -> int:
    response = requests.get(base + name)
    data = response.text
    index = data.find('(age&#160;')
    if index < 1:
        return "Celeb not found"
    else:
        return data[index + 10:index + 12]
