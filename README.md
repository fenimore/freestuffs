# freestuff-bot - or, Never Buy Again!
This is a bot which scrapes free stuff from craigslist (montrea). It posts the data onto a map/html page. It's written in python 3 but ought to be compatible with 2.7 (once you change the print functions accordingly).
I'm trying to get it to work according to the user 
input, that is, whatsoever city we want free stuff from.
And I'm switching this to BeautifulSoup, it makes the 
issue 
for missing nodes (for images/locations) no longer an 
issue.

##To run freestuff-bot, run <code>python -m http.server</code>
<b>The findit.html file is an example of the map output</b>

###Main Dependencies:
<ul>
<li>requests</li>
<li>geopy #crashes after loading over ten 'stuffs'</li>
<li>folium</li>
<li>lxml</li>
</ul>

###So much todo:
<ul>
  <li>Woah, daemon sync in the background: https://github.com/serverdensity/python-daemon</li>
  <li>xpath the img src from craigslist....mmm... (this proves difficult, because when the node is empty, the list is dichevelled. This isn't as much of a problem (but it still is a problem) for the location data.</li>
  <li>put <code>python -m http.server</code> in the init... Is this possible?</li>
  <li>Refine_location method:</li>
    <ul>
      <li>st. Laurent</li>
      <li>st hubert</li>
      <li>West Island</li>
      <li>and many others</li>
    </ul>
  <li>Continue experimenting with Tkinter</li>
</ul>

