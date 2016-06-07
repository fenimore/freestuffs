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
#TODO: Do I have to include empty list declaration? Or maybe I should
###

import requests, re
from bs4 import BeautifulSoup
from unidecode import unidecode
from stuff import Stuff

class Stuffify:
    """A freestuff Craigslist scraper.
    
    Compile parrellel lists of stuff attributes
    in order to store a freestuffs list, with an
    option for including stuff coordinates.
    
    Attributes:
        - freestuffs -- a list of stuff objects
        - soup
        - quantity -- constructed from url, implicit
        - locations -- passed explicitly
        - urls -- passed explicitly, requires clean up
        - things -- 
        - images -- 
    """
    def __init__(self, place, _quantity, precise=False, use_cl=False):
        """Scrape Craigslist for a list of stuff.
        
        Keyword arguments:
            - place
            - _quantity
            - precise -- A boolean to explicitly use geolocator
                         and crawl individual posting URL
        """
        if use_cl:
            place = self.setup_place()
        _url = 'http://' + place +'.craigslist.com/search/zip'
        try:
            free_stuff_page = requests.get(_url)
            _soup = BeautifulSoup(free_stuff_page.text, "html.parser")
        except:
            _soup = "something when wrong" # Something informative
        self.soup = _soup  
        self.quantity = int(_quantity)
        self.locs = self.get_locations(place, self.soup) # locations, needs user place for fine tuning
        self.urls = self.get_urls(self.soup)      
        self.things = self.get_things(self.soup) # titles 
        self.images = self.get_images(self.soup)  # I can't believe this works..
        self.freestuffs = [Stuff(self.things[x], self.urls[x], self.locs[x], 
                           self.images[x], place) 
                           for x in range(0, self.quantity)] 
        if precise:
            for stuff in self.freestuffs:
                stuff.find_coordinates()
    
    def get_freestuffs(self):
        """Get a list of freestuffs"""
        return self.freestuffs
        
    def setup_place():
        """Take cl input of user location."""
        user_place = input("What major city are you near? (or, 'help') ")
        if user_place == "help":
            print("craigslist serves many major cities, \
            and the peripheral neighborhoods, try something\
             like 'montreal' or 'newyork'\n It's gotta be \
             one word (no spaces) or funny characters, visit\
              the craigslist.org site for your cities 'name'.\
              \nAlso, the mappify module currently only works with montreal")
            user_place = input("What major city are you near? ")
        return user_place   
        
        
    def get_things(self, _soup):
        """Scrape titles.
        
            Keyword arguments:
            - soup - bs4 object of a Craiglist freestuffs page
        """
        free_things = []
        for node in _soup.find_all("a", class_="hdrlnk"):
            _thing = node.get_text() # Get content from within the Node
            free_things.append(_thing)
        return free_things

    def get_locations(self, user_place, _soup):
        """Scape locations.
        
           Returns a list of locations, more or less
           precise. Concatnate user_place to string
           in order to aid geolocator in case of
           duplicate location names in world. Yikes.
        
           Keyword arguments:
               - user_place -- 
               - soup - bs4 object of a Craiglist freestuffs page
        """
        free_locations = []
        # location = Stuff.refine_city_name(user_place=user_place)
        location = user_place
        for span in _soup.find_all("span", class_="pnr"):
            loc_node = str(span.find('small')) 
            if loc_node == "None": # Some places have no where
                _loc = location + ", NY" # +", Somewhere"
            else:
                _loc = loc_node.strip('<small ()</small>')
                _loc = unidecode(_loc)# Unicode!
                _loc = _loc + ", " + location 
            free_locations.append(_loc)
        return free_locations
        
        
    def get_urls(self, _soup):
        """Scrape stuff urls.
        
        Keyword arguments:
            - soup - bs4 object of a Craiglist freestuffs page
        """
        free_urls = []
        for row in _soup.find_all("a", class_="i"):
            _url = row['href'] # Gets the attr from href
            free_urls.append(_url)
        return free_urls


    def get_images(self, _soup):
        """Scrape images.
        
        Uses wikpedia No-image image if no image is found.
        
        Keyword arguments:
            - soup - bs4 object of a Craiglist freestuffs page
        """
        free_images = []
        for row in _soup.find_all("a", class_="i"):
            try:
                _img = str(row['data-ids']) # Take that Craig!
                _img = _img[2:19] # eats up the first image ID
                _img = _img.replace(',', '')
                _img = "https://images.craigslist.org/" + _img + "_300x300.jpg" # this took me forever
            except:
                _img = "http://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg" # No-image image
            free_images.append(_img)
        return free_images
