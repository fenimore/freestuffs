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
import requests, re
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import stuffify

"""
    This module houses the ever important Stuff class.
    
    Use stuffify in order to gather a list of stuffs.
    
    Example usage:
    from stuffify import Stuffify
    freestuffs = Stuffify('montreal', 5, precise=True).get_freestuffs()
    freestuffs[0].thing
    freestuffs[0].coordinates
"""

class Stuff(object):
    """A freestuff Craigslist object.
    
    Attributes:
        - thing -- title of object passed explicitly
        - url -- constructed from url, implicit
        - image -- passed explicitly
        - user_location -- passed explicitly, requires clean up
        - coordinates -- array of longitude and latitude
    """    
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


    def __str__(self):
        """Print stuff summary."""
        return "what: %s \n where: %s \n link: %s \n image: %s" % (self.thing, self.location, self.url, self.image)


    def find_coordinates(self):
        """Get and set longitude and Latitude
        
        Scrape individual posting page, if no
        coordinates are found, cascade precision.
        Returns an array, first latitude and then
        longitude.
        """
        self.coordinates = []
        geolocator = Nominatim()
        follow_this = self.url
        follow_page = requests.get(follow_this)
        follow_soup = BeautifulSoup(follow_page.text, "html.parser")
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
        self.coordinates.append(lat)
        self.coordinates.append(lon)
