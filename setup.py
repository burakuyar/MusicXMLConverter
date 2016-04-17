#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup


setup(name='musicxmlconverter',
      version='1.2.0',
      author='Burak Uyar',
      author_email='burakuyar@gmail.com',
      license='agpl 3.0',
      description='Tool for generating a MusicXML file from a SymbTr txt file.',
      url='https://github.com/burakuyar',
      packages=find_packages(),
      install_requires=[
          'numpy<=1.11.0',
          'lxml==3.6.0'
      ],
      include_package_data=True,
      )
