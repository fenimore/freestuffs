#!/usr/bin/env python
"""Chart where free things are.

The StuffCharter class is a wrapper around the folium 
openstreetmap python object, which in turn generates a 
leaflet map.

Example usage:

    >>> from stuff_scraper import StuffScraper
    >>> from stuff_charter import StuffCharter
    >>> stuffs = StuffScraper('montreal', 5, precise=True).stuffs
    >>> treasure_map = StuffCharter(stuffs)
    call save_map(path) generate html map
    >>> treasure_map.save_test_map() # saves map in current dir
    BEWARNED, this map is likely inaccurate:
    Craigslist denizens care not for computer-precision
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
        - stuffs -- a list of stuff objects
        - address -- for an optional map marker of the user address.
        - do_create_map -- set to False to override modify attributes
                           before create_map.
        - is_testing -- use to test module from commandline
        - is_flask -- automatically create map for treasure-map
        - zoom -- the map default zoom level 
    """
    
    def __init__(self, stuffs, address=None, zoom=13, 
                 do_create_map=True, 
                 is_testing=False, is_flask=False):
        self.user_location = stuffs[0].user_location
        self.start_coordinates = self.find_city_center(self.user_location)
        self.zoom = zoom
        self.stuffs = stuffs
        self.radius = 500
        self.address = address 
        if do_create_map:
            self.create_map(is_testing, is_flask)
        
    def create_map(self, is_testing=False, is_flask=False):
        """Create a folium Map object, treasure_map.
        
        treasure_map can be used to save an html leaflet map.
        This method is called automatically on __init__ unless
        do_create_map is set to False.
        
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
            print("call save_map(path) to generate html map")
    
    def save_test_map(self):
        """Create html map in current directory.
        
        Should have python -m http.server running in directory
        """
        path = os.getcwd()
        self.treasure_map.save(os.path.join(path, 'treasure_map.html')) 
        print("BEWARNED, this map is likely inaccurate:\nCraigslist denizens care not for computer-precision")
        # webbrowser.open_new_tab("localhost:8000/webmap/findit.html") # Open the map in a tab
        
        
    def save_flask_map(self):
        """Create html map in flask server."""
        folium_figure = self.treasure_map.get_root()
        folium_figure.header._children['bootstrap'] = folium.element.CssLink('static', 'css', 'style.css') #'/static/css/style.css'
        folium_figure.header._children['Woops'] = folium.element.CssLink('static', 'css', 'map.css') # Why woops?
        self.treasure_map.save(os.path.join('treasuremap', 'templates', 'raw_map.html')) 
        
        
    def save_map(self, map_path, css_path=None): # make **argv
        """Create html map in map_path.
        
        Keyword arguments:
            - map_path -- the path to create_map in
            - css_path -- the path to override css 
                          (defaults to bootstrap via folium)
        """
        path = os.getcwd()
        if not os.path.exists(os.path.join(path, map_path)):
            os.makedirs(os.path.join(path, map_path))
        if css_path is not None:
            folium_figure = self.treasure_map.get_root() # Leaflet Style conflicts with custom Bootstrap
            folium_figure.header._children['Woops'] = folium.element.CssLink(css_path)
        self.treasure_map.save(map_path)

        
    def find_city_center(self, location):
        """Return city center longitude latitude."""
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

    def add_address(self, _address):
        """Add address to folium map"""
        self.address = _address
        if _address != None:
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


    def sort_stuff(self, stuff): 
        """Return a color according to regex search.
        
        1. Furniture pattern, red 
        2. Electronics pattern, blue
        3. Miscellaneous pattern, black 
        4. no match, white
        
        sort_stuff will return  with the first pattern found in 
        that order.
        
        TODO:
            - Set and patterns as modifiable attributes.
        """
        PATTERN_1 = "(wood|shelf|shelves|table|chair|scrap|desk|oak|pine|armoire|dresser)"
        PATTERN_2 = "(tv|screen|écran|speakers|wire|electronic|saw|headphones|arduino|print|television)" #search NOT match
        PATTERN_3 = "(book|games|cool|guide|box)"

        COLOR_1 = "#FF0000" #red 
        COLOR_2 = "#3186cc" #blue
        COLOR_3 = "#000000" #black
        
        COLOR_DEFAULT = "white"
        if re.search(PATTERN_1, stuff, re.I):
            color = COLOR_1 #red #  TODO: set as Variable
        elif re.search(PATTERN_2, stuff, re.I): #the end all
            color = COLOR_2 #blue at once
        elif re.search(PATTERN_3, stuff, re.I):
            color = COLOR_3 #black
        else:
            color = COLOR_DEFAULT #white
        # color = "#ffff00"
        return color
