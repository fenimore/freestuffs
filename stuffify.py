from stuff import Stuff
from geopy.geocoders import Nominatim
import folium, sys, re
from random import randint
# cool kids import all at once

# stuff constructor
def gather_stuff(thing, url, location): #what if I refined the location here?
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
    electronics_pattern = "(tv|sony|écran|speakers|books)" #these aren't working
    if re.match(furniture_pattern, stuff, re.I):
        return "#FF0000" #red
    if re.match(electronics_pattern, stuff, re.I):
        return "#3186cc" #blue
    else:
        return "#FFFFFF" #white

#Refine Craigslist's pitiful location specifications
def refine_location(place): #this should be a switch!!!
    if place == "montreal, Montréal":#poster didn't specify where in Montreal
        refinition = "Montréal, Somewhere"
    if place == "Montreal, Montréal":#poster didn't specify where in Montreal
        refinition = "Montréal, Somewhere"
    else: refinition = place
    return refinition #slick word, huh?

#Post listings in terminal
def post_listings(freestuffs): #for now, print but later i'll list on html page
    for freestuff in freestuffs:
        output = str(freestuff) #locations aren't refined
        print(output)

#Post listings in map; looks more complicated than it is
#Everytime this script runs, findit.html gets a new map
def post_map(freestuffs):
    map_osm = folium.Map([45.5088, -73.5878], zoom_start=13) #Montreal's Mont Royal
    radi = 700 #this corrects overlapping stuffs
    for freestuff in freestuffs:                    #loop through stuffs
        place = refine_location(freestuff.location) #location
        thing = freestuff.thing                     #thing
        url = freestuff.url                         #link
        image = "imagessss"                         #"<img src="freestuff.image "/>"
        color = sort_stuff(thing)                   #map marker color
        # name is the map posting --- add img src tag
        name = image + "<br><h3>" + thing + "</h3><h4>" + place + "</h4><a href=" + url + " target='_blank'>view ad</a>"
        try:
            coordinates = get_coordinates(freestuff.location)#get coords returns a list (lat = 0 lon = 1)
            lat = coordinates[0]
            lon = coordinates[1]
        except: #put it on the mountain somewhere if it's "somewhere"
            lat = 45.5088
            lon = -73.5878
        map_osm.circle_marker(location=[lat, lon], radius=radi,
          popup=name, line_color='#000000',
          fill_color=color, fill_opacity=0.2)
        radi -= 60 #decrease the radius to show older postings
    map_osm.create_map(path='findit.html') #open this 
