# Never Buy Again! Bot, or, freestuff-bot
This is a bot which scrapes free stuff from craigslist (montreal). It posts the data onto a map/html page. It's written in python 3 but ought to be compatible with 2.7 (once you change the print functions accordingly).

I'm trying to get it to work according to the user input, that is, whatsoever city we want free stuff from. And I'm switching this to BeautifulSoup, it makes the issue for missing nodes (for images/locations) no longer an issue. Although it still is apparently...

My goal is to have an accessible library for craigslist freestuff and eventually use it for a remote hosted map, pump.io-bot, and a GUI)

## To run freestuff-bot, run <code>python -m http.server</code>
### Example:
* <code>stuffs = stuff.gather_stuff("montreal")</code>
* <code>mappify.post_map(stuffs)</code> 

<b>The findit.html file is an example of the map output</b>

### Main Dependencies:
<ul>
<li>requests</li>
<li>geopy # Crashes after loading over ten 'stuffs'</li>
<li>folium</li>
<li> ~~lxml~~ </li>
<li>BeautifulSoup4</li>
<li>PyPump (one of these days)</li>
</ul>

### So much todo (planned features & broken features):
<ul>
  <li>Woah, daemon sync in the background: https://github.com/serverdensity/python-daemon</li>
  <li>Package it?</li>
  <li>Pass UserLocation into map starting location</li>
  <li>Create a webapplication!?</li>
  <li>Bot for posting onto pump.io/statusnet</li>
  <li>Post Images onto pret-ty website?</li>
  <li>put <code>python -m http.server</code> in the init... Is this possible?</li>
  <li> ~~Refine_location method:~~ Something ought to be done about the crappy location data</li>
  <li>Continue experimenting with Tkinter/GUI</li>
</ul>

