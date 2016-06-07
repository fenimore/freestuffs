*********************************
Treasure Finder! Never Buy Again!
*********************************

This is a bot which scrapes free stuff from craigslist. It's written in python 3.x but ought to be compatible with 2.x (once you change the print/input functions accordingly).

* Using Stuffify one can gather a list of Free Stuffs. 
* Using Mappify, one can post the freestuffs, and geolocalize them, onto a leaflet/folium map.
* With tweetstuffs and shortenurl, one can post free stuffs onto Craigslist (shortenurl is not needed for twitter anymore).

The "Twitter" Branch is for posting freestuffs onto twitter. 
############################################################
Horay! New York is the pilot project.

Example Usage::

    stuffs = Stuffify("montreal", 10, precise=True).get_freestuffs()
    Mappify(stuffs, is_testing=True)

**The findit.html file is an example of the map output.** It can be nicely embedded in a Jinja2 app. See my `Treasure map <https://github.com/polypmer/treasure-map>`_.

Main Dependencies:
******************

* requests
* geopy
* folium
* BeautifulSoup4
* tweepy (for twitterbot)


TODO (planned features & broken features):
******************************************

* Woah, daemon sync in the background: https://github.com/serverdensity/python-daemon
* Add contact info? [This is harder than it seems...]
* Package it, add commandline script
* Continue to refine location methods/folium tricksss
* put <code>python -m http.server</code> in the init... Is this possible? Or as a map feature?


