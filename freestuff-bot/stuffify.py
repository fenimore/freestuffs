from lxml import html
import requests, re, folium, webbrowser
from bs4 import BeautifulSoup

# Setup the Location from User Input
def setup_place():
    user_place = input("What major city are you near? (or, 'help') ")
    if user_place == "help":
        print("craigslist serves many major cities, and the peripheral neighborhoods, try something like 'montreal' or 'newyork'\n It's gotta be one word (no spaces) or funny characters, visit the craigslist.org site for your cities 'name'.")
        user_place = input("What major city are you near? ")
    return user_place 

# Setup up the Soup
def setup_page(user_place):
    free_url = 'http://' + user_place +'.craigslist.com/search/zip'
    try:
        free_page = requests.get(free_url)
        soup = BeautifulSoup(free_page.text)
    except:
        print("something when wrong")
    return soup
    
# Setup the Images
def get_images(soup):
    free_images = []
    for row in soup.find_all("a", class_="i"):
        try:
            _img = str(row['data-ids'])
            _img = _img[2:]
            _img = "https://images.craigslist.org/" + _img + "_300x300.jpg"
        except:
            _img = "no image"
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
def get_locations(user_place, soup):
    free_locations = []
    for span in soup.find_all("span", class_="pnr"):
        loc_node = str(span.find('small')) 
        if loc_node == "None": # Some places have no where
            _loc = user_place +", Somewhere"
        else:
            _loc = loc_node.strip('<small ()</small>')
            _loc = _loc + ", " + user_place
        #print(_loc)#
        free_locations.append(_loc)
    return free_locations
    
# Setup the Stuff URLs
def get_urls(soup):
    free_urls = []
    for row in soup.find_all("a", class_="i"):
        _url = row['href'] # Gets the attr from href
        free_urls.append(_url)
    return free_urls
