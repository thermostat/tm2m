
"""
Packaging for tm2m
"""

import setuptools
from setuptools import setup

setup(
    name='tm2m',
    scripts=['bin/tm2m', 'bin/tm2m_pick'],
    version="0.2",
    install_requires=['pick']
    )
