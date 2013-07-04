# Common Registration Based Communication Protocol (CRBCP)

It defines the Common Registration Based Communication Protocol (CRBCP).

## Common headers messages

CRBC/1.0 Register <name:([a..z][A-Z][0..9]([a..z][A-Z][0..9]-))*>\r\n
Time-to-live: 0|[1..9][0..9]*\r\n
\r\n

CRBC/1.0 Alias <name>\r\n
Time-to-live: 0|[1..9][0..9]*\r\n
Alias-for: <name:([a..z][A-Z][0..9]([a..z][A-Z][0..9]-))*>\r\n
\r\n

CRBC/1.0 Accept <name>\r\n
Status-code: [1..9][0..9]{2}\r\n
Reason-Phrase: (Status-code description; see below)\r\n
Time-to-live: 0|[1..9][0..9]*\r\n
\r\n

CRBC/1.0 Reject <name>\r\n
Status-code: [1..9][0..9]{2}\r\n
Reason-Phrase: (Status-code description; see below)\r\n
\r\n

CRBC/1.0 Send <name>\r\n
Body-size: [0..9]*\r\n
Flow-Id: <value:([a..z][A-Z][0..9]([a..z][A-Z][0..9]-))*>\r\n
\r\n
(Body-message: message)

CRBC/1.0 Received <name>\r\n
Status-code: [1..9][0..9]{2}\r\n
Reason-Phrase: (Status-code description; see below)\r\n
Body-size: [0..9]*\r\n
Flow-Id: <value:([a..z][A-Z][0..9]([a..z][A-Z][0..9]-))*>\r\n
\r\n
(Body-message: response)

CRBC/1.0 Unknown <name>\r\n
Status-code: [1..9][0..9]{2}\r\n
Reason-Phrase: (Status-code description; see below)\r\n
Body-size: [0..9]*\r\n
Flow-Id: <value:([a..z][A-Z][0..9]([a..z][A-Z][0..9]-))*>\r\n
\r\n

CRBC/1.0 General <name>\r\n
Status-code: [1..9][0..9]{2}\r\n
Reason-Phrase: (Status-code description; see below)\r\n
\r\n

## Status-codes and their (description) messages

100  Undefined name error (Method: Reject)
101  Name already in use (Method: Reject)
102  Name revoked (Method: Reject)
103  Wrong name pattern (Method: Reject)
110  Undefined registry error (Method: Reject)
111  Registry is full (Method: Reject)

200  Name accepted gracefully (Method: Accept)
201  Name aliased gracefully (Method: Accept)

300  Message sent and received gracefully (Method: Received)

400  Message fully understood, but doens't make any sense for me (Method: General)
401  Bad CRBC message (Method: General)
402  Unknown name destination (Method: Unknown)
403  That's not me (name non-repudiation) (Method: Unknown)
