from lxml import html
import requests, re, folium, webbrowser #cool kids import all at once
from geopy.geocoders import Nominatim
from stuff import Stuff
import stuffify #these are modules

                                                                #request Free Stuff
freestuff = requests.get('http://montreal.craigslist.com/search/zip')

#scraping, using xpath maybe I should I gone with bsoup
freetree = html.fromstring(freestuff.text)                      #get HTML tree
stuffs = freetree.xpath('//a[@class="hdrlnk"]/text()')          #get Stuff Titles
urls = freetree.xpath('//a[@class="hdrlnk"]/@href')             #get URLS
locations = freetree.xpath('//span[@class="pnr"]/small/text()') #get Location
##Images xpath gets empty node
##############################
images = freetree.xpath('//a[@class="hdrlnk"]/@href')  #'.//*[@id="searchform"]/div[2]/div[3]/p[4]/a/div[1]/div/div[1]/img')


# this is a list combobulator. Python really is beautiful:
geocode_freestuffs = [stuffify.gather_stuff(stuffs[x], urls[x], locations[x], images[x]) for x in range(0,10)] 
                                                                #geocoding crashes after ten markers
freestuffs = [stuffify.gather_stuff(stuffs[x], urls[x], locations[x], images[x]) for x in range(0,20)] 
                                                                #the terminal will print a bigger list

##RUNNING IT
############
stuffify.post_listings(freestuffs) #list freestuffs in terminal
                                   #Make sure http.server is running
stuffify.post_map(geocode_freestuffs) #throw freestuffs onto map
         #stuffserver.launch_server() #This doesn't work
webbrowser.open_new_tab("localhost:8000/findit.html")
print("\n", "Never Buy Again!", "\n\n", "see Legend file for details")          
                                      #Print Exit Message

##END PROGRAM
#############


####THIS IS A COOL FEATURE
#geolocator = Nominatim()
#findit = geolocator.geocode(freestuffs[0].location)
#if findit is not None:    
#    print(findit)
