#!/usr/bin/python
# -*- coding=utf-8 -*-
from setuptools import setup

# to install type:
# python setup.py install --root=/
from io import open
def readme():
    # Updated to read README.md instead of README.rst
    with open('README.md', encoding="utf8") as f:
        return f.read()

setup (name='semawal', version='0.3.0', # Version updated
      description="SemaWal: Semantic Network Resolver",
      long_description = readme(),
      long_description_content_type='text/markdown', # Added content type

      author='Ali Aouf',
      author_email='40uf4l1@gmail.com',
      url='https://40uf411.github.io/SemaWal/',
      license='GPL-3.0-or-later', # Made license more specific
      python_requires='>=3.6', # Added python_requires
      package_dir={'semawal': 'semawal'},
      packages=['semawal'],
      install_requires=[
      ],         
      include_package_data=True,
      package_data = {
        'semawal': ['doc/*.*','doc/html/*', 'data/*.sqlite', 'data/*.sql'],
        },
      classifiers=[
          'Development Status :: 4 - Beta', # Updated Development Status
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers', # Added Developers
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)', # Added GPLv3+ classifier
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3', # Specify Python 3
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Topic :: Scientific/Engineering :: Information Analysis', # Added relevant topic
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
    );

