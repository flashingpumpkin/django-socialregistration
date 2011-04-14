#!/usr/bin/env python
from setuptools import setup,find_packages

METADATA = dict(
    name='django-socialregistration',
    version='0.4.4',
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    description='Django application enabling registration through a variety of APIs',
    long_description=open('README.rst').read(),
    url='http://github.com/flashingpumpkin/django-socialregistration',
    keywords='django facebook twitter oauth openid registration',
    install_requires=['oauth2', 'python-openid'],
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
    zip_safe = False,
    packages=find_packages(),
    package_data={'socialregistration': ['templates/socialregistration/*.html'], }
)

if __name__ == '__main__':
    setup(**METADATA)
    
