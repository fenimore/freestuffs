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

# TODO: add __init__ ?
#       as in, have this module be main
# TODO: Take argv params?

class Stuff(object):
    thing = ""
    url = ""
    location = ""
    image = ""
    user_location = ""
		
    #constructor the de-structor!!  
    def __init__(self, thing, url, location, image, user_location):
        self.thing = thing
        self.url = 'http://' + user_location + '.craigslist.ca' + url
        self.location = location
        self.image = image
        self.user_location = user_location

    #the stringifing printer.... Python is so pretty
    def __str__(self):
        return " what: %s \n where: %s \n link: %s \n image: %s" % (self.thing, self.location, self.url, self.image)

def gather_stuff(place):
    soup = stuffify.setup_page(place)   # soup, needs the user place for request
    """Construction"""
    locs = stuffify.get_locations(place, soup) # locations, needs user place for fine tuning
    urls = stuffify.get_urls(soup)      # urls of stuff
    things = stuffify.get_things(soup)  # things of stuff
    images = stuffify.get_images(soup)  # I can't believe this works..

    """Constructor Combobulator"""
    freestuffs = [Stuff(things[x], urls[x], locs[x], images[x], place) for x in range(0,20)] 
    return freestuffs

def test_montreal(): # for quick testing with ipython
    stuffs = gather_stuff("montreal")
    mappify.post_map(stuffs)
def test_newyork(): # for quick testing with ipython
    stuffs = gather_stuff("newyork")
    mappify.post_map(stuffs)


