# freestuff-bot -- or, Never Buy Again!
<br>
This is a bot which scrapes free stuff from craigslist (montreal).<br>It puts it onto a map/html page. It's written in python3.
<hr>
##Main Dependencies:
requests<br>
lxml
<br>geopy #crashes after loading over ten 'stuffs'<br>
folium
<hr>

<br><br>
##TODO:<br>xpath the img src from craigslist....mmm...<br>
put http.server in init... How possible is this?
<br>Refine_location method needs to be a switch<br>AND it needs to take into account:<br>st. Laurent<br>, st hubert?<br>Etc.
<br>
and IMAGES, the xpath nodes are sometimes missing; this also causes a bug in the location listings<br><hr>

#To run, run 'python -m http.server'
###The findit.html file is an example of the map output
