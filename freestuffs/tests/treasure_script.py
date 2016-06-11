#!/usr/bin/env python
"""Freestuff script"""
from freestuffs import stuff_scraper, stuff_charter

def sample_stuff():
    location = input('Enter city: ')
    stuffs = Stuffify(location, 10, precise=True).get_freestuffs()
    Mappify(stuffs, is_testing=True)
    for stuff in stuffs:
        print('What: %s, Where %s' % (stuff.thing, stuff.location))



