import pathlib
from setuptools import setup

setup(
    name='gcdmc',
    version='0.1.0',
    packages=['gcdmc'],
    install_requires=[
        'google-cloud-datastore == 2.4.0',
        'phonenumbers == 8.12.40'
    ],
)
