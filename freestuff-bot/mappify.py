#!/usr/bin/env python
"""Chart where free things are.

The reverse Geolocator is at nominatim.openstreetmap.org.

Example usage:
    from stuffify import Stuffify
    freestuffs = Stuffify('montreal', 5, precise=True).get_freestuffs()
    map = Mappify(freestuffs, is_testing=True)
    
@author: Fenimore Love
@license: MIT
@date: 2015-2016

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import os, re
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import requests, folium, webbrowser
from folium.element import IFrame


class Mappify:
    """Post folium map of freestuffs.

    After constructing Mappify map object, call
    create_map and pass in map_path in order to create 
    the HTML map.
    
    Attributes:
        - treasure_map -- an OSM folium map object
    """
    def __init__(self, freestuffs, address=None, zoom=13, 
                 is_testing=False, is_flask=False):
        """Post freestuffs on map.
        
        Make sure python -m http.server is running the directory.
        The circle markers diminish in size, so that they
        do not cover newer markers.
        
        Keyword arguments:
            - freestuffs -- a collection of stuff objects generated with
                            Stuffify
            - address -- for an optional map marker of the user address.
            - is_testing -- use to test module from commandline
            - is_flask -- automatically create map for treasure-map
            - zoom -- the map default zoom level
            
        Attributes:
            - name -- freestuff marker blurb
        """
        user_location = freestuffs[0].user_location
        start_coord = self.set_city_center(user_location)
        center_lat = start_coord[0]
        center_lon = start_coord[1] 
        map_osm = folium.Map([center_lat, center_lon], zoom_start=zoom) 
        radi = 500 
        for freestuff in freestuffs:
            place = freestuff.location  # thing location
            thing = freestuff.thing     # thing title
            url = freestuff.url         # thing URL
            image = freestuff.image     # thing image url
            color = self.sort_stuff(thing)   # Map marker's color
            name = """
                    <link rel='stylesheet' type='text/css' 
                    href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css'>
                    <img src='%s' height='auto' width='160px' />
                    <h3>%s</h3>
                    <h4>%s</h4>
                    <a href='%s' target='_blank'>View Posting in New Tab</a>
                   """ % (image, thing, place, url)
            # TODO: Contigency Plan for 0, 0?
            lat = freestuff.coordinates[0] # Latitude
            lon = freestuff.coordinates[1] # Longitude
            popup = folium.Popup(IFrame(name, width=200, height=300),
                                 max_width=3000)
            folium.CircleMarker([lat, lon], radius=radi, popup=popup,
                                fill_color=color, fill_opacity=0.2).add_to(map_osm)
            radi -= 10 # Diminishing order
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
                          icon=folium.Icon(color='red',icon='home')
                          ).add_to(map_osm)
        self.treasure_map = map_osm
        if is_testing:
            self.create_test_map()
        elif is_flask:
            self.create_flask_map()
        else:
            print("call create_map(_path) and pass in path to create map")
        
    
    def create_test_map(self):
        """Create html map in local webmap directory.
        
        Must have python -m http.server running in directory
        """
        path = os.getcwd()
        if not os.path.exists(os.path.join(path, 'webmap')):
            os.makedirs(directory)
        self.treasure_map.save(os.path.join(path, 'webmap', 'findit.html')) # depecrated, change to save
        print("BEWARNED, this map is likely incorrect:\nCraigslist denizens care not for computer-precision")
        # webbrowser.open_new_tab("localhost:8000/webmap/findit.html") # Open the map in a tab
        
        
    def create_flask_map(self):
        """Create html map in flask server."""
        folium_figure = self.treasure_map.get_root()
        folium_figure.header._children['bootstrap'] = folium.element.CssLink('/static/css/style.css')
        folium_figure.header._children['Woops'] = folium.element.CssLink('/static/css/map.css') # Why woops?
        self.treasure_map.save('treasuremap/templates/raw_map.html') # TODO: use join
        
        
    def create_map(self, map_path, css_path=None):
        """Create html map in _path.
        
        Keyword arguments:
            - map_path -- the path to create_map in
            - css_path -- the path to override css 
                          (defaults to bootstrap via folium)
        """
        if css_path is not None:
            folium_figure = self.treasure_map.get_root() # So that Leaflet Style Doesn't conflict with custom Bootstrap
            folium_figure.header._children['Woops'] = folium.element.CssLink(css_path)
        self.treasure_map.save(map_path)
        
        
    def set_city_center(self, location):
        """Setter for center longitude latitude."""
        geolocator = Nominatim()
        if re.match("montreal", location, re.I):
            coord = [45.5088, -73.5878] 
        elif re.match("newyork", location, re.I):
            coord = [40.7127, -74.0058] 
        elif re.match("toronto", location, re.I):
            coord = [43.7, -79.4000] 
        elif re.match("washingtondc", location, re.I):
            coord = [38.9047, -77.0164]
        elif re.match("vancouver", location, re.I):
            coord = [49.2827, -123.1207]
        elif re.match("sanfrancisco", location, re.I):
            coord = [37.773972, -122.431297]
        else:
            try:
                findit = geolocator.geocode(location) # Last resort
                lat = findit.latitude                 
                lon = findit.longitude                
                coord = [lat, lon]
            except:
                coord = [0,0] # This is a bit silly, nulle island
        return coord


    def sort_stuff(self, stuff): # This doesn't work...
        """Rendering the markers in pretty colors."""
        color = ""
        furniture_pattern = "(wood|shelf|table|chair|scrap)"
        electronics_pattern = "(tv|sony|écran|speakers)" #search NOT match
        find_pattern = "(book|games|cool)"
        if re.search(furniture_pattern, stuff, re.I):
            color = "#FF0000" #red ##### THIS should set variable and return at
        elif re.search(electronics_pattern, stuff, re.I): #the end all
            color = "#3186cc" #blue at once
        elif re.search(find_pattern, stuff, re.I):
            color = "#000000" #black
        else:
            color = "white" #white
        color = "#ffff00"
        return color
