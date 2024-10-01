from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A simple module to assist in physics bachelor'

# Setting up
setup(
    name="weltetools",
    version=VERSION,
    author="Paul Welte",
    description=DESCRIPTION,
    packages=["weltetools"],
    install_requires=['scipy']
)