#!/usr/bin/env python
# coding=utf-8
"""Distribution configuration."""
import os

from setuptools import find_packages, setup


REQUIREMENTS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'requirements.txt'
)


setup(
    name='onedrive_client.entities_protoc_plugin',
    namespace_packages=['onedrive_client'],
    version='0.0.1',
    author='EPAM Systems',
    author_email='OneDriveTeam@epam.com',
    description='OneDrive Client - Entities - Protoc Plugin',
    packages=find_packages(
        where='src',
        include=['onedrive_client', 'onedrive_client.*']
    ),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=list(map(str.strip, open(REQUIREMENTS_PATH))),
    entry_points={
        'console_scripts': [
            'protoc-gen-entities=onedrive_client.entities_protoc_plugin.'
            'protoc_plugin:main'
        ]
    },
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
