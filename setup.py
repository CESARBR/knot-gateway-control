import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="control",
    version="1.0",
    author="Allysson Lukas",
    author_email="alla@cesar.org.br",
    description=("Daemon"),
    license="BSD-3-Clause",
    keywords="daemon control gateway iot dbus",
    url="https://github.com/CESARBR/knot-gateway-control",
    packages=find_packages(),
    long_description=read("README.md"),
    entry_points={
        "console_scripts": [
            "kcontrold = control.__main__:main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD 3-Clause License",
    ],
)
