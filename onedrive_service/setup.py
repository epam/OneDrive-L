#!/usr/bin/env python
# coding=utf-8
"""Distribution configuration."""
import os

from setuptools import find_packages, setup
import versioneer


REQUIREMENTS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'requirements.txt'
)


setup(
    name='onedrive_service',
    author='EPAM Systems',
    author_email='OneDriveTeam@epam.com',
    description='OneDrive Client - OneDrive Service',
    packages=find_packages(where='src', include=[]),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=map(str.strip, open(REQUIREMENTS_PATH)),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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
