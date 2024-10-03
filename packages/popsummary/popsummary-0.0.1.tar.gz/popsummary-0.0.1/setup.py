#!/usr/bin/env python
"""
Adapted from setup.py authored by Colm Talbot at https://github.com/ColmTalbot/gwpopulation/blob/master/setup.py
"""
from setuptools import setup

setup(
    name='popsummary',
    version='0.0.1',
    url='https://git.ligo.org/zoheyr-doctor/popsummary',
    author = 'Christian Adamcewicz and Zoheyr Doctor',
    author_email = 'christian.adamcewicz@ligo.org',
    description = 'tool for reading and writing standard data products from LIGO-Virgo-KAGRA rates and populations analyses',
    packages = ['popsummary'],
    py_modules = ['popsummary.popresult'],
    install_requires=["h5py", "numpy"],
    extras_require=dict(
        test=["scipy", "nbconvert", "nbstrip", "ipykernel"]
    ),
	python_requires=">=3.9",
)

