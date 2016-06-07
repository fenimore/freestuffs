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

"""
    This module houses the ever important Class Definition
    and the gather_stuff method which calls stuffify
    and returns a list of stuffs
    
    Example use, using ipython:
    
    import stuff
    import mappify
    
    stuffs = stuff.gather_stuff("montreal")
    mappify.post_map(stuffs)
"""

import requests, re, folium, webbrowser
from bs4 import BeautifulSoup
import stuffify, mappify # Internal Modules

class Stuff(object):
    """A freestuff Craigslist object.
    
    Attributes:
        - thing -- title of object passed explicitly
        - url -- constructed from url, implicit
        - image -- passed explicitly
        - user_location -- passed explicitly, requires clean up
        - coordinates -- array of longitude and latitude
    """
    #thing = "" # title
    #url = ""
    #location = ""
    #image = ""
    #user_location = ""
    #coordinates = []
		
    def __init__(self, thing, url, location, image, user_location):
        """Construct stuff object.
        
        Fill this object with the information from
        a craigslist page. (There is no price attribute,
        because it is designed for invaluable things).
        The precise coordinates are not initially set,
        because they require significantly more requests.
        See class method get_coordinates().
        
        Keyword arguements:
            - user_location -- use to construct url
        """
        self.thing = thing
        self.url = 'http://' + user_location + '.craigslist.ca' + url
        self.location = location
        self.image = image
        self.user_location = user_location
        self.coordinates = []

    def __str__(self):
        """Print stuff summary."""
        return "what: %s \n where: %s \n link: %s \n image: %s" % (self.thing, self.location, self.url, self.image)

    def refine_city_name(self, city_name):
        """Refine location of two word cities."""
        if city_name == 'newyork': # does this have to capitalized?
            loc = '#FreeStuffNY' # For tweeting
        elif city_name == 'washingtondc':
            loc = 'Washington D.C.'
        elif city_name == 'sanfrancisco':
            loc = 'San Francisco, USA'
        else:
            return loc

    def get_coordinates(self):
    """Get longitude and Latitidue
    
    Scrape individual posting page, if no
    coordinates are found, cascade precision.
    Returns an array, first latitude and then
    longitude.
    """
        geolocator = Nominatim()
        follow_this = self.url
        follow_page = requests.get(follow_this)
        follow_soup = BeautifulSoup(follow_page.text)
        location = follow_soup.find("div", class_="viewposting")
        if location is not None:
            lat = location['data-latitude']
            lon = location['data-longitude']
        else:
            try:
                lat = geolocator.geocode(self.location).latitude
                lon = geolocator.geocode(self.location).longitude
            except:
                try:
                    lat = geolocator.geocode(self.user_location).latitude
                    lon = geolocator.geocode(self.user_location).longitude
                except:
                    lat = 0 #38.9047 # This is DC
                    lon = 0 #-77.0164
        return [lat, lon]
        
def gather_stuff(place, quantity, precise=False):
    """Scrape Craigslist for stuff
    
    
    Keyword arguements:
        - place
        - quantity
        - precise -- A boolean to explicitly use geolocator
                     and crawl individual posting URL
    """
    soup = stuffify.setup_page(place)  
    _quantity = int(quantity)
    locs = stuffify.get_locations(place, soup) # locations, needs user place for fine tuning
    urls = stuffify.get_urls(soup)      
    things = stuffify.get_things(soup) # titles 
    images = stuffify.get_images(soup)  # I can't believe this works..
    """Constructor Combobulator"""
    freestuffs = [Stuff(things[x], urls[x], locs[x], images[x], place) for x in range(0,quantity)] 
    if precise:
        for stuff in freestuffs:
            stuff.coordinates = stuff.get_coordinates()            
    return freestuffs

def test_montreal(): # for quick testing with ipython
    stuffs = gather_stuff("montreal", 10)
    mappify.post_map(stuffs)
def test_newyork(): # for quick testing with ipython
    stuffs = gather_stuff("newyork", 10)
    mappify.post_map(stuffs)


