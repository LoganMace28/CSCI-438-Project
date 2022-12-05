# Emulation of Reliable Transport Protocol

## Task A: Emulated network topology
The main goal for this section of the project is to create a dynamic emulated network capable of dealing with lost nodes and additional nodes.

  This was partially achieved via simple data hiding, however the dynamic portion was not realized in our implementation.

## Task B. Emulation of point-to-point links
The main goal for this section is to create a peer-to-peer network of nodes that are able to communicate to each other via direct communication and forwarding

  This was realized through the use of threads and the socket library. Two threads are kept in a loop, one for sending and one for receiving. A third thread
  will be spun off as needed to handle forwarding. These two methods also make us of support methods to deal with acknowledgements sent by the receiving node.
  When a message is acknowledged, the sending node will display a checkmark by the sent message. If a message fails to be acknowledged, the sending node will
  attempt to resend it 5 times, if that fails it will display an x by the message

## Task C. The network protocol
The main goal here is to create a protocol that is able to transfer packets from one node to another with the inclusion of a TTL (time to live) header field.

  This again was partially realized in our project, as we have implemented a TTL field in our header to ensure messages can't loop forever. For demonstration
  purposes, the default TTL is initialized to 1 and thus the initial send of any node to a node greater than 1 hop away will fail. This is then rectified by
  as the sending node will increment the TTL by 1 causing the message send to succeed.
