=============================
OneDrive Client RPC subsystem
=============================

.. contents:: Table of Contents

Features
========
1. **Automatic detection of disconnected/hung peers.**

   So users don't need to implement heartbeats or message acknowledgement
   mechanisms themselves (unlike ZeroMQ).
   Heartbeats and acknowledgement are optional features and whether
   they are used entirely depends on how the communication model is defined.
   So, for example, in case if user needs fast one-way messaging and is
   not concerned about guaranteed delivery they could be just not used in
   the communication model definition.
2. **High-level.**

   Provides many high-level communication models like publish-subscribe,
   request-response, command, etc.
   None of the communication model's logic is hardcoded, communication models
   are an extension point of the RPC system - they are defined in
   platform-independent DSL. New communication models could be added without
   modifying code in the target programming language.
3. **Reliable.**

   The protocol supports optional ACK-based message delivery tracking as
   well as non-optional duplicate packet detection using a sliding-window-style
   alghorithm.
4. **Transport agnostic.**

   Doesn't depend on any specific transport protocol. TCP, UDP, Unix-sockets,
   pipes could be used.
5. **Language independent.**

   Relies on Protobuf and language-independent definitions of communications
   models.
6. **Multiplexing.**

   Supports multiple logical communication sessions (potentially of different
   type and duration) over a single transport layer connection.
7. **Asynchronous by default.**

Architecture overview
=====================
The architecture consists of three layers:

  - **Transport layer**

    Consistently delivers byte sequences.
  - **Peer layer**

    Handles high-level communication models logic (whether it request-response,
    publish-subscribe or other), packet acknowledgement, duplicate packet
    detection, heartbeats and dead peers detection. Communication logic is not
    hardcoded but is pluggable and is defined in a platform-independent DSL.
  - **Facade layer**

    Provides auto-generation of service implementations based on declarations
    of concrete services in Protobuf. Contains mostly plumbing and none of
    the important logic.

Transport layer
===============
Provides basic means for process-to-process (or peer-to-peer) communication.

Key properties:

- MUST provide guarantee of delivery of data without corruption.
- MUST be capable to establish connections to unlimited number of peers and
  provide a public API for it.
- MUST be able to listen for coming data to a single address and provice
  a public API for it.
- It MUST possible to listen for inbound connections and connect to peers
  simultaneously.
- SHOULD NOT enforce datagram delivery order.
- SHOULD NOT be responsible for handling of lost datagrams.

Transport protocol could use different communication channels. TCP, UDP,
Unix-sockets, pipes could be used as communication channels and transmission
alghorithm could be different for each of them. At the same time
implementations of the transport protocol over different communication
channels must have the same interface and have the same properties as defined
above.

TCP transport
~~~~~~~~~~~~~
Sends datagrams_ over TCP connections with payload size encoded
in the header.

Datagram structure
******************
::

    MSB                                 LSB
    +---------+---------------------------+
    | Header  | Payload                   |
    +---------+---------------------------+
    | 4 bytes | As defined in the header. |
    +---------+---------------------------+

Peer layer
==========
Encapsulates high-level inter-process communication.

This is the most complex and important layer of the RPC protocol.
The central concepts of this layer are Session_, Model_ and Endpoint_.

In a few words
~~~~~~~~~~~~~~
Peers_ manage logical communication connections called sessions_  which could
follow different `communication models`_ defined as finite state machines.
Models are essentially plugins that implement different communication patterns
like request-response or publish-subscribe. No communication logic is
"hardcoded".

Peers_ pass messages between each other and internally feed them to
appropriate endpoints_ which are in turn transition internal state machines
defined by the models_.

Endpoints_ work as interpretators or virtual machines that execute programs
defined by the models-state-machines - they provide events as inputs and the
state machines generate actions and transition themselves to new states and
the endpoints in turn execute the actions. The events and the actions both
consist of finite number of elements. Example events are "inbound message is
received" or "user wants to send an outbound close request". Example actions
are "send the message with a payload" or "process the payload of the inbound
message".

Sessions
~~~~~~~~
Session_ is a logically separate communication cycle between two or more
peers_. The purpose of why this concept is introduced is to abstract logical
"connections" from transport-level connections and make it possible to have
multiple logical "connections" over a single transport connection - this is
called multiplexing.

Sessions_ have several important attributes:

  - Model_.
    The most important attribute of a session_. `Session's`_ model defines how
    communication progresses within the session_.
  - `Model type`_.
    Type of communication - one-to-one or many-to-one. Initiating side is on
    the left and the accepting is on the right.
  - Multiplicity.
    Depends on model type. If the initiating side is "many" there could be only
    one session at a time - it's called "singledton session". Otherwise
    unlimited number of different sessions could be created.
  - Session ID.
    Each session has an ID that helps to distuingish packets of one session
    from packets of another.
  - Service ID/Method ID.
    Session always belongs to a certain method. And Protobuf method definition
    in turn contains information about request/response messages format and
    model type.
  - Bi-directionality.
    In which direction packets are sent and when is entirely decided by
    the `session's`_ model_ except when the initial packet exchange is performed
    in `regular sessions`_.
  - Packet acknowledgement tracking/Duplicate packet tracking.
    These two things happen within a session using sliding-window-style
    alghorithm specified in the RPC protocol.
  - Session end.
    Session is considered to be ended by the peer when the model is
    transitioned to it's end-state. In contrast with session initiation there
    is no exact specification of how sessions are ended. It's entirely up
    to models to define in which circumstances the session is closed.

Session start / Session ID generation
*************************************
How `session ID`_ is generated is determined by whether the session_ is a
`singleton session`_ or a `regular session`_. And it is in turn determined by
the `session's`_ `model type`_.

In **all cases** the initiating side must set 'is_initial' flag to ``true`` in
the first packet. 'is_initial' flag MUST not be set to ``true`` in any other
situations.

In case of a **regular session** the initiating side MUST generate and
set 'session_id' field and then both the initiating and the accepting sides
MUST use it in all of the session's packets.

In case of a **singleton session** the session always MUST have a constant
session ID equal to ``0``. 'new_session_request_id' field must not be used at
all.

Packet exchange
***************
Primary concepts in packet exchange process are "packet window" and
"packet clearance". See the details below.

Packet batching
^^^^^^^^^^^^^^^
The protocol allows to merge multiple logical packets into one real packet if
there are no conflicts across their fields. For example if there is a need
to send a packet with some flag and also a packet with a payload - they MAY
be merged into one packet and sent in a batch.

Sender and receiver roles
^^^^^^^^^^^^^^^^^^^^^^^^^
In a session each participant could be both a sender and a receiver. Sender
is the peer who sent the packet and the receiver of the packet is a peer
who received it.

.. hint::
   Don't confuse terms "sender" and "receiver" with terms "initiating side" and
   "accepting side" - they have different meaning.

Packet ID
^^^^^^^^^
Each packet_ has an ID__. These IDs are used to identify duplicate packets when
a packet arrives more than once and also they are used to acknowledge the
packets that require acknowledgement.

Each next packet IDs is generated by application of MurmurHash3_ 32-bit hash
function to the previous packet ID so that the packet IDs form an infinite
ordered sequence.

The initial packet ID SHOULD be random.

__ _packet_id


Packet clearance
^^^^^^^^^^^^^^^^
The sender is responsible for "clearing" the sent packets. A packet is
considered to be cleared when the sender is satisfied with the delivery.

Packet window
^^^^^^^^^^^^^
The sender and the receiver maintain "packet window" which slides forward in
the infinite packet ID sequence as the sender clears the sent packets.

Window serves multiple purposes:

1. Unique packet IDs.

   Without window technique it would be hard to generate unique packet IDs -
   some sort of centralized facility would be needed or using larger ID
   value lengths to store something like UUIDs. Introduction of ID-window
   makes it possible to have limited amount of unique IDs at a time and
   by gradually sliding the window it's possible to generate new IDs for new
   packets.

2. Avoiding receiving duplicate packets / excessive amount of packets.

   When a sender clears a continuous interval of packet IDs on the left side
   of the packet window it moves the left boundary of the window forward.
   All packets to the left of the left boundary are considered to be cleared.
   And so when the receiver receives a packet which is outside of the window's
   boundaries it MUST discard it as a duplicate or as a packet that exceeds
   receiver's buffering capacity in case if it's ID is to the right of the
   window's right boundary.

Sender responsibilities
^^^^^^^^^^^^^^^^^^^^^^^
1. Generation of the first packet ID.

   The sender MUST generate the packet ID in the packet IDs sequence.
2. Clearing packets.

   There are two ways to clear a packet:

       a. By receiving an acknowledgement for a packet that required it.

          If the packet required an acknowledgement the sender MUST clear it
          only after receiving the acknowledgement from the receiver(s). To
          request an acknowledgement for a packet the sender sets
          'acknowledgement_required' field to ``true``. And when it receives
          a packet with the packet ID for the sent packet in 'acknowledges'
          collection field - it MUST clear the sent packet.

       b. When a packet that doesn't require an acknowledgement is sent it
          is cleared immediately.

          The sending side MAY implement clearing of packets that doesn't
          require an acknowledgement after sending the packet multiple
          times to improve reliability of packet delivery.

   .. hint:: Whether a packet requires acknowledgement or not is entirely
             determined by the session's model.

3. Maintenance of packet window.

   Sender maintains 'window_start' field. When a continuous interval of packet
   IDs adjacent to the left boundary of the window becomes cleared the sender
   could move the window's boundary the the left-most uncleared packet ID.
   When it happens is entirely up to the sender and its implementation.
   Sender must set 'window_start' field in each sent packet to the relevant
   value. This value is naturally can only progress forward.

Receiver responsibilities
^^^^^^^^^^^^^^^^^^^^^^^^^
1. Acknowledgement of packets that require it.

   If a received packet has 'acknowledgement_required' field set to ``true`` it
   signifies that the sender awaits an acknowledgement of this packet.

2. Tracking of "skipped packets".




.. _acknowledgements: _acknowledgement
.. _acknowledgement: https://en.wikipedia.org/wiki/Acknowledgement_(data_networks)
.. _sliding-window: https://en.wikipedia.org/wiki/Sliding_window_protocol
.. _packets: packet_
.. _packet ID: packet_id_
.. _MurmurHash3: https://en.wikipedia.org/wiki/MurmurHash#MurmurHash3

Model
~~~~~
Models are "communication models" - they are specifications of
implementations of various communication patterns like request-response or
publish-subscribe. Models are specified as finite state machines in a
specialized DSL separate from implementations in "real" programming
languages.

A model_ is an FSM with finite number of states, inputs ("events") and outputs
("actions").
A model_ works by consuming "events" and outputting "actions" and
transitioning itself to a new state (or staying at the same state). Models
also have some additional properties that are described in this section.

Models are also essentially plugins - a model contains the complete
speicifcation of communication alghorithm - they could be added or removed
without any modifications in the concrete protocol implementations.

Endpoints use models to track their state. They work as interpreters
that interpret the programs written in the form of FSM. They pass
events to them as an input and then receive actions as an output and
process them. Events and Actions are finite sets and the reader can
find their specification in the Protobuf code below.

.. note::

  FSM as a form to specify the models was chosen because it's very natural
  to think in terms of state machines about network connections and how
  peers connected via network track their state and their expectations about
  incoming messages as the communication cycle progresses. Finite state
  machines are very simple and leave little room for errors.

Models could be of two types:

One-to-one
  Sessions that use models of this type could be created in unlimited number
  by both initiating and accepting sides.

  Only two peers could participate in a session with a model of such type.

Many-to-one
  Multiple peers could enter a session with a single peer this model type
  is used.
  Only a single session of such models could be maintained at a time. Such
  session are called "singleton sessions".
  Though a single peer could maintain multiple endpoints for such a session.
  Peer on the accepting side always maintains only one endpoint for such a
  session which is always active.

Facade layer
============
Provides user-facing methods. The least complex layer. It contains mostly
pluming and "syntactic sugar". Code of this layer is supposed to be
auto-generated by Protobuf Compiler and provide wrappers around implementation
of the second layer.

Glossary
========
This section briefly describes commonly used terminology. It doesn't
contain any detailed info, look at the other sections for this.

.. _peer:

Peer
  An application process, a participant of a communication process
  identified by an "identity". A peer sends and receives arbitrary messages
  defined by the application.

.. _identity:

Identity
  Arbitrary string that uniquely identifies a peer and is used on
  application-level to specify message recipient(s).

.. _address:

Address
  Implementation of a transport procol uses address to connect to a peer.

.. _connection:

Connection
  Connection over the transport protocol.

.. _datagram:

Datagram
  Basic unit of communication of the transport proctol. Contains a payload
  and a header. Payload is a arbitrary sequence of bytes./ And header has
  the following structure.

.. _model:

Model/Communication model
  Implementation of a communication pattern such as request-response or
  publish-subscribe. Model is a declaration of an alghorithm that controls
  which messages of what kind must be sent to whom, in what order, when
  the session must be closed, etc.

  Models are defined in a special language-independent DSL as a
  specialized kind of finite state machine. Model is described by a number
  of states, transitions between them and some additional model-wise
  properties.

.. _model_type:

Model type
  TODO

.. _session:

Session
  Logical connection between two or more peers. What happens within a
  single session's lifetime is determined by the corresponding model.
  Multiple sessions could be created over a single transport protocol
  connection.

  Session is identified by one or more IDs which could be added or
  removed within session lifetime.

.. _session_id:

Session ID
  An ID that is stored in 'session_id' field of a packet that helps to
  distinguish which packet belongs to which session. It is needed to achieve
  multiplexing.

.. _regular_session:

Regular session
  A session_ that is not singleton_. A session_ with a model_ where the
  initiating side is ``one``. Multiple instances of sessions_ of this type
  could exist at a time with different session IDs.

.. _singleton: singleton_session_

.. _singleton_session:

Singleton session
  A session with a model where the initiating side is "many". Such sessions
  exist only one at a time and always have 'session_id' equal to ``0``.

.. _packet:

Packet
  TODO

.. _packet_id:

Packet ID
  TODO

.. _endpoint:

Endpoint
  Representation of the state of the participation of a peer in the
  session. It's the same as "socket" is for TCP/IP.

  Endpoint is described by it's current state (as defined in the model's
  state machine), "initiative" and known remote peers that are registered in
  the same session.

.. _initiative:

Initiative
  Initiative indicates whether the peer to which the endpoint belongs to
  initiated the session or accepted an incoming session initiated by
  another peer.

.. _peers: peer_
.. _communication models: model_
.. _communication model: model_
.. _models: model_
.. _endpoints: endpoint_
.. _sessions: session_
.. _`session's`: session_
.. _`regular sessions`: regular_session_
.. _`regular session`: regular_session_
.. _`singleton sessions`: singleton_session_
.. _`singleton session`: singleton_session_
.. _datagrams: datagram_
.. _initiating: initiative_
.. _accepting: initiative_
.. _`session ID`: session_id_
.. _`model type`: model_type_
