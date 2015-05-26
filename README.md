# Treasure Finder! Never Buy Again!
This is a bot which scrapes free stuff from craigslist (montreal). At the moment, it posts the data onto a map/html page but I hope to add other features one-of-these-days. It's written in python 3.x but ought to be compatible with 2.x (once you change the print/input functions accordingly).

I'm trying to get it to work according to the user input, that is, whatsoever city we want free stuff from. And I'm switching this to BeautifulSoup, it makes the issue for missing nodes (for images/locations) no longer an issue. Although it still is apparently...

My goal is to have an accessible library for craigslist freestuff and eventually use it for a remote hosted map, pump.io-bot, and a GUI). I have another repository wherein I try to use these modules to make a web application.

### To run freestuff-bot, run <code>python -m http.server</code>
### Example:
* <code>stuffs = stuff.gather_stuff("montreal")</code>
* <code>mappify.post_map(stuffs)</code> 

<b>The findit.html file is an example of the map output</b>

It's pretty wonky right now.

### Main Dependencies:
<ul>
<li>requests</li>
<li>geopy</li>
<li>folium</li>
<li>BeautifulSoup4</li>
<li>PyPump (one of these days)</li>
</ul>

### So much todo (planned features & broken features):
<ul>
  <li>Woah, daemon sync in the background: https://github.com/serverdensity/python-daemon</li>
  <li>Package it?</li>
  <li>Pass UserLocation into map starting location</li>
  <li>Bot for posting onto pump.io/statusnet</li>
  <li>put <code>python -m http.server</code> in the init... Is this possible?</li>
  <li> Refine_location method: Something ought to be done about the crappy location data</li>
  <li>Continue experimenting with Tkinter/GUI</li>
</ul>

