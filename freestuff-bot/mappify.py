###########################################################################
# Copyright (C) 2015 Fenimore Love <fenimore@polypmer.com>
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
###

from geopy.geocoders import Nominatim
import requests, re, folium, webbrowser
import stuff

# TODO: Method for taking user input and starting
# The map on that location, otherwise this won't work
# For cities other than Montreal
# TODO: post_map ought to take two params:
# list of freestuffs AND the location
# This location would also go into the
# TODO: get_coordinates method
# Reverse Geolocator is at nominatim.openstreetmap.org

"""Getter for Longitude and Latitude"""
def get_coordinates(location): # TODO: take in USER LOCATION
    geolocator = Nominatim()
    try:
        findit = geolocator.geocode(location) # Use Geolocator
        lat = findit.latitude                 # to get the long
        lon = findit.longitude                # and lat of the stuff
        coord = [lat, lon]
    except:
        coord = set_city_center(location) # [45.5088, -73.5878]?
    return coord
    
"""Setter for Starting Longitude Latitude"""
def set_city_center(location):
    geolocator = Nominatim()
    if re.match("montreal", location, re.I):
        coord = [45.5088, -73.5878] # Montreal Center
    if re.match("newyork", location, re.I):
        coord = [40.7127, -74.0058] # New York Center
    else:
        try:
            findit = geolocator.geocode(location) # Use Geolocator
            lat = findit.latitude                 # to get the long
            lon = findit.longitude                # and lat of the stuff
            coord = [lat, lon]
        except:
            coord = [0,0] # This is a bit silly
    return coord

"""Rendering the Map pretty Colors""" # TODO: Read about if statements 
def sort_stuff(stuff):
    furniture_pattern = "(wood|shelf|table|chair|scrap)"
    electronics_pattern = "(tv|sony|écran|speakers)" #search NOT match
    find_pattern = "(book|games|cool)"  
    if re.search(furniture_pattern, stuff, re.I):
        return "#FF0000" #red ##### THIS should set variable and return at
    if re.search(electronics_pattern, stuff, re.I): #the end all
        return "#3186cc" #blue at once
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
    user_location = freestuffs[0].user_location
    start_coord = set_city_center(user_location)
    center_lat = start_coord[0]
    center_lon = start_coord[1]
    map_osm = folium.Map([center_lat, center_lon], zoom_start=13) 
    radi = 700 # Having it start big and get small corrects overlaps
    for freestuff in freestuffs:  
        # Loop through the Stuff and Post it
        place = freestuff.location  # thing location
        thing = freestuff.thing     # thing Title
        url = freestuff.url         # thing URL
        image = freestuff.image     # It Works! (images)
        color = sort_stuff(thing)   # Map marker's color
        # Name is Map Posting
        name = """
                <img src='%s' height='auto' width='160px' />
                <h3>%s</h3>
                <h4>%s</h4>
                <a href='%s' target='_blank'>View Posting in New Tab</a>
               """ % (image, thing, place, url)
        coordinates = get_coordinates(freestuff.location) # Get Coordinates Function is Above
        # TODO: Contigency Plan for 0, 0?
        lat = coordinates[0] # It returns an array 0 = Latitude
        lon = coordinates[1] # and 1 = Longitude
        # This is the Map business with many options
        map_osm.circle_marker(location=[lat, lon], radius=radi,
          popup=name, line_color="#000000",
          fill_color=color, fill_opacity=0.2)
        radi -= 60 # decrease the radius to be sure not to cover up older postings
    map_osm.create_map(path='webmap/findit.html') # needs a small server
    print("BEWARNED, this map is likely incorrect,\nCraigslist denizens care not for computer-precision")
    webbrowser.open_new_tab("localhost:8000/webmap/findit.html") # Open the map in a tab
