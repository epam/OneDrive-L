.. image:: https://travis-ci.org/epam/OneDrive-L.svg?branch=master
   :target: https://travis-ci.org/epam/OneDrive-L


OneDrive-L
==========
OneDrive for Business Linux client

Project Status
==============
The project is currently at the early development stage.

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
- Choose between supporting multiple versions of Python and the libraries
  and pin the versions and distribute all the dependencies within
  the client's distribution.
- Consider giving the project it's own original name, because the current
  one is too generic.
