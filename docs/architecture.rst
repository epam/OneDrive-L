Introduction
============

The goal of the project is to build a client for OneDrive for Business
for Linux that would be able to fulfill the the functionality of the
same, developed by Microsoft for Windows, and as future plans to provide
access to OneDrive Personal and be multi-platform.

This document concentrates on the initial phase of the development and
discusses only the aspects of the projects that are related to this
phase.

Requirements 
============

1. File synchronization.

   1. The client should properly resolve file conflicts.
   2. Moves and copies should be handled efficiently.

2. Reliability.

   1. File corruption prevention.
      The client should try hard to not corrupt the user’s files while
      working and in case of abrupt terminations.
   2. Graceful termination.

3. Command Line Interface.

   1. Headless mode.
      CLI should provide a way to use the client fully without GUI
      (including the authentication step).

4. Performance.

   1. Network connection should be used efficiently.

Resources
=========

This section outlines the resources available that could be used in the development.
====================================================================================

OneDrive API
------------

1. Has good documentation:
   https://dev.onedrive.com/README.htm

   1. It is hosted on GitHub:
      https://github.com/OneDrive/onedrive-api-docs
   2. If you want to search through it, search directly on
      GitHub, because the web-site doesn’t have it.

   3. GitHub, authors usually respond quickly – within 24 hours.

2. Has official SDKs for:

   1. `C# <https://github.com/OneDrive/onedrive-sdk-csharp>`_
   2. `Python <https://github.com/OneDrive/onedrive-sdk-python>`_

3. Supports *check-and-swap* operations using headers
   `“if-match” <https://github.com/OneDrive/onedrive-api-docs/blob/bede978b6a9c5a107306dd779b878af387a5dcbb/items/update.md#optional-request-headers>`_
   and “if-none-match”. Their usage is not fully documented though, see:

   1. https://github.com/OneDrive/onedrive-api-docs/issues/607

   2. https://github.com/OneDrive/onedrive-api-docs/issues/608

4. Does not support methods for operating on file versions:
   https://github.com/OneDrive/onedrive-api-docs/issues/559

5. Delta method is recommended for querying for changes AND for listing files:
   https://dev.onedrive.com/items/view_delta.htm

File changes monitoring libraries
---------------------------------

1. Python

   1. `Pyinotify <https://pypi.python.org/pypi/pyinotify/>`_

      1. Popular.
      2. Cross-platform.
      3. Unmaintained.
      4. Latest release and commit on 2015-06-04.
      5. A lot of unanswered open issues on GitHub.
      6. Some people do not recommend it:
         http://www.serpentine.com/blog/2008/01/04/why-you-should-not-use-pyinotify/

   2. `inotify <https://pypi.python.org/pypi/inotify>`_

      1. Suggested by Artur.
      2. Development stalled just recently.
      3. Latest commit on Dec 15, 2016.

   3. `fsmonitor <https://github.com/shaurz/fsmonitor>`_

      1. Semi-actively developed.
      2. Latest commit in 2017

2. C

   1. `Inotify-tools <https://github.com/rvoicilas/inotify-tools>`__

      1. Popular.
      2. Seems abandoned.
      3. Latest commit on Nov 9, 2014.

3. C++

   1. `fswatch <https://github.com/emcrisostomo/fswatch>`__

      1. Popular.
      2. Cross-platform.
      3. Seems like it just entered the phase when
         developers do not develop it actively.
      4. Latest commit on Jul 23, 2016.

   2. `efsw <https://bitbucket.org/SpartanJ/efsw>`__

      1. Somewhat popular (hard to say with Bitbucket).
      2. Maintained.
      3. Latest commit 2017-03-29.
      4. Cross-platform.

Architecture
============

Components overview
-------------------

.. figure:: components.png
   :width: 100%
   :alt: Components overview

   Figure 1.0

Highlights:

1. *SynchronizationStateStorageService* stores metadata for last
   successfully synchronized files. It is required because otherwise it
   is impossible to make decisions about whether to overwrite a file or
   not (see the note in the diagram).
2. Service-classes provide basic infrastructural and domain-specific
   operations that are needed by higher-level components.
3. *entities* package contains entity-definitions that are 1 to 1 match
   to the OneDrive API entities.
4. *DataStorageService* is used for storing arbitrary data. Currently it
   is required for storing last snapshot token returned by the API (see
   delta method).
5. All the business logic related to how files are synchronized (e.g.
   conflict resolution, moves/copies handling) is encapsulated within
   *SynchronizationService*.
6. Synchronizer service does not contain business logic, but instead
   assembles all the components required for synchronization, bootstraps
   a synchronization process and continuously monitors and synchronizes
   changes.
7. The whole system is supposed to be built on cooperative concurrency
   execution model.
   Most probably it will be gevent.
   This choice was made because the project deals with events and I/O so
   a light-weight concurrency + task scheduler, that gevent provides
   “for free”, seems to fit perfectly.

Files synchronization
---------------------

Here is a list of basic synchronization tasks/problems:

1. Conflict resolution.

   1. How to detect a conflict?
      Let’s define “conflict” as mismatch between last known state of a
      synchronized remote or local file and the current state of the file when
      the opposite state initiated a change.
      Let’s suppose we have fileA, that is synchronized between the local side
      and the remote side.

      Conflict type #1:

          - Remote file is changed.
          - Local file, compared to the last known sync-state, is different.

      Conflict type #2:

          - Local file is changed.
          - Remote file, compared to the last known sync-state, is different.

      Conflict resolution logic:
          - If conflict (type #1 or #2) occurred, local file should be
            renamed and put under synchronization. Remote file always “wins”
            since it represents synchronized file tree.
          - In case if there is no conflict – remote or local file should
            be overwritten or a new file should be created if it doesn’t
            exist on the opposite side.

      1. All that implies, that last known state of a synchronized files
         should be stored. This is the reason, why an **embedded
         storage** should be used.
         Without using a storage of last known synchronized file state
         it is impossible to detect conflicts.

   2. How a conflict should be solved?
      Conflicts are resolved by creating file copies according to
      specific rules.

2. Changes detection.

   1. How to monitor local changes?
      For that there is a number of existing libraries, and one of them
      should probably be used.
   2. How to detect remote changes?
      There are two solutions:

      1. By using `“delta” API
         method <https://dev.onedrive.com/items/view_delta.htm>`__,
         which allows to create snapshot and retrieve a delta between
         the previous snapshot and the current state in one
         request-response cycle.

3. Consistent writes.

   1. For remote writes consistency CAS operations should be used. They
      are supported by the OneDrive API as “if-match” and
      “if-none-match” headers (see the docs for the details).
   2. For local writes consistency OS-level or filesystem-level locks
      could be used.

4. Startup synchronization.

   1. How to initialize synchronization at startup?
      At startup the client should compare all the files and propagate
      needed changes.

5. Moves/copies handling.

   1. Moves and copies should be handled efficiently by re-using
      existing remote and local files and avoiding redundant
      downloads/uploads.
