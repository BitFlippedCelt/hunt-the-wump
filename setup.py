__author__ = 'petastream'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Hunt the Wumpus python style.',
    'author': 'Petastream',
    'url': '',
    'download_url': '',
    'author_email': 'petastream@gmail.com',
    'version': '0.1',
    #'install_requires': [],
    'packages': ['game'],
    'scripts': ['bin/wumpus.py'],
    'name': 'HuntTheWumpus'
}

setup(
    **config
)