from setuptools import setup, find_packages

setup(
    name='gcdmc',
    version='0.1.0',
    packages=find_packages(exclude=('tests', )),
    install_requires=[
        'google-cloud-datastore == 2.4.0',
        'phonenumbers == 8.12.40',
    ],
)
