from setuptools import setup, find_packages
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ctfutils',
    version='0.1',
    description='Collection of utilities for use with my other CTF tools', 
    packages=find_packages(),
    install_requires=['argparse', 'colorama']
)
