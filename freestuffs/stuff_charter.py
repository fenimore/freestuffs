#!/usr/bin/env python
"""Chart where free things are.

The reverse Geolocator is at nominatim.openstreetmap.org.

Example usage:
    from stuff_scraper import StuffScraper
    freestuffs = StuffScraper('montreal', 5, precise=True).stuffs
    osm_map = Mappify(freestuffs).treasure_map
    
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


class StuffCharter:
    """Post folium map of freestuffs.

    After constructing Mappify map object, call
    create_map and pass in map_path in order to create 
    the HTML map.
    
    Attributes:
        - treasure_map -- an OSM folium map object
        - stuffs -- list of free stuff
        - user_location -- the user's location
        - start_coordinates -- the origin coordinates for city
        - zoom -- default map zoom
        
    Keyword arguments:
        - stuffs -- a collection of stuff objects 
                        generated with StuffScraper
        - address -- for an optional map marker of the user address.
        - is_testing -- use to test module from commandline
        - is_flask -- automatically create map for treasure-map
        - zoom -- the map default zoom level 
    """
    def __init__(self, stuffs, address=None, zoom=13, 
                 do_create_map=True, 
                 is_testing=False, is_flask=False):
        self.user_location = stuffs[0].user_location
        self.start_coordinates = self.set_city_center(self.user_location)
        self.zoom = zoom
        self.stuffs = stuffs
        self.radius = 500
        self.address = address 
        if do_create_map:
            self.create_map(is_testing, is_flask)
        
    def create_map(self, is_testing=False, is_flask=False):
        """Create a folium Map object, treasure_map.
        
        Keyword arguments:
            - is_testing -- creates a map in webmap directory
            - is_flask -- creates a flask map
        """
        map_osm = folium.Map([self.start_coordinates[0], self.start_coordinates[1]], zoom_start=self.zoom) 
        for stuff in self.stuffs:
            place = stuff.location  
            thing = stuff.thing  # thing title
            url = stuff.url
            image = stuff.image
            color = self.sort_stuff(stuff.thing)   # Map marker's color
            name = """
                    <link rel='stylesheet' type='text/css' 
                    href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css'>
                    <img src='%s' height='auto' width='160px' />
                    <h3>%s</h3>
                    <h4>%s</h4>
                    <a href='%s' target='_blank'>View Posting in New Tab</a>
                   """ % (image, thing, place, url)
            # TODO: Contigency Plan for 0, 0?
            lat = stuff.coordinates[0] # Latitude
            lon = stuff.coordinates[1] # Longitude
            popup = folium.Popup(IFrame(name, width=200, height=300),
                                 max_width=3000)
            folium.CircleMarker([lat, lon], radius=self.radius, popup=popup,
                                fill_color=color, fill_opacity=0.2).add_to(map_osm)
            self.radius -= 10 # Diminishing order
        self.treasure_map = map_osm
        self.add_address(self.address)
        if is_testing:
            self.save_test_map()
        elif is_flask:
            self.save_flask_map()
        else:
            print("call save_map(path) generate html map")
    
    def save_test_map(self):
        """Create html map in current directory.
        
        Should have python -m http.server running in directory
        """
        path = os.getcwd()
        self.treasure_map.save(os.path.join(path, 'treasure_map.html')) 
        print("BEWARNED, this map is likely incorrect:\nCraigslist denizens care not for computer-precision")
        # webbrowser.open_new_tab("localhost:8000/webmap/findit.html") # Open the map in a tab
        
        
    def save_flask_map(self):
        """Create html map in flask server."""
        folium_figure = self.treasure_map.get_root()
        folium_figure.header._children['bootstrap'] = folium.element.CssLink('static', 'css', 'style.css') #'/static/css/style.css'
        folium_figure.header._children['Woops'] = folium.element.CssLink('static', 'css', 'map.css') # Why woops?
        self.treasure_map.save(os.path.join('treasuremap', 'templates', 'raw_map.html')) 
        
        
    def save_map(self, map_path, css_path=None): # make **argv
        """Create html map in _path.
        
        Keyword arguments:
            - map_path -- the path to create_map in
            - css_path -- the path to override css 
                          (defaults to bootstrap via folium)
        """
        path = os.getcwd()
        if not os.path.exists(os.path.join(path, map_path)):
            os.makedirs(os.path.join(path, map_path))
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

    def add_address(self, address):
        """Add address to folium map"""
        if self.address != None:
            geolocator = Nominatim()
            try:
                add_lat = geolocator.geocode(self.address).latitude
                add_lon = geolocator.geocode(self.address).longitude
            except:
                add_lat = 0
                add_lon = 0
            pop_up = self.address + str(add_lat) + str(add_lon)
            folium.Marker(location=[add_lat, add_lon],popup=self.address,
                          icon=folium.Icon(color='red',icon='home')
                          ).add_to(self.treasure_map)        


    def sort_stuff(self, stuff): # This doesn't work...
        """Rendering the markers in pretty colors."""
        furniture_pattern = "(wood|shelf|table|chair|scrap|desk)"
        electronics_pattern = "(tv|sony|écran|speakers|wire|electronic|saw)" #search NOT match
        find_pattern = "(book|games|cool|guide|box)"
        if re.search(furniture_pattern, stuff, re.I):
            color = "#FF0000" #red ##### THIS should set variable and return at
        elif re.search(electronics_pattern, stuff, re.I): #the end all
            color = "#3186cc" #blue at once
        elif re.search(find_pattern, stuff, re.I):
            color = "#000000" #black
        else:
            color = "white" #white
        # color = "#ffff00"
        return color
