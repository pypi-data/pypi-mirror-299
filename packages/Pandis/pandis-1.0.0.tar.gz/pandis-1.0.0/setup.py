# setup.py
from setuptools import setup, find_packages

setup(
    name='Pandis',
    version='1.0.0',
    description='A Redis-like interface using pandas as the data store.',
    author='Hamsa AI',
    author_email='support@tryhamsa.com',
    packages=find_packages(),
    install_requires=[
        'pandas==2.2.3',
    ],
    classifiers=[
    ],
)
