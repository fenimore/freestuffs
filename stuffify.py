from stuff import Stuff
from geopy.geocoders import Nominatim

def gather_stuff(thing, url, location):
    stuff = Stuff(thing, url, location)
    return stuff

def get_coordinates(location):
    geolocator = Nominatim()
    findit = geolocator.geocode(location)
    lat = findit.latitude
    lon = findit.longitude
    coord = [lat, lon]
    return coord
