"""
OneDrive for Business Linux client
-------------

An interface to One Drive for Business services

"""

from setuptools import setup

setup(
    name="od4b",
    version="0.0.1",
    license="MIT",
    author="EPAM Systems",
    author_email="info@epam.com",
    description="OneDrive for Business ",
    long_description=__doc__,
    packages=["od4b"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=[
    ],
    tests_require=[
        "nose",
    ],
    test_suite='nose.collector',
    keywords=['OneDrive', 'client', 'linux'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Communications",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: Utilities"
    ]
)
