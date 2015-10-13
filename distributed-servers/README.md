# CRBCP v1.0

## Common Registration Based Communication Protocol

WARNING: THIS PROJECT IS INTENDED TO DEVELOP CONCEPTS IN COMPUTER NETWORKING AND DISTRIBUTED SYSTEMS.
IT IS NOT INTENDED FOR REAL WORLD USE.

The present project aims to establish a protocol over the TCP/IP stack to communicate through the
exchange of messages based on registration mechanisms. It defines thus the Common Registration Based
Communication Protocol (CRBCP). This project also presents a reference implementation of that protocol
in several programming languages: Python, Ruby, and Java.

In CRBCP it is defined two kind of entities: a registry, a register container, analagous to a router
--- in networking concepts and terminology a real router doesn't implement all the TCP/IP stack, what
does happen for a "registry" entity in CRBCP; and a communicant, an entity that aims to establish a
communication over the CRBC protocol. A communicant could be a server, a client or both.

In a CRBCP based communication there are two main processes: a establishment process, that aims to
register a communicant in a previously known registry (or even registries); and a communication process,
when a communicant previously registered sends CRBCP messages (in this specification, CRBCP bundles)
over the network, through the protocol.

The sections below will present some concepts and deeper considerations about the protocol.

## Motivations for a registration based communication protocol

An obvious motivation is a means of masking TCP/IP (host, port) tuple, majorly necessary to establish
a communication process. A communicant entity registers its name in a registry host, and then it may
exchange messages to every known communicants in that "communication section". If someone "unknown"
sends a message to any communicant in a section, the later may drop the message; it only establishes
a communication process to another communicant in a section.

Another motivation, related to the later one, is a way to establish a communication process only
knowing the "proper name" of another communicant. There's no need for host and port values.

## CRBCP bundles; or CRBCP messages and attributes

Below is presented how messages in CRBCP are established. The first line is known as the "presentation
line", respectively formated as {CRBCP version}, {Method}, and {Communicant name}. The meaning of the
{Communicant name} vary according to the {Method} in a message.

The four messages shown below correspond to the "establishment process bundles"; they are messages
used to establish the registration of a communicant entity. The {Time-to-live} field sets the seconds
a communicant has to be known by the registry. When it is setted to 0, it means it should be known
"forever"; although the registry is not forced to guarantee that. The {Status-code} and the {Reason-Phrase}
fields establishes the status of the returnee messages. The is a set of Status-codes and their
Reason-phrases specified down below.

In {Register}, {Alias}, {Accept} and {Reject}, the given name is about the communicant that wants to
establish a registration process.

CRBC/1.0 Register {name : ([a..z][A-Z][0..9]([a..z][A-Z][0..9]-))*}\r\n<br>
Time-to-live: 0|[1..9][0..9]*\r\n<br>
\r\n

CRBC/1.0 Alias {name}\r\n<br>
Time-to-live: 0|[1..9][0..9]*\r\n<br>
Alias-for: {name : ([a..z][A-Z][0..9]([a..z][A-Z][0..9]-))*}\r\n<br>
\r\n

CRBC/1.0 Accept {name}\r\n<br>
Status-code: [1..9][0..9]{2}\r\n<br>
Reason-Phrase: (Status-code description; see below)\r\n<br>
Time-to-live: 0|[1..9][0..9]*\r\n<br>
\r\n

CRBC/1.0 Reject {name}\r\n<br>
Status-code: [1..9][0..9]{2}\r\n<br>
Reason-Phrase: (Status-code description; see below)\r\n<br>
\r\n

The three messages below are used for the "communication process" by the communicants in a communication
section. The {Body-size} fields sets the size of the message sent by the number of caracters (Unicode);
the {Flow-Id} identifies a communication process between two communicants --- both values are setted by
the original communicant. The {Send} method is sent by the original communicant to a registry; if the
registry know the given name, it forwards the message to the corresponding communicant. When the recipient
communicant reveices the message, it answers the registry entity with a {Received} method and gives the
proper {Status-code} and related {Reason-Phrase} for that communication flow. Then the registry entity
forwards the message to the original communicant. If the registry unknown any of the given communicant
names, it answers the given communicant with the {Unknown} method.

In {Send}, {Received}, and {Unknown}, the given name is about the adressee communicant.

CRBC/1.0 Send {name}\r\n<br>
Body-size: [0..9]*\r\n<br>
Flow-Id: {value : ([a..z][A-Z][0..9]([a..z][A-Z][0..9]-))*}\r\n<br>
\r\n<br>
(Body-message: message)

CRBC/1.0 Received {name}\r\n<br>
Status-code: [1..9][0..9]{2}\r\n<br>
Reason-Phrase: (Status-code description; see below)\r\n<br>
Body-size: [0..9]*\r\n<br>
Flow-Id: {value : ([a..z][A-Z][0..9]([a..z][A-Z][0..9]-))*}\r\n<br>
\r\n<br>
(Body-message: response)

CRBC/1.0 Unknown {name}\r\n<br>
Status-code: [1..9][0..9]{2}\r\n<br>
Reason-Phrase: (Status-code description; see below)\r\n<br>
Body-size: [0..9]*\r\n<br>
Flow-Id: {value : ([a..z][A-Z][0..9]([a..z][A-Z][0..9]-))*}\r\n<br>
\r\n

The last message kind is a {General} method. Its purpose is to enable a general message, when it is
not possible to use the later messages. Its purpose is to prepare the protocol for any future extension.

In {General} the given name is not a concise information and is determined by the message intents (with
the help of the proper Status-code).

CRBC/1.0 General {name}\r\n<br>
Status-code: [1..9][0..9]{2}\r\n<br>
Reason-Phrase: (Status-code description; see below)\r\n<br>
\r\n

## Status-codes and their Reason-Phrase messages

The Status-codes are three digits values, organized as follow: 1xx relates to registration process errors;
10x relates to given names errors; 11x relates to registry errors; 2xx relates to successful names
registration or aliasing; 3xx relates to successful communication status; 4xx relates to errors and problems
that prevents a successful functioning of the protocol; and 5xx are user-defined Status-codes.

100  Undefined name error (Method: Reject)<br>
101  Name already in use (Method: Reject)<br>
102  Name revoked (Method: Reject)<br>
103  Wrong name pattern (Method: Reject)<br>
110  Undefined registry error (Method: Reject)<br>
111  Registry is full (Method: Reject)

200  Name accepted gracefully (Method: Accept)<br>
201  Name aliased gracefully (Method: Accept)<br>
202  Name accepted, but restricted Time-to-live value was applied (Method: Accept)

300  Message sent and received gracefully (Method: Received)

400  Message fully understood, but doens't make any sense for me (Method: General)<br>
401  Bad CRBC message (Method: General)<br>
402  Unknown name destination (Method: Unknown)<br>
403  That's not me (non-repudiation) (Method: Unknown)

## License

Apache License, Version 2.0. Copyright 2011-2014 &copy; Ewerton Assis.
