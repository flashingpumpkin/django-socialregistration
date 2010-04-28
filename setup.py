#!/usr/bin/env python

METADATA = dict(
    name='django-socialregistration',
    version='0.3.2',
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    description='Django application enabling registration through a variety of APIs',
    long_description=open('README.rst').read(),
    url='http://github.com/flashingpumpkin/django-socialregistration',
    keywords='django facebook twitter oauth openid registration',
)
SETUPTOOLS_METADATA = dict(
    install_requires=['setuptools', 'django', 'oauth2', 'python-openid'],
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
    packages=['socialregistration', 'socialregistration.templatetags'],
    package_data={'socialregistration': ['templates/socialregistration/*.html'], }
)

if __name__ == '__main__':
    try:
        import setuptools
        METADATA.update(SETUPTOOLS_METADATA)
        setuptools.setup(**METADATA)
    except ImportError:
        import distutils.core
        distutils.core.setup(**METADATA)
