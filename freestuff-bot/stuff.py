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

#place = stuffify.setup_place() # user place
#soup = stuffify.setup_page(place) # soup, needs the user place for request
"""Construction"""
#locs = stuffify.get_locations(place, soup) # locations, needs user place for fine tuning
#urls = stuffify.get_urls(soup) # urls of stuff
#things = stuffify.get_things(soup) # things of stuff
#images = stuffify.get_images(soup) # get images
"""Constructor Combobulator"""
#freestuffs = [Stuff(things[x], urls[x], locs[x], images[x]) for x in range(0,20)] 
"""Print the Newest Things!"""
#print("The most recent stuff is:\n\n", freestuffs[0])

def gather_stuff(place):
    soup = stuffify.setup_page(place)   # soup, needs the user place for request
    """Construction"""
    locs = stuffify.get_locations(place, soup) # locations, needs user place for fine tuning
    urls = stuffify.get_urls(soup)      # urls of stuff
    things = stuffify.get_things(soup)  # things of stuff
    images = stuffify.get_images(soup)  # I can't believe this works..

    """Constructor Combobulator"""
    freestuffs = [Stuff(things[x], urls[x], locs[x], images[x]) for x in range(0,20)] 
    return freestuffs




