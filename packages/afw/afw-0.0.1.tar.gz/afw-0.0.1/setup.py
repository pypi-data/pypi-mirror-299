from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='afw', # name of packe which will be package dir below project
    version='0.0.1',
    url='https://github.com/tsachikotek/AFW',
    author='Tsachi Kotek',
    author_email='tsachikotek@gmail.com',
    description='Tests Automation Framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
)