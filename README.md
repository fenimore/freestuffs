# freestuff-bot - or, Never Buy Again!
This is a bot which scrapes free stuff from craigslist (montrea). It posts the data onto a map/html page. It's written in python 3 but ought to be compatible with 2.7 (once you change the print functions accordingly).

##To run freestuff-bot, run 'python -m http.server'
<label>The findit.html file is an example of the map output</label>

###Main Dependencies:
<ul>
<li>requests</li>
<li>geopy #crashes after loading over ten 'stuffs'</li>
<li>folium</li>
<li>lxml</li>
</ul>

###So much todo:
<ul>
  <li>xpath the img src from craigslist....mmm... (this proves difficult, because when the node is empty, the list is dichevelled. This isn't as much of a problem (but it still is a problem) for the location data.</li>
  <li>put <code>python -m http.server</code> in the init... Is this possible?</li>
  <li>Refine_location method:</li>
    <ul>
      <li>st. Laurent</li>
      <li>st hubert</li>
      <li>West Island</li>
      <li>and many others</li>
    </ul>
</ul>

