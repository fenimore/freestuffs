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

# Setup the Location from User Input
# Basically just for kicks
def setup_place():
    user_place = input("What major city are you near? (or, 'help') ")
    if user_place == "help":
        print("craigslist serves many major cities, and the peripheral neighborhoods, try something like 'montreal' or 'newyork'\n It's gotta be one word (no spaces) or funny characters, visit the craigslist.org site for your cities 'name'.\nAlso, the mappify module currently only works with montreal")
        user_place = input("What major city are you near? ")
    return user_place 

""" Setup up the Soup """ 
# This has to Change for Europe, it's all jumbled there.
def setup_page(user_place):
    free_url = 'http://' + user_place +'.craigslist.com/search/zip'
    try:
        free_page = requests.get(free_url)
        soup = BeautifulSoup(free_page.text)
    except:
        soup = "something when wrong" # Something informative
    return soup
    
""" Setup the Images """
def get_images(soup):
    free_images = []
    for row in soup.find_all("a", class_="i"):
        try:
            _img = str(row['data-ids']) # Take that Craig!
            _img = _img[2:19] # eats up the first image ID
            _img = _img.replace(',', '')
            _img = "https://images.craigslist.org/" + _img + "_300x300.jpg" # Fuck yeah this took me forever
        except:
            _img = "http://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg" # No-image image
        free_images.append(_img)
    return free_images

# Setup the Thing Titles
def get_things(soup):
    free_things = []
    for node in soup.find_all("a", class_="hdrlnk"):
        _thing = node.get_text() # Get content from within the Node
        free_things.append(_thing)
    return free_things

# Setup the Stuff Locations
# This needs to be redone # FOR TWITTER IT HAS BEEN MODIFIED
"""Refine the Location for two word cities """
def refine_city_name(location):
    if location == 'newyork': # does this have to capitalized
        loc = '#FreeStuffNewYork'
    elif location == 'washingtondc':
        loc = 'Washington D.C.'
    elif location == 'sanfrancisco':
        loc = 'San Francisco, USA'
    else:
        loc = location
    return loc

# Setup the Stuff Locations
# This needs to be redone
def get_locations(user_place, soup):
    free_locations = []
    location = refine_city_name(user_place)
    for span in soup.find_all("span", class_="pnr"):
        loc_node = str(span.find('small')) 
        if loc_node == "None": # Some places have no where
            _loc = location +", Somewhere"
        else:
            _loc = loc_node.strip('<small ()</small>')
            _loc = unidecode(_loc)# Unicode!
            _loc = _loc + ", " + location
        free_locations.append(_loc)
    return free_locations

# Setup the Stuff URLs
def get_urls(soup):
    free_urls = []
    for row in soup.find_all("a", class_="i"):
        _url = row['href'] # Gets the attr from href
        free_urls.append(_url)
    return free_urls
