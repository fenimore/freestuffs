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

import requests, re, folium, webbrowser
from bs4 import BeautifulSoup
from unidecode import unidecode
from stuff import refine_city_name

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

def setup_page(user_place):
    """Request page and return soup.
    
    Bugs:
        - This has to be changed for Europe, where it's all jumbled
    Keyword arguments:
        - user_place -- construct scraping link
    """ 
    _url = 'http://' + user_place +'.craigslist.com/search/zip'
    try:
        free_page = requests.get(_url)
        soup = BeautifulSoup(free_page.text, "html.parser")
    except:
        soup = "something when wrong" # Something informative
    return soup

# ====== Gather Stuff methods ==========================
"""
    Compile paralell lists of stuff attributes in order
    to be fed into a stuff object.
"""
# ==============================================================
    
def get_images(soup):
    """Scrape images.
    
    Keyword arguments:
        - soup - bs4 object of a Craiglist freestuffs page
    """
    free_images = []
    for row in soup.find_all("a", class_="i"):
        try:
            _img = str(row['data-ids']) # Take that Craig!
            _img = _img[2:19] # eats up the first image ID
            _img = _img.replace(',', '')
            _img = "https://images.craigslist.org/" + _img + "_300x300.jpg" # this took me forever
        except:
            _img = "http://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg" # No-image image
        free_images.append(_img)
    return free_images

def get_things(soup):
    """Scrape titles.
    
        Keyword arguments:
        - soup - bs4 object of a Craiglist freestuffs page
    """
    free_things = []
    for node in soup.find_all("a", class_="hdrlnk"):
        _thing = node.get_text() # Get content from within the Node
        free_things.append(_thing)
    return free_things

def get_locations(user_place, soup):
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
    location = refine_city_name(user_place)
    for span in soup.find_all("span", class_="pnr"):
        loc_node = str(span.find('small')) 
        if loc_node == "None": # Some places have no where
            _loc = location + ", NY" # +", Somewhere"
        else:
            _loc = loc_node.strip('<small ()</small>')
            _loc = unidecode(_loc)# Unicode!
            _loc = _loc + ", " + location 
        free_locations.append(_loc)
    return free_locations

def get_urls(soup):
    """Scrape stuff urls.
    
    Keyword arguments:
        - soup - bs4 object of a Craiglist freestuffs page
    """
    free_urls = []
    for row in soup.find_all("a", class_="i"):
        _url = row['href'] # Gets the attr from href
        free_urls.append(_url)
    return free_urls
