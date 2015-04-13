class Stuff(object):
    thing = ""
    url = ""
    location = ""
    coord = [] #mmmh, no luck
    #construct it!
    def set_coord(lat, lon): #yearh right htis doesn't work!
        self.coord = [lat, lon]
        
    def __init__(self, thing, url, location):
        self.thing = thing
        self.url = 'http://montreal.craigslist.ca' + url
        place = str(location).strip(' ()')
        self.location = "montreal, " + place
    
    def __str__(self):
        return "what:%s \n where:%s \n link:%s" % (self.thing, self.location, self.url)
        
