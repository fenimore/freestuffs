============
Introduction
============


Free Stuffs!
------------

This is a Python 3.x package which scrapes free stuff from Craigslist.
freestuffs is under the MIT license. Check out the `source code <https://github.com/polypmer/freestuff-bot>`_
and the `docs <http://freestuffs.readthedocs.io/en/latest>`_.

* Using StuffScraper one can gather a list of free stuffs.
* Using StuffCharter, one can create an HTML map of the free stuffs.

This package can be used to create a web application, such as the
Treasure-map_ (source_), or for use on Twitter_.

.. _Github: https://github.com/polypmer/freestuffs
.. _Twitter: https://twitter.com/Freeebot
.. _source: https://github.com/polypmer/treasure-map
.. _Treasure-map: http://treasure.plyp.org

Installation
------------

``freestuffs`` can be installed with pip:

.. code-block:: bash

    pip install freestuffs

The package has the following dependencies which are automatically
installed by pip:

* ``beautifulsoup4``
* ``bs4``
* ``folium``
* ``geopy``
* ``requests``
* ``Unidecode``

Additionally, these may be manually installed using pip with
``pip install -r requirements.txt``.

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


Legend
+++++++++++++++++

- The smaller the posting, the older it is.
- The darker the border, the higher the amount of overlap.

Triage
++++++

The triage checks for regex search in this order:

#. Red are furniture - wood, shelf, shelves, table, chair, scrap, desk.
#. Blue are electronics: tv, sony, ecran, speakers, wire, electronic, saw, headphones, arduino.
#. Black are the "desired" stuffs: book, games, cool, guide, box.
#. White is default (no regex search matches).

Support
-------

The easiest way to get support is to open an issue on `Github <http://github.com/polypmer/freestuff-bot/issues>`_.
