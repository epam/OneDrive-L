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

1. The architecture features service-oriented design.
   The main reason why it is done that way is because it allows to implement
   different components in different languages which could be instrumental
   in case of this project since some languages are more suitable for low
   level tasks (working with filesystem), offer more performance and some
   are more suitable for high-level tasks like business logic.
2. *StorageService* serves as a "hub" that stores information about changed
   (or "dirty") files and information about last successfully synchronized
   (or "pristine") files.
   Storing information about pristine files is required because otherwise it is
   impossible to make decisions about whether to overwrite a file or not
   (see the note in the diagram).
   Storing information about dirty files is required to free monitor-services
   from responsibility of ensuring that changes that they monitor are propagated
   and synchronized. With the Storage Service they could just save them and
   "forget" about them.
   It also allows to store arbitrary key-value data and this capability is
   used by OneDrive Service to store last known snapshot token.
3. *entities* package provides contracts that is used in communication
   between the services.
4. Util-classes provide basic infrastructural and domain-specific
   operations that are needed by higher-level components.
5. All the business logic related to how files are synchronized (e.g.
   conflict resolution, moves/copies handling) is encapsulated within
   *SynchronizationService*.
6. Protobuf and ZeroMQ are supposed to be used for interprocess communication.

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

Synchronization rules
---------------------
Generation of the business rules is automated and you can find the code that
implements the automation in `rules.ipynb` file.

======================================  ====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====
..                                      0     1      2      3      4      5      6      7      8      9      10     11     12     13     14     15     16     17     18     19     20     21     22     23     24     25     26     27
Conditions                              *     *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *
LOCAL_FILE_CHANGED                                                                                                         FALSE  TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE
REMOTE_FILE_CHANGED                                  TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   TRUE   FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  TRUE   TRUE   TRUE   TRUE
FILES_CONTENT_IS_SAME                         TRUE                                             FALSE  FALSE  FALSE  TRUE                                                           FALSE  FALSE  FALSE  TRUE                        TRUE
FILES_METADATA_IS_SAME                        TRUE                               FALSE  FALSE  FALSE  FALSE  FALSE  FALSE                                            FALSE  FALSE  FALSE  FALSE  FALSE  FALSE         FALSE  FALSE  FALSE
LOCAL_FILE_DOES_NOT_EXIST               TRUE  FALSE  TRUE   TRUE   TRUE   TRUE   FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  TRUE   FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE
REMOTE_FILE_DOES_NOT_EXIST              TRUE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  TRUE   TRUE   TRUE   TRUE   TRUE   FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  FALSE  TRUE   FALSE  FALSE  FALSE
LOCAL_COPIES_DO_EXIST                                FALSE  TRUE   TRUE   TRUE   FALSE  TRUE   FALSE  TRUE   TRUE                                                                                                            TRUE
REMOTE_COPIES_DO_EXIST                                                                                                            FALSE  TRUE   TRUE   TRUE          FALSE  TRUE   FALSE  TRUE   TRUE
LOCAL_COPY_COUNTERPART_DOES_NOT_EXIST                              FALSE  TRUE                        FALSE  TRUE                                                                                                            FALSE
REMOTE_COPY_COUNTERPART_DOES_NOT_EXIST                                                                                                          FALSE  TRUE                               FALSE  TRUE
LOCAL_COPY_METADATA_IS_SAME                                 FALSE                       FALSE
Actions                                 *     *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *      *
REMOTE_COPY_METADATA_IS_SAME                                                                                                             FALSE                              FALSE
DOWNLOAD_REMOTE_FILE                                 TRUE                                      TRUE
UPLOAD_LOCAL_FILE                                                                                                                 TRUE                                             TRUE
DELETE_REMOTE_FILE                                                                                                                                            TRUE
DELETE_LOCAL_FILE                                                                                                          TRUE
UPDATE_LOCAL_FILE_METADATA                                  TRUE                 TRUE   TRUE   TRUE                 TRUE                                                                                                            TRUE
UPDATE_REMOTE_FILE_METADATA                                                                                                              TRUE                        TRUE   TRUE   TRUE                 TRUE
RENAME_LOCAL_FILE                                                                                                                                                                                              TRUE   TRUE   TRUE   TRUE
COPY_LOCAL_FILE                                                    TRUE                               TRUE                                                                                                                   TRUE   TRUE
COPY_REMOTE_FILE                                                                                                                                TRUE                                      TRUE
MOVE_LOCAL_FILE                                                           TRUE                               TRUE
MOVE_REMOTE_FILE                                                                                                                                       TRUE                                      TRUE
DO_NOTHING                              TRUE  TRUE
======================================  ====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====  =====
