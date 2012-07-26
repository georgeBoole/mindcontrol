# setup.py
# This code is mostly copied from the example on
# http://packages.python.org/an_example_pypi_project/setuptools.html

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mindcontrol",
    version = "0.7dev",
    author = "Michael Sobczak",
    author_email = "michaelsobczak54@gmail.com",
    description = ("Python wrappers for the NeuroSky Mindwave Headsets"),
    license = "GPLv3",
    keywords = "neurosky mindwave brainwave thinkgear",
    url = "http://packages.python.org/mindcontrol",
    packages=['mindcontrol','tests', 'examples'],
    long_description=read('README.txt'),

)