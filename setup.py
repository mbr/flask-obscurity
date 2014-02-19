import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='Flask-Obscurity',
    version='0.3',
    url='http://github.com/mbr/flask-obscurity',
    license='BSD',
    author='Marc Brinkmann',
    author_email='git@marcbrinkmann.de',
    description='Security-by-obscurity. Move along, nothing to see here.',
    long_description=read('README.rst'),
    packages=['flask_obscurity'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.8', 'six>=1.5.2'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
