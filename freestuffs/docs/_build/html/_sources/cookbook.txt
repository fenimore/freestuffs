============
Cookbook
============

Stuffs
------

The stuff class corresponds to a `Craiglist <https://www.craigslist.org>`_
free stuff posting. It's basic characteristics include title and location.
Notably, there is no price attribute. If the posting has no image, the 
`Wikipedia <https://www.wikipedia.org>`_ no-image image is used in it's place.

::
    
    >>> from freestuffs.stuff_scraper import StuffScraper
    >>> stuffs = StuffScraper('montreal', 5).stuffs
    >>> print(stuffs[0])
    what: free shelves 
     where: Workman St, montreal 
     link: http://montreal.craigslist.ca/zip/5629811181.html 
     image: https://images.craigslist.org/00r0r_4p06sM5Hn4O_300x300.jpg


Scape Stuffs
------------

The StuffScraper class will scrape Craiglist for
free stuff. The two required args are the city name and 
the quantity of stuff to scrape. The city name **must**
conform to the Craiglist url name. Cities like New York, 
are then 'newyork'.

::

    >>> from freestuffs.stuff_scraper import StuffScraper
    >>> stuffs = StuffScraper('montreal', 5).stuffs # precise=False
    >>> print(stuffs[0].thing)  # Title
    Meubles / furniture

In order for the scraper to automatically
scrape for latitude and longitude coordinates, pass in the
parameter precise=True into the constructor.

::

    >>> from freestuffs.stuff_scraper import StuffScraper
    >>> stuffs = StuffScraper('montreal', 5, precise=True).stuffs
    >>> print(stuffs[0].coordinates)
    ['45.617854', '-73.633931']
    
Otherwise, one can call :code:`stuffs[0].find_coordinates()` in order to set (and scrape) the stuff coordinates one by one.

Pass in :code:`use_cl=true` in order to ask for user input and override
the location entered in the __init__.::

    >>> from freestuffs.stuff_scraper import StuffScraper
    >>> stuffs = StuffScraper('ill decide later', 1, use_cl=True).stuffs
    What major city are you near? (or, 'help') newyork
    >>> print(stuffs[0].location)
    East Harle, New York 


Chart Stuffs
------------

The StuffCharter class will produce a folium Map object populated
with free stuff from the StuffScraper. The StuffCharter object is
a wrapper around the folium.Map.

::

    >>> from freestuffs.stuff_scraper import StuffScraper
    >>> from freestuffs.stuff_charter import StuffCharter
    >>> stuffs = StuffScraper('montreal', 5, precise=True).stuffs
    >>> stuffs_chart = StuffCharter(stuffs)
    call save_map(path) generate html map
    >>> type(map.treasure_map)
    <class 'folium.folium.Map'>

Call :code:`save_map(HTML_PATH, CSS_PATH)` in order to save an HTML
map from the folium.Map object. (equivelant to calling :code:`folium.Map.save(path)`)

::

    >>> stuffs_chart.save_map('webmap', 'static/style.css')
    
This function creates a directory if it is not found in the path. Call instead
:code:`save_test_map()` to generate an HTML map in the current directory.

Optionally pass in an :code:`address` or :code:`zoom` level into its construction. 
Otherwise if :code:`do_create_map` is :code:`False`, these attributes can be
modified manually.

::

    >>> from freestuffs.stuff_scraper import StuffScraper
    >>> from freestuffs.stuff_charter import StuffCharter
    >>> stuffs = StuffScraper('montreal', 5, precise=True).stuffs
    >>> stuffs_chart = StuffCharter(stuffs, zoom=15, do_create_map=False)
    >>> stuffs_chart.zoom = 10 # default 13
    >>> stuffs_chart.create_map()
    call save_map(path) generate html map
    
The stuff markers are colored circles in diminishing order; the small the circle, the older the posting (this prevents inaccessible overlaps).

And you can add an address (not zoom) after the map has been created::

    >>> stuffs_chart.add_address('5989 Rue du Parc, Montreal, Quebec')
    >>> print(stuffs_chart.address) 
    5989 Rue du Parc, Montreal, Quebec
    
And why stop at one address maker(the :code:`address` attribute will
always be the last address added)::

    >>> stuffs_chart.add_address('5989 Rue du Parc, Montreal, Quebec')
    >>> stuffs_chart.add_address('604 Rue Saint Joseph, Montreal, Quebec')
    >>> print(stuffs_chart.address) 
    604 Rue Saint Joseph, Montreal, Quebec

Override the css by adding links to the folium object header::

    >>> import folium
    >>> osm_map = stuffs_chart.treasure_map
    >>> folium_figure = osm_map.get_root()
    >>> folium_figure.header._children['bootstrap'] = folium.element.CssLink('/static/css/style.css')   
    
To use the treasure_map as a template in a python web app, the leaflet bootstrap css 
might conflict with the user defined styles. Before saving the map, add a CssLink.

The fastest way to get a map up and running, is to pass :code:`is_testing=True`
into the constructor::

    >>> from freestuffs.stuff_scraper import StuffScraper
    >>> from freestuffs.stuff_charter import StuffCharter
    >>> stuffs = StuffScraper('montreal', 5, precise=True).stuffs
    >>> stuffs_chart = StuffCharter(stuffs, is_testing=True)
    BEWARNED, this map is likely inaccurate:
    Craigslist denizens care not for computer-precision
