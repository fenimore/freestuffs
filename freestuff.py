from lxml import html
import requests, re, folium
from geopy.geocoders import Nominatim
from stuff import Stuff
import stuffify #this is a module
import webbrowser
import stuffserver

#request
freestuff = requests.get('http://montreal.craigslist.com/search/zip')
#scraping, using xpath maybe I should I gone with bsoup
freetree = html.fromstring(freestuff.text)
stuffs = freetree.xpath('//a[@class="hdrlnk"]/text()')
urls = freetree.xpath('//a[@class="hdrlnk"]/@href')
locations = freetree.xpath('//span[@class="pnr"]/small/text()')

# this is a list combobulator. Python really is beautiful
geocode_freestuffs = [stuffify.gather_stuff(stuffs[x], urls[x], locations[x]) for x in range(0,10)] #geocoding crashes after ten markers
freestuffs = [stuffify.gather_stuff(stuffs[x], urls[x], locations[x]) for x in range(0,20)]

#test geolocator, cool feature
#geolocator = Nominatim()
#findit = geolocator.geocode(freestuffs[0].location)
#if findit is not None:    
#    print(findit)

stuffify.post_listings(freestuffs)
#Make sure http.server is running
stuffify.post_map(geocode_freestuffs)
#stuffserver.launch_server() #This doesn't work
webbrowser.open_new_tab("localhost:8000/findit.html")

