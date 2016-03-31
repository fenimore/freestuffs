###########################################################################
# Copyright (C) 2015 Fenimore Love
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

import os
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import requests, re, folium, webbrowser
import stuff
from folium.element import IFrame

# TODO: Only Supporting Montreal, NY and Toronto
# Why Toronot even?
# For cities other than Montreal
# Reverse Geolocator is at nominatim.openstreetmap.org
# Is there a different way of sending this stuff onto
# A javscript map thang? I have the coordinates
# There must be other ways.

"""Getter for Longitude and Latitude"""
def get_coordinates(freestuff):
    geolocator = Nominatim()
    follow_this = freestuff.url
    follow_page = requests.get(follow_this)
    follow_soup = BeautifulSoup(follow_page.text)
    location = follow_soup.find("div", class_="viewposting")
    if location is not None:
        lat = location['data-latitude']
        lon = location['data-longitude']
    else:
        try:
            lat = geolocator.geocode(freestuff.location).latitude
            lon = geolocator.geocode(freestuff.location).longitude
        except:
            try:
                lat = geolocator.geocode(freestuff.user_location).latitude
                lon = geolocator.geocode(freestuff.user_location).longitude
            except:
                lat = 38.9047 # This is DC
                lon = -77.0164
    return [lat, lon]

"""Setter for Starting Longitude Latitude"""
def set_city_center(location):
    geolocator = Nominatim()
    if re.match("montreal", location, re.I):
        coord = [45.5088, -73.5878] # Montreal Center
    elif re.match("newyork", location, re.I):
        coord = [40.7127, -74.0058] # New York Center
    elif re.match("toronto", location, re.I):
        coord = [43.7, -79.4000] # Toronto? Center TODO:
    elif re.match("washingtondc", location, re.I):
        coord = [38.9047, -77.0164]
    elif re.match("vancouver", location, re.I):
        coord = [49.2827, -123.1207]
    elif re.match("sanfrancisco", location, re.I):
        coord = [37.773972, -122.431297]
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
def sort_stuff(stuff): # This doesn't work...
    color = ""
    furniture_pattern = "(wood|shelf|table|chair|scrap)"
    electronics_pattern = "(tv|sony|écran|speakers)" #search NOT match
    find_pattern = "(book|games|cool)"
    if re.search(furniture_pattern, stuff, re.I):
        color = "#FF0000" #red ##### THIS should set variable and return at
    if re.search(electronics_pattern, stuff, re.I): #the end all
        color = "#3186cc" #blue at once
    if re.search(find_pattern, stuff, re.I):
        color = "#000000" #black
    else:
        color = "white" #white
    color = "#ffff00"
    return color
        
"""
    Pass stuffs into an HTML page
    Post listings in map; LOOKS more complicated than it is
    Everytime this script runs, findit.html gets a new map
    Make sure python -m http.server is running in the directory
"""
def post_map(freestuffs, address=None): # Pass in freestuffs list
    # TODO: This part sucks
    user_location = freestuffs[0].user_location
    start_coord = set_city_center(user_location)
    center_lat = start_coord[0]
    center_lon = start_coord[1]
    ######## 
    map_osm = folium.Map([center_lat, center_lon], zoom_start=13) 
    # Look into Folium for real, so this is a Folium
    # Object filled with map markers
    radi = 500 # Having it start big and get small corrects overlaps
    for freestuff in freestuffs:
        # Loop through the Stuff and Post it
        place = freestuff.location  # thing location
        thing = freestuff.thing     # thing Title
        url = freestuff.url         # thing URL
        image = freestuff.image     # It Works! (images)
        color = sort_stuff(thing)   # Map marker's color
        # Name is Map Posting
        name = """
                <link rel='stylesheet' type='text/css' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css'>
                <img src='%s' height='auto' width='160px' />
                <h3>%s</h3>
                <h4>%s</h4>
                <a href='%s' target='_blank'>View Posting in New Tab</a>
               """ % (image, thing, place, url)
        coordinates = get_coordinates(freestuff) # Get Coordinates Function is Above
        # TODO: Contigency Plan for 0, 0?
        lat = coordinates[0] # It returns an array 0 = Latitude
        lon = coordinates[1] # and 1 = Longitude
        # This is the Map business with many options
        popup = folium.Popup(IFrame(name, width=200, height=300), max_width=3000)
        folium.CircleMarker([lat, lon], radius=radi, popup=p,
            fill_color=color, fill_opacity=0.2).add_to(map_osm)
        radi -= 10 # decrease the radius to be sure not to cover up newer postings
    if address != None:
        geolocator = Nominatim()
        try:
            add_lat = geolocator.geocode(address).latitude
            add_lon = geolocator.geocode(address).longitude
        except:
            add_lat = 0
            add_lon = 0
        pop_up = address + str(add_lat) + str(add_lon)
        folium.Marker(location=[add_lat, add_lon],popup=address,
            icon=folium.Icon(color='red',icon='home')).add_to(map_osm)
    # So that Leaflet Style Doesn't conflict with custom Bootstrap
    folium_figure = map_osm.get_root()
    folium_figure.header._children['bootstrap'] = folium.element.CssLink('/static/css/style.css')
    folium_figure.header._children['Woops'] = folium.element.CssLink('/static/css/map.css')
    path = os.getcwd() # For testing!
    map_osm.create_map(path= path + 'webmap/findit.html') # needs a small server

    print("BEWARNED, this map is likely incorrect,\nCraigslist denizens care not for computer-precision")
    webbrowser.open_new_tab("localhost:8000/webmap/findit.html") # Open the map in a tab
