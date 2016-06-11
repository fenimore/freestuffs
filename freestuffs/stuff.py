#!/usr/bin/env python
"""This houses the Stuff class.
    
Use stuff_scraper in order to gather a list of
stuffs. For testing, the reverse Geolocator is at 
nominatim.openstreetmap.org.
    
Example usage::

    >>> from stuff_scraper import StuffScraper
    >>> stuffs = StuffScraper('montreal', 5).stuffs
    >>> print(stuffs[0].thing)  # Title
    Meubles / furniture
    >>> stuffs[0].find_coordinates() # pass precise=True in constructor
    >>> print(stuffs[0].coordinates) # to automatically fetch coordinates
    ['45.617854', '-73.633931']
"""
import requests, re
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup


class Stuff(object):
    """A freestuff Craigslist object.
    
    Fill this object with the information from
    a craigslist page. (There is no price attribute,
    because it is designed for invaluable things).
    The precise coordinates are not initially set,
    because they require significantly more requests.
    See class method get_coordinates().
    
    Attributes:
        - thing -- title of object passed explicitly
        - url -- constructed from url, implicit
        - image -- passed explicitly
        - user_location -- passed explicitly, requires clean up
        - coordinates -- array of longitude and latitude
    Keyword arguements:
        - thing -- 
        - url -- 
        - location -- 
        - image -- 
        - user_location -- must conform to valid craiglist url
    """    
    def __init__(self, thing, url, location, image, user_location):
        self.thing = thing
        self.url = 'http://' + user_location + '.craigslist.ca' + url
        self.location = location
        self.image = image
        self.user_location = user_location


    def __str__(self):
        """Print stuff summary."""
        return "what: %s \n where: %s \n link: %s \n image: %s" \
                % (self.thing, self.location, self.url, self.image)


    def find_coordinates(self):
        """Get and set longitude and Latitude
        
        Scrape individual posting page, if no
        coordinates are found, cascade precision
        (try location, try user_location, or set
        to zero).  Returns an array, first 
        latitude and then longitude.
        """
        self.coordinates = []
        geolocator = Nominatim()
        follow_this = self.url
        follow_page = requests.get(follow_this)
        follow_soup = BeautifulSoup(follow_page.text, "html.parser")
        location = follow_soup.find("div", class_="viewposting")
        if location is not None: # Get from Page
            lat = location['data-latitude']
            lon = location['data-longitude']
        else:
            try: # Get from posted location
                lat = geolocator.geocode(self.location).latitude
                lon = geolocator.geocode(self.location).longitude
            except:
                try: # Get from user locatoin
                    lat = geolocator.geocode(self.user_location).latitude
                    lon = geolocator.geocode(self.user_location).longitude
                except:
                    lat = 0 #38.9047 # This is DC
                    lon = 0 #-77.0164
        self.coordinates.append(lat)
        self.coordinates.append(lon)
