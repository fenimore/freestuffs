from lxml import html
import requests



class Stuff(object):
    thing = ""
    url = ""
    location = ""
    #construct it!
    def __init__(self, thing, url, location):
        self.thing = thing
        self.url = url
        self.location = location
    
    def __str__(self):
        return "what:%s \n where:%s \n link:%s" % (self.thing, self.location, self.url)
        
def gather_stuff(thing, url, location):
    stuff = Stuff(thing, url, location)
    return stuff


#request and scraping
freestuff = requests.get('http://montreal.craigslist.com/search/zip')
freetree = html.fromstring(freestuff.text)
stuffs = freetree.xpath('//a[@class="hdrlnk"]/text()')
urls = freetree.xpath('//a[@class="hdrlnk"]/@href')
locations = freetree.xpath('//span[@class="pnr"]/small/text()')

#the construction of free stuffs
freestuffs = [gather_stuff(stuffs[x], urls[x], locations[x]) for x in range(0,50)]

