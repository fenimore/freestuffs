import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
setup(
    name='freestuffs',
    description='Find free stuff near you!',
    version='0.1',
    author='Fenimore Love',
    license='MIT',
    url='https://github.com/polypmer/freestuffs',
    packages=['freestuffs',],
    include_package_data=True,
    install_requirements=['nose', 'folium','geopy','beautifulsoup4', 'requests', 'unidecode'],
    long_description=read('README.rst'),
)
