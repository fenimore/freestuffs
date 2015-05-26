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
# TODO: No-Image image?

"""Getter for Longitude and Latitude"""
def get_coordinates(location): # TODO: take in USER LOCATION
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
    if re.match(furniture_pattern, stuff, re.I):
        return "#FF0000" #red
    if re.match(electronics_pattern, stuff, re.I):
        return "#3186cc" #blue
    if re.match(find_pattern, stuff, re.I):
        return "#000000" #black
    else:
        return "#FFFFFF" #white
        
"""
    Pass stuffs into an HTML page
    Post listings in map; LOOKS more complicated than it is
    Everytime this script runs, findit.html gets a new map
    Make sure python -m http.server is running in the directory
"""
def post_map(freestuffs): # Pass in freestuffs list TODO: Take in User Location
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
