from lxml import html
from geopy.geocoders import Nominatim
import requests, re, folium, webbrowser, random
import stuff

"""Getter for Longitude and Latitude"""
def get_coordinates(location):
    geolocator = Nominatim()
    try:
        findit = geolocator.geocode(location)
        lat = findit.latitude
        lon = findit.longitude
        coord = [lat, lon]
    except:
        coord = [45.5088, -73.5878]
    return coord

"""Rendering the Map pretty Colors"""
def sort_stuff(stuff):

    furniture_pattern = "(wood|shelf|table|chair|scrap)"
    electronics_pattern = "(tv|sony|écran|speakers)" #search NOT match
    find_pattern = "(book|games|cool)"               #sooo these are what I'm looking for?
    if re.search(furniture_pattern, stuff, re.I):
        return "#FF0000" #red
    if re.search(electronics_pattern, stuff, re.I):
        return "#3186cc" #blue
    if re.search(find_pattern, stuff, re.I):
        return "#000000" #black
    else:
        return "#FFFFFF" #white
        
# Post listings in map; looks more complicated than it is
# Everytime this script runs, findit.html gets a new map
"""Pass stuffs into an HTML page"""
def post_map(freestuffs): # Pass in freestuffs list
    #hexa = hex(random.randint(0, 16777215))[2:].upper() #maybe these are a waste of breathe
    #random_color = "#{0}".format(hexa)
    map_osm = folium.Map([45.5088, -73.5878], zoom_start=13) #Montreal's Mont Royal But this is Wrong
                                                              #It should start at the long/lat of user_place
    radi = 700 #this corrects overlapping stuffs
    for freestuff in freestuffs:                    #loop through stuffs
        """
            This takes in the Freestuff and puts it onto the map
            the image bit isn't working (still, but I have hope with bs4
        """
        place = freestuff.location                  #location
        thing = freestuff.thing                     #thing
        url = freestuff.url                         #link
        image = freestuff.image                     # "<img src="freestuff.image "/>"
        color = sort_stuff(thing)                   #map marker color
        # name is the map posting --- add img src tag
        name = image + "<br><h3>" + thing + "</h3><h4>" + place + "</h4><a href=" + url + " target='_blank'>view ad</a>"
        #try:
        coordinates = get_coordinates(freestuff.location)#get coords returns a list (lat = 0 lon = 1)
        lat = coordinates[0]
        lon = coordinates[1]
        #except: #put it on the mountain somewhere if it's "somewhere"
        #    lat = 45.5088
        #    lon = -73.5878
        map_osm.circle_marker(location=[lat, lon], radius=radi,
          popup=name, line_color="#000000",
          fill_color=color, fill_opacity=0.2)
        radi -= 60 #decrease the radius to be sure not to cover up older postings
    map_osm.create_map(path='webmap/findit.html') #open this ... but it needs a small server running etc whatevs
    print("BEWARNED, this map is likely incorrect,\nCraigslist denizens care not for computer-precision")
    webbrowser.open_new_tab("localhost:8000/webmap/findit.html") # Does it work?
