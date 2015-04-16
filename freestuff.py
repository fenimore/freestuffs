from lxml import html
import requests, re, folium, webbrowser #cool kids import all at once
from geopy.geocoders import Nominatim
from stuff import Stuff
import stuffify #these are modules

#request
freestuff = requests.get('http://montreal.craigslist.com/search/zip')

#scraping, using xpath maybe I should I gone with bsoup
freetree = html.fromstring(freestuff.text)
stuffs = freetree.xpath('//a[@class="hdrlnk"]/text()')
urls = freetree.xpath('//a[@class="hdrlnk"]/@href')
locations = freetree.xpath('//span[@class="pnr"]/small/text()')
images = freetree.xpath('//a[@class="hdrlnk"]/@href')   #'.//*[@id="searchform"]/div[2]/div[3]/p[4]/a/div[1]/div/div[1]/img')
# this is a list combobulator. Python really is beautiful
geocode_freestuffs = [stuffify.gather_stuff(stuffs[x], urls[x], locations[x], images[x]) for x in range(0,10)] #geocoding crashes after ten markers
freestuffs = [stuffify.gather_stuff(stuffs[x], urls[x], locations[x], images[x]) for x in range(0,20)] #the terminal will print a bigger list

#runnnnning
stuffify.post_listings(freestuffs) #list freestuffs in terminal
#Make sure http.server is running
stuffify.post_map(geocode_freestuffs) #throw freestuffs onto map
#stuffserver.launch_server() #This doesn't work
webbrowser.open_new_tab("localhost:8000/findit.html")
print("never buy again!")

#test geolocator, cool feature
#geolocator = Nominatim()
#findit = geolocator.geocode(freestuffs[0].location)
#if findit is not None:    
#    print(findit)
