#!/usr/bin/env python
from setuptools import setup, find_packages
import socialregistration

METADATA = dict(
    name='django-socialregistration',
    version=socialregistration.__version__,
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    description='Django app providing registration through a variety of APIs',
    long_description=open('README.rst').read(),
    url='http://github.com/flashingpumpkin/django-socialregistration',
    keywords='django facebook twitter oauth openid registration foursquare '\
        'linkedin github oauth2',
    install_requires=['oauth2', 'python-openid', 'mock'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    packages=filter(lambda pack: not pack.startswith('example'), find_packages()),
)

if __name__ == '__main__':
    setup(**METADATA)
