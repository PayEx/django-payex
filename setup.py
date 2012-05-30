#!/usr/bin/env python
import os
import sys

from djpayex import __version__
from setuptools import setup


# Publish to Pypi
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

setup(
    name='django-payex',
    version=__version__,
    description='Django application for saving statuses and receiving callbacks from the PayEx API.',
    long_description=open('README.md').read(),
    author='Funkbit AS',
    author_email='post@funkbit.no',
    url='https://github.com/funkbit/django-payex',
    packages=['djpayex',],
    license='BSD',
    classifiers = (
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    )
)
