from stuff import Stuff
from geopy.geocoders import Nominatim
import folium
import sys

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

def post_map(freestuffs):
	map_osm = folium.Map([45.5088, -73.5878], 13) #Montreal
	for freestuff in freestuffs: #sooo will this work? 
		#holy shit I can't believe it worked
		place = freestuff.location
		name = freestuff.thing
		url = freestuff.url
		try:
			coordinates = get_coordinates(freestuff.location)
			print(coordinates)
		except:
			print("nope")

		print(name, url, place)
		#well, it runs but it doesn't load
		map_osm.circle_marker(location=coordinates, radius=15,
                  popup=name, line_color='#3186cc',
                  fill_color='#3186cc', fill_opacity=0.2)
	map_osm.create_map(path='findit.html') #open this 
