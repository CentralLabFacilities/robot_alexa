# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='rlservicelib',
      version='0.1.0',
      long_description=__doc__,
      packages=['rlservicelib'],
      url='https://opensource.cit-ec.de/projects/citk/repository/tools',
      install_requires=['requests', 'flask_restful', 'flask_cors'],
      scripts=['remotelabservice.py', 'naoqiRestServer.py']
      )
