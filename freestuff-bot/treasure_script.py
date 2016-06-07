#!/usr/bin/env python
"""Freestuff script"""
from stuffify import Stuffify
from mappify import Mappify

stuffs = Stuffify('montreal', 5, precise=True).get_freestuffs()
Mappify(stuffs, is_testing=True)

