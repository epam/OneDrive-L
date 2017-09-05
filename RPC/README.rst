=====================
OneDrive Client - RPC
=====================

The project's RPC system is defined in this place.

Motivation
==========
This sub-project is created as a consequence of dissatisfaction with ZeroMQ
and other RPC systems. The purpose of it is to build a reliable RPC system,
which would handle peers disconnects reliably and provide message-delivery
guarantees. Another reason is desire to have freedom in choosing the
technology-stack.

Features
========
- Reliability. Particularly - reliable handling of peers disconnects using
  heartbeats.
- High-level interface for common communication patterns:
    - Request/Response.
    - Publish/Subscribe.
    - Producer/Consumer.
    - Broadcast.
    - Notification.
- Basic validation of messages.
- Pluggable transports.
- Language-independent contracts.
- Automatic generation of clients and servers for the services.

Architecture
============
The architecture consists of three layers:
- Transport layer.
- RPC layer.
- User-defined client/server layer.

Transport layer
---------------
Responsible for consistent and guaranteed delivery of messages as byte
sequences.

Transport layer abstracts concrete method of message-passing which could be
TCP, UDP, ZeroMQ, D-Bus, HTTP, etc.

RPC layer
---------
Responsible for:
- Maintaining connection with peers:
    - Tracking whether peers are "alive" or "dead" using heartbeats.
    - Tracking acknowledgements of messages when it's required.
- Implementing common communication patterns and providing high-level interface
  for using them.

RPC Layer is dependent on transport layer. At the same it should not depend
on any implementation details of particular transport implementation.

User-defined client/server layer.
---------------------------------
Responsible for providing stubs for servers and client for concrete services of
the application. Both are supposed to be thin wrappers around RPC layer
that route calls of concrete methods ("get_item()", "put()", etc) to correct
RPC calls made by methods implemented in RPC layer.

Generated clients are fully-functional accessors for associated services.
Server-stubs are server implementations that only lack business logic and
otherwise are fully-functional servers that can accept connections. Business
logic for server-stubs are supposed to be provided via call-backs by users of
the stub-classes.

Client and server-stub generation is supposed to be made based on
language-independent interface declarations (or contracts).

Technology stack
================
TCP - primary transport protocol.
Protobuf - as an interface declaration language, a tool for code-generation and
           serialization.
