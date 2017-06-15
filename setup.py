#!/usr/bin/env python
# coding=utf-8
"""Distribution configuration."""
import os

from setuptools import find_packages, setup


README_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'README.rst'
)


setup(
    name='onedrive_client',
    author='EPAM Systems',
    author_email='OneDriveTeam@epam.com',
    description='OneDrive Client',
    long_description=open(README_PATH).read(),
    packages=find_packages(where='src', include=[]),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=map(str.strip, open('requirements.txt')),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Utilities'
    ]
)
