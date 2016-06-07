try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Treasure Finder',
    'author': 'Fenimore Love',
    'url': 'https://github.com/polypmer/freestuff-bot',
    'download_url': 'https://github.com/polypmer/freestuff-bot',
    'author_email': 'exorable.ludos@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'folium','geopy','beautifulsoup4', 'requests', 'tweepy'],
    'packages': ['freestuff-bot'],
    'scripts': [],
    'name': 'freestuff-bot'
}

setup(**config)
