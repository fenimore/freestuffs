============
Read Me
============

Free Stuffs!
------------

This is a python 3.x package which scrapes free stuff from Craigslist. 
freestuffs is under the MIT license. Check out the `source code <https://github.com/polypmer/freestuff-bot>`
and the `docs <http://freestuffs.readthedocs.io/en/latest/>`.

* Using StuffScraper one can gather a list of free stuffs. 
* Using StuffCharter, one can create an HTML map of the free stuffs.

This library can be used to create a simple web application, such as the
`Treasure map <https://github.com/polypmer/treasure-map>`_, or a simple
`Twitter bot <https://github.com/polypmer/freestuff-bot>`_

Installation
------------

Install using pip, requires python 3 and these dependences:

* requests
* geopy
* folium
* BeautifulSoup4
* unidecode

Install::

    pip install freestuffs

Or, with virtualenvwrapper installed:

.. code-block:: bash

    mkvirtualenv freestuffs
    pip install freestuffs

Getting Started
---------------

Stuffs
******

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
************

The StuffScraper class will scrape Craiglist for
free stuff. 

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

Chart Stuffs
************

The StuffCharter class will produce a folium Map object populated
with free stuff from the StuffScraper.

::

    >>> from freestuffs.stuff_scraper import StuffScraper
    >>> from freestuffs.stuff_charter import StuffCharter
    >>> stuffs = StuffScraper('montreal', 5, precise=True).stuffs
    >>> stuffs_chart = StuffCharter(stuffs)
    call save_map(path) generate html map
    >>> type(map.treasure_map)
    <class 'folium.folium.Map'>

The StuffCharter object is a wrapper around the folium.Map.
Call :code:`save_map(HTML_PATH, CSS_PATH)`

::

    >>> stuffs_chart.save_map('webmap', 'static/style.css')
    
This function creates a directory if it is not found in the path. Call instead
:code:`save_test_map()` to generate an HTML map in the current directory.


Support
-------

The easiest way to get support is to open an issue on Github_.

.. _Github: http://github.com/polypmer/freestuff-bot/issues
