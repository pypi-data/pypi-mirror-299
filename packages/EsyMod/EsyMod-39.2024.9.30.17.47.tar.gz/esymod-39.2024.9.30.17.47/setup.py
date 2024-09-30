# -*- coding:utf-8 -*-
import sys
sys.argv.append('sdist')
from distutils.core import setup
from setuptools import find_packages

setup(name='EsyMod',
            version='39.2024.9.30.17.47',
            packages=['EsyMod',],
            description='a python lib for project files',
            long_description='',
            author='Quanfa',
            package_data={
            '': ['*.*'],
            },
            author_email='quanfa@tju.edu.cn',
            url='http://www.xxxxx.com/',
            license='MIT',
            )

            