from stuff import Stuff
from geopy.geocoders import Nominatim
import folium, re, random # cool kids import all at once

# stuff constructor
def gather_stuff(thing, url, location, image):
    place = refine_location(location) #pass location through refine method
    stuff = Stuff(thing, url, place, image)
    return stuff

# getter for longitude and latitude
def get_coordinates(location):
    geolocator = Nominatim()
    findit = geolocator.geocode(location)
    lat = findit.latitude
    lon = findit.longitude
    coord = [lat, lon]
    return coord

#Refine Craigslist's pitiful location specifications
def refine_location(place): #there is no switch in python
    location = str(place).strip(' ()') #why do i need that space? Do I need that space? Yes.
                                        #this thing barely works
                                        # TODO: West Island
    montreal_pattern = "montreal|mtl"
    henri_pattern = "st-henri"
    if re.match(montreal_pattern, location, re.I): #why doesn't this work?
        refinition = " Montréal, Somewhere"
        return refinition
    if re.match(henri_pattern, location, re.I): #OHHHH I figuredc it out
        refinition = " Place Saint-Henri, Montréal"
        return refinition
    if re.match("mcgill", location, re.I):
        refinition = " McGill Univesrity, Montréal"
        return refinition
    if re.match("saint laurent", location, re.I):
        refinition = "blvd St Laurent, Montréal"
        return refinition
    if re.match("plateau", location, re.I):
        refinition = "Plateau Mont Royal, Montréal"
        return refinition
    if re.match("ndg", location, re.I):
        refinition = " Notre-Dame-de-Grâce, Montréal" #Are if statements a silly way to do this?
        return refinition
    if re.match("cdn", location, re.I):
        refinition = " Côte-des-Neiges, Montréal"
        return refinition 
    else:
        refinition = location + ", Montréal" #this don't work!
        return refinition #slick word, huh?

#Returns the color for map rendering
def sort_stuff(stuff):

    furniture_pattern = "(wood|shelf|table|chair|scrap)"
    electronics_pattern = "(tv|sony|écran|speakers)" #search NOT match
    find_pattern = "(book|games|cool)"               #sooo these are what I'm looking for?
    if re.search(furniture_pattern, stuff, re.I):
        return "#FF0000" #red
    if re.search(electronics_pattern, stuff, re.I):
        return "#3186cc" #blue
    if re.search(find_pattern, stuff, re.I):
        return "#000000" #black
    else:
        return "#FFFFFF" #white

#Post listings in terminal
def post_listings(freestuffs): #for now, print but later i'll list on html page
    for freestuff in freestuffs:
        output = str(freestuff) #locations aren't refined
        print(output)

#Post listings in map; looks more complicated than it is
#Everytime this script runs, findit.html gets a new map
def post_map(freestuffs):
    #hexa = hex(random.randint(0, 16777215))[2:].upper() #maybe these are a waste of breathe
    #random_color = "#{0}".format(hexa)
    map_osm = folium.Map([45.5088, -73.5878], zoom_start=13) #Montreal's Mont Royal
    radi = 700 #this corrects overlapping stuffs
    for freestuff in freestuffs:                    #loop through stuffs
        place = freestuff.location                  #location
        thing = freestuff.thing                     #thing
        url = freestuff.url                         #link
        image = freestuff.image                     #"<img src="freestuff.image "/>"
        color = sort_stuff(thing)                   #map marker color
        # name is the map posting --- add img src tag
        name = image + "<br><h3>" + thing + "</h3><h4>" + place + "</h4><a href=" + url + " target='_blank'>view ad</a>"
        try:
            coordinates = get_coordinates(freestuff.location)#get coords returns a list (lat = 0 lon = 1)
            lat = coordinates[0]
            lon = coordinates[1]
        except: #put it on the mountain somewhere if it's "somewhere"
            lat = 45.5088
            lon = -73.5878
        map_osm.circle_marker(location=[lat, lon], radius=radi,
          popup=name, line_color="#000000",
          fill_color=color, fill_opacity=0.2)
        radi -= 60 #decrease the radius to show older postings
    map_osm.create_map(path='findit.html') #open this 
