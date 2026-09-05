# HERESY-API

> **A software-art joke about APIs, abstraction, ceremony, and the heroic number of tokens sometimes required to say almost nothing.**

HERESY-API asks a deeply irresponsible question:

**What if we judged modern API ceremony by making it compete with punch cards, magnetic tape, fixed-width files, raw sockets, and other historical monsters?**

The project is not an argument that punch cards were better. They were not. It is an argument that every abstraction should occasionally be dragged into a fluorescent-lit basement and asked to justify its byte count.

## The canonical scientific experiment

We need a computer to perform the advanced distributed-systems workload:

```text
ADD 2 2
```

HERESY-API expresses that same tiny intent through increasingly ceremonial interfaces and measures the resulting application-level payload.

```bash
python3 heresy.py
```

You will receive a **Ceremony Ratio**: exhibit payload bytes divided by the seven bytes of useful canonical intent.

The token estimate is deliberately crude (`ceil(UTF-8 bytes / 4)`). It is a joke-meter, not a tokenizer, benchmark, protocol-efficiency paper, or invoice predictor.

## Current exhibits

| Exhibit | Era / style | Curatorial interpretation |
| --- | --- | --- |
| Punch Card | 1940s-1960s | Uses 80 columns because storage had furniture. |
| Magnetic Tape | 1950s-1980s | Sequential access. Please rewind your microservice. |
| Raw Socket | 1970s-1980s | Nine application bytes. Documentation: `good luck`. |
| FTP Batch | 1970s-1990s | Real-time, provided your definition of real-time includes tomorrow morning. |
| RPC-ish | 1980s-1990s | Pretends the network is a function call until the network remembers it is a network. |
| SOAP-ish | 1990s-2000s | The request has entered the XML cathedral. |
| REST-ish JSON | modern web | Human-readable bureaucracy. Authentication pending: Dave lost the API key again. |
| GraphQL-ish | modern web | Ask precisely for what you need, after introducing yourself to the syntax tree. |
| Agent Tool Call | current AI stack | Seven useful bytes escorted by a schema, description, arguments, and several responsible adults. |

## The Heresies

1. **Every byte must explain why it exists.**
2. **JSON is not an emotional-support syntax.**
3. **A schema can prevent chaos and still become baroque. Both things can be true.**
4. **Tokens are a computational resource, not decorative confetti.**
5. **Human-readable does not automatically mean machine-efficient.**
6. **If `ADD 2 2` needs three abstraction layers, the punch-card operator is allowed one smug cigarette break.**
7. **The worst historical interface can still make a useful punchline about the present one.**
8. **An API key stored safely is apparently indistinguishable from an API key lost forever.**

## Why the heretics occasionally have a point

This is where the joke gets annoyingly defensible.

### TCP

TCP gives you an ordered, reliable byte stream. If both ends are under your control, you can put a tiny binary or fixed-width protocol directly on that stream instead of wrapping every request in HTTP headers, JSON field names, versioned routes, content negotiation, and whatever else followed the architecture astronaut into the meeting.

Long-lived TCP connections can also keep application chatter compact once framing is established.

**Heresy:** sometimes the shortest API documentation really can be `opcode 0x01 + two int32s`.

**Reality check:** TCP only gives you the stream. Message framing, authentication, versioning, schema evolution, observability, security, retries above the stream, and not ruining production remain your problem.

### UDP

UDP preserves datagram boundaries and has no transport-level connection handshake. That makes it attractive for workloads where sending the newest state quickly matters more than waiting to recover stale state, such as some telemetry, real-time media, games, discovery, and tightly controlled protocols.

**Heresy:** the packet can simply leave. It does not need a meeting invite.

**Reality check:** delivery, ordering, retransmission, authentication, congestion behavior, and application semantics may need to be supplied elsewhere. Small is not the same thing as complete.

### FTP and batch files

For the ancient business requirement **MOVE THIS FILE OVER THERE**, a file-transfer workflow can be beautifully literal. Files are easy to inspect, archive, checksum, retry, replay, process asynchronously, and hand to another tool without first inventing a resource model for them.

That is why batch exchange refuses to die in finance, science, industry, and enterprise integration. Sometimes a durable file is the interface.

**Heresy:** yesterday's `results.dat` does not need twelve endpoints and an SDK.

**Reality check:** plain FTP does not encrypt credentials or data. Secure deployments need an appropriate protected alternative or tunnel, and batch transfer is obviously a poor fit when low latency is actually required.

## Modern authentication ceremony

A typical contemporary integration lifecycle:

```text
1. Put API key in .env
2. Forget which .env
3. Search .env.local, .env.old, .env.backup and notes-final-FINAL.txt
4. Find key in shell history
5. Rotate key because finding it in shell history is bad
6. Update every service except the one that matters
7. Receive HTTP 401
8. Consider magnetic tape
```

Punch-card authentication had one underrated property: **if you lost the credential, it was probably underneath the desk and remained visible to the naked eye.**

## What this project is actually making fun of

The target is not REST, GraphQL, SOAP, RPC, JSON, XML, LLM tooling, or API designers individually. All of those exist for reasons.

The target is **ceremony without proportional value**: duplicated metadata, compulsive envelopes, needless verbosity, abstraction piled onto abstraction, token-heavy machine-to-machine chatter, and interfaces that spend more effort describing the request than expressing it.

That distinction matters. Satire is much funnier when it knows what the engineering trade-off actually was.

## Planned gallery wings

- **PUNCHCARD/1.0**: emit an actual 80-column card image for requests.
- **TAPE/1.0**: append-only virtual tape with rewind latency theatre.
- **FTP-MIDNIGHT**: request now, response after the batch window, because immediacy is a lifestyle choice.
- **CORBA CATHEDRAL**: generate enough IDL to make `ADD` require organizational governance.
- **SOAP APOCALYPSE**: wrap a one-digit answer in progressively more XML until the answer develops namespaces.
- **TOKEN TRIBUNAL**: compare useful semantic content with wire-format ceremony.
- **API TIME MACHINE**: solve the same task using each historical interface and graph the abstraction tax.
- **NO-API MODE**: write the answer to a file and physically instruct the user to carry it to the other computer.
- **KEY LOST AGAIN**: benchmark mean time between provisioning an API key and forgetting where it went.

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

No runtime dependencies are required.

## Important lack of seriousness

HERESY-API is software art and technical satire. The payload comparisons are intentionally theatrical and are **not** claims that older mechanisms are generally superior, safer, faster, cheaper, or more maintainable than modern APIs.

Use modern interfaces where they solve modern problems.

Then, occasionally, ask why your integer needed a JSON entourage.

## License

Apache-2.0. See `LICENSE`.
