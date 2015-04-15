from stuff import Stuff
from geopy.geocoders import Nominatim
import folium, sys, re
from random import randint
# cool kids import all at once

# stuff constructor
def gather_stuff(thing, url, location):
    stuff = Stuff(thing, url, location)
    return stuff

# getter for longitude and latitude
def get_coordinates(location):
    geolocator = Nominatim()
    findit = geolocator.geocode(location)
    lat = findit.latitude
    lon = findit.longitude
    coord = [lat, lon]
    return coord
    
#Returns the color for map rendering
def sort_stuff(stuff):
    furniture_pattern = "(wood|shelf|table|chair|scrap)"
    electronics_pattern = "(TV|tv|sony|Écran|speakers)"

    if re.match(furniture_pattern, stuff, re.I):
        return "#FF0000" #red
    if re.match(electronics_pattern, stuff, re.I):
        return "#3186cc" #blue
    else:
        return "#FFFF00" #yellow

def post_map(freestuffs):
	map_osm = folium.Map([45.5088, -73.5878], zoom_start=13) #Montreal
	for freestuff in freestuffs: #sooo will this work? 
		#holy shit I can't believe it worked
		place = freestuff.location
		if place == "Montréal, Montréal":
			place = "Montréal, Somewhere"
			randomlat = randit(45.5040, 45.5090)
			randomlon = randit(-73.5880, -73.5840)
			lat = randomlat
			lon= randomlon
			#poster didn't specify where in Montreal
		thing = freestuff.thing
		url = freestuff.url
		image = "imagessss" #"<img src="freestuff.image "/>"
		#plug image url then src it in an img tag
		# name is the map posting add img src tag
		name = image + "<br><h3>" + thing + "</h3><h4>" + place + "</h4><a href=" + url + " target='_blank'>view ad</a>"
		try:
			coordinates = get_coordinates(freestuff.location)#get coords returns a list (lat = 0 lon = 1)
			lat = coordinates[0]
			lon = coordinates[1]
		except:	#put it on the mountain if it's "somewhere"
			lat = 45.5088
			lon = -73.5878

		#print(thing, place)
		#TODO: Change color according to regex 
		#		searches of furniture/electronics/etc
		#		link to image src.... ooooo that'd be slick
		# color = sort_stuff(thing)
		color = sort_stuff(thing)
		
		map_osm.circle_marker(location=[lat, lon], radius=300,
                  popup=name, line_color=color,
                  fill_color=color, fill_opacity=0.2)
		
	map_osm.create_map(path='findit.html') #open this 
