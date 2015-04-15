#This Object is anything so-called Free
class Stuff(object):
    thing = ""
    url = ""
    location = ""
    image = ""
		
    #constructor the de-structor!!  
    def __init__(self, thing, url, location):
        self.thing = thing
        self.url = 'http://montreal.craigslist.ca' + url
        place = str(location).strip(' ()') #what if I put this crap in refinition method?
        self.location = place + ", Montréal"
        #put 'montreal' so geolocator works
        #add image constructor? self.image = image... can't find xpath for src

    #the stringifing printer.... Python is so pretty
    def __str__(self):
        return "what:%s \n where:%s \n link:%s" % (self.thing, self.location, self.url)
        
