from lxml import html
from geopy.geocoders import Nominatim
import requests, re, folium, webbrowser, random
import stuff

"""Getter for Longitude and Latitude"""
def get_coordinates(location):
    geolocator = Nominatim()
    try:
        findit = geolocator.geocode(location) # Use Geolocator
        lat = findit.latitude                 # to get the long
        lon = findit.longitude                # and lat of the stuff
        coord = [lat, lon]
    except:
        coord = [45.5088, -73.5878]           # Sometimes it is "None"
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
        
"""
    Pass stuffs into an HTML page
    Post listings in map; LOOKS more complicated than it is
    Everytime this script runs, findit.html gets a new map
    Make sure python -m http.server is running in the directory
"""
def post_map(freestuffs): # Pass in freestuffs list
    #hexa = hex(random.randint(0, 16777215))[2:].upper() #maybe these are a waste of breathe
    #random_color = "#{0}".format(hexa)
    map_osm = folium.Map([45.5088, -73.5878], zoom_start=13) #Montreal's Mont Royal But this is Wrong. It should start at the long/lat of user_place
    radi = 700 # Having it start big and get small corrects overlaps
    for freestuff in freestuffs:  # Loop through the Stuff
        """
            This takes in the Freestuffs and puts it onto the map
        """
        place = freestuff.location                  # thing location
        thing = freestuff.thing                     # thing Title
        url = freestuff.url                         # thing URL
        image = "<img src=" + freestuff.image + "/>"# It Works! (images)
        color = sort_stuff(thing)                   #map marker's color
        # Name is the Map Posting, formating all this stuff...
        # Oooo.... I should use %s .format... ? No?
        name = image + "<br><h3>" + thing + "</h3><h4>" + place + "</h4><a href=" + url + " target='_blank'>View Posting in New Tab</a>"
        coordinates = get_coordinates(freestuff.location) # Get Coordinates Function is Above
        lat = coordinates[0] # It returns an array 0 = Latitude
        lon = coordinates[1] # and 1 = Longitude
        # This is the Map business
        map_osm.circle_marker(location=[lat, lon], radius=radi,
          popup=name, line_color="#000000",
          fill_color=color, fill_opacity=0.2)
        radi -= 60 # decrease the radius to be sure not to cover up older postings
    map_osm.create_map(path='webmap/findit.html') # needs a small server
    print("BEWARNED, this map is likely incorrect,\nCraigslist denizens care not for computer-precision")
    webbrowser.open_new_tab("localhost:8000/webmap/findit.html") # Open the map in a tab
