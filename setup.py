import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = open('requirements.txt').read().splitlines()


setup(
    name='freestuffs',
    description='Find free stuff near you!',
    version='0.1.2',
    author='Fenimore Love',
    license='MIT',
    url='https://github.com/fenimore/freestuffs',
    packages=['freestuffs',],
    include_package_data=True,
    install_requires=requirements,
    long_description=read('README.rst'),
)
