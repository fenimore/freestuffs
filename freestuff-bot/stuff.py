from lxml import html
import requests, re, folium, webbrowser
from bs4 import BeautifulSoup
import stuffify

class Stuff(object):
    thing = ""
    url = ""
    location = ""
    image = ""
		
    #constructor the de-structor!!  
    def __init__(self, thing, url, location, image):
        self.thing = thing
        self.url = 'http://montreal.craigslist.ca' + url
        self.location = location
        self.image = image #this isn't implemented yet

    #the stringifing printer.... Python is so pretty
    def __str__(self):
        return "what: %s \n where: %s \n link: %s \n image: %s" % (self.thing, self.location, self.url, self.image)
        
def get_freestuffs():
    """Set Up"""
    place = setup_place() # user place
    soup = setup_page(place) # soup, needs the user place for request
    """Construction"""
    locs = get_locations(place, soup) # locations, needs user place for fine tuning
    urls = get_urls(soup) # urls of stuff
    things = get_things(soup) # things of stuff
    images = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20] # get_images(soup) # WILL THIS EVERY WORK?

    """Constructor Combobulator"""
    freestuffs = [Stuff(things[x], urls[x], locs[x], images[x]) for x in range(0,20)] 
    return freestuffs








