#!/usr/bin/env python
"""Freestuff script"""
from stuffify import Stuffify
from mappify import Mappify

def sample_stuff():
    location = input('Enter city: ')
    stuffs = Stuffify('montreal', 10, precise=True).get_freestuffs()
    Mappify(stuffs, is_testing=True)
    for stuff in stuffs:
        print('What: %s, Where %s' % (stuff.thing, stuff.location))



