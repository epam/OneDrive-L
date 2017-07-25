.. image:: https://travis-ci.org/epam/OneDrive-L.svg?branch=master
   :target: https://travis-ci.org/epam/OneDrive-L


OneDrive-L
==========
OneDrive for Business Linux client

Project Status
==============
The project is currently at the early development stage.

Development Setup
=================
The project uses Tox_ for managing Python environments.
To start using it you can install it by following `the installation
instructions`_ in it's documentation.

It defines several environments:

py36
    For running tests.
coverage
    For running coverage.py.
flake8 and pylint
    For static analysis.
dev
    For development.

To build and activate a development environment after you installed Tox you can
execute the following commands from the directory with ``tox.ini`` file::

   tox -edev
   . .tox/dev/bin/activate

For more information about how to use Tox refer to the `Tox documentation`_.

.. _Tox: https://tox.readthedocs.io/en/latest/
.. _Tox documentation: https://tox.readthedocs.io/en/latest/
.. _the installation instructions: https://tox.readthedocs.io/en/latest/install.html

TODO
====
- Breakdown the class diagram into several pieces and add an
  UML cheatsheet to it. Prettify it in general.
- Consider dropping the UML in favor of generic diagrams/annotations.
- Add business logic rules.
- Add specification of how race conditions during synchronization
  should be handled. For example - remotely moved file generates two events
  for deletion and for creation. If the client consumed the deletion event,
  found out that it's a move and started synchronizing it, how to avoid a
  conflict if the client then consumes the creation event?
- Consider giving the project it's own original name, because the current
  one is too generic.
