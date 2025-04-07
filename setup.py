"""Setup for Click to define entry points."""

from setuptools import setup

setup(
    name='m3',
    version='0.1.0',
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'm3 = m3.m3'
        ]
    }
)
