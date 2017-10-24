import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ofcsv2svg",
    version = "0.2",
    author = "Mondmann",
    author_email = "mondmann@co.zeitloos.de",
    description = ("Create SVG gantt diagram from OmniFocus CSV Export"),
    license = "GPLv3",
    keywords = "gantt omnifocus",
    url = "https://github.com/mondmann/ofcvs2svg-gantt",
    scripts=['ofcsv2svg/ofcsv2svg.py'],
    long_description=read('README.md'),
    install_requires=['python-gantt'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",

    ],
)
