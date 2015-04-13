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
	map_osm = folium.Map([45.5088, -73.5878]) #Montreal
	for freestuff in freestuffs: #sooo will this work? 
		#holy shit I can't believe it worked
		place = freestuff.location
		thing = freestuff.thing
		url = freestuff.url
		image = "imagessss"
		name = image + "<br><h3>" + thing + "</h3><a href=" + url + " target='_blank'>view ad</a>"
		try:
			coordinates = get_coordinates(freestuff.location)
			lat = coordinates[0]
			lon = coordinates[1]
			print(coordinates)
		except:
			print("nope")

		print(name, url, place)
		#well, it runs but it doesn't load
		map_osm.circle_marker(location=[lat, lon], radius=300,
                  popup=name, line_color='#3186cc',
                  fill_color='#3186cc', fill_opacity=0.2)
	map_osm.create_map(path='findit.html') #open this 
