#!/usr/bin/python
# -*- coding=utf-8 -*-
from setuptools import setup

# to install type:
# python setup.py install --root=/
from io import open
def readme():
    with open('README.rst', encoding="utf8") as f:
        return f.read()

setup (name='semawal', version='0.4',
      description="Semawal: Semantic Network Resolver",
      long_description = readme(),      

      author='Ali Aouf',
      author_email='ali.aouf@gmail.com',
      url='https://40uf411.github.io/SemaWal/',
      license='GPL',
      package_dir={'semawal': 'semawal'},
      packages=['semawal'],
      install_requires=[
      ],         
      include_package_data=True,
      package_data = {
        'semawal': ['doc/*.*','doc/html/*', 'data/*.sqlite', 'data/*.sql'],
        },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: End Users/Desktop',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          ],
    );

