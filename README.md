# HERESY-API

> **A software-art joke about APIs, abstraction, ceremony, and the heroic number of tokens sometimes required to say almost nothing.**

HERESY-API asks a deeply irresponsible question:

**What if modern API ceremony had to justify itself in a museum beside punch cards, magnetic tape, raw TCP frames, UDP datagrams, batch files, CORBA, SOAP, JSON, GraphQL, and agent tool schemas?**

The answer is the **API Time Machine**.

## API Time Machine

The default experiment remains magnificently difficult:

```text
ADD 2 2
```

Run the full timeline:

```bash
python3 heresy.py
```

Every stop receives the same useful semantic intent and reports:

- useful semantic intent
- application payload bytes
- deliberately crude approximate token count
- Ceremony Ratio
- protocol-specific punchline
- what the additional ceremony actually buys
- an honest engineering caveat
- authentication status where Dave has been entrusted with an API key

Example custom journey:

```bash
python3 heresy.py --left 17 --right -3 --details
```

Jump directly to one or more eras:

```bash
python3 heresy.py --style udp --details
python3 heresy.py --style punch-card --style soap --style agent-tool
```

Discover the available style slugs:

```bash
python3 heresy.py --list-styles
```

Produce machine-readable metadata about our joke about machine-readable metadata:

```bash
python3 heresy.py --left 10 --right -7 --style graphql --json
```

The operands are intentionally restricted to signed 32-bit integers so the binary TCP/UDP exhibits remain deterministic and structurally comparable.

## Current timeline

| Stop | Era / style | Curatorial interpretation |
| --- | --- | --- |
| Punch Card / Fixed Width | 1940s-1960s | 80 columns because storage used to arrive with furniture. |
| Magnetic Tape Record | 1950s-1980s | Sequential access. Please rewind your microservice. |
| Raw TCP-style Frame | 1970s-1980s | Length prefix, opcode, two int32s. The documentation has become frighteningly short. |
| UDP-style Datagram | 1970s-1980s | The packet can simply leave. No architecture review calendar invite required. |
| FTP / Batch File | 1970s-1990s | Real-time, if tomorrow morning counts as a latency target. |
| RPC-ish Invocation | 1980s-1990s | The network is local until packet loss files an objection. |
| CORBA / IDL Theatre | 1990s | The addition has been referred to the Object Request Broker. |
| SOAP-ish XML | late 1990s-2000s | The integer has entered the XML cathedral and acquired a namespace. |
| REST-ish HTTP + JSON | modern web | Human-readable bureaucracy. Dave has lost the API key again. |
| GraphQL-ish HTTP | modern web | Ask precisely for what you need after introducing yourself to the syntax tree. |
| Agent Tool Call | current AI stack | Tiny arithmetic escorted by a schema and several responsible adults. |

## Ceremony Ratio

For any Time Machine request:

```text
Ceremony Ratio = application payload bytes / useful semantic intent bytes
```

For the canonical `ADD 2 2`, useful intent is seven ASCII bytes.

The approximate token meter remains deliberately crude:

```text
estimated tokens = ceil(application payload bytes / 4)
```

It is a joke-meter, not a tokenizer, benchmark, protocol-efficiency paper, or invoice predictor.

Network headers, TLS, Ethernet, filesystem overhead, physical-media overhead, server implementation cost, latency, reliability, maintenance, observability, governance, and all the other things capable of ruining a simple chart are intentionally outside this metric.

## The Heresies

1. **Every byte must explain why it exists.**
2. **JSON is not an emotional-support syntax.**
3. **A schema can prevent chaos and still become baroque. Both things can be true.**
4. **Tokens are a computational resource, not decorative confetti.**
5. **Human-readable does not automatically mean machine-efficient.**
6. **If `ADD 2 2` needs three abstraction layers, the punch-card operator gets one smug cigarette break.**
7. **An old mechanism can be unsuitable for modern production and still make a devastating comparison at a deliberately tiny scale.**
8. **An API key stored safely is apparently indistinguishable from an API key lost forever.**
9. **If an abstraction adds bytes, the Time Machine is allowed to ask what those bytes purchased.**

## Why the heretics occasionally have a point

### TCP

TCP gives an ordered, reliable byte stream. When both ends are controlled and the message set is tiny, a compact framed binary protocol can avoid repeatedly shipping field names, route names, content negotiation, and text envelopes.

**Heresy:** sometimes the protocol really can be `length + opcode + two int32s`.

**Reality check:** TCP gives a stream, not a complete distributed-system design. Framing, authentication, versioning, schema evolution, observability, timeouts, retries above the stream, and not setting production on fire remain your problem.

### UDP

UDP preserves datagram boundaries and avoids a transport-level connection handshake. That can suit workloads where newest-state freshness matters more than recovering stale data.

**Heresy:** the packet can simply leave.

**Reality check:** delivery, ordering, retransmission, authentication, congestion behavior, and application semantics may need to be provided elsewhere. Small is not synonymous with complete.

### FTP and batch files

For **MOVE THIS FILE OVER THERE**, a durable file can be wonderfully literal: inspectable, archivable, replayable, checksum-friendly, asynchronously processable, and easy to hand to another tool.

**Heresy:** yesterday's `results.dat` does not necessarily need twelve endpoints and an SDK.

**Reality check:** plain FTP is unencrypted. Secure deployments need an appropriate protected alternative, and batch exchange is a poor fit when low latency is actually required.

## CORBA honesty clause

The CORBA stop is deliberately **GIOP-ish theatre**, not a byte-accurate packet capture. IDL is normally a build-time interface contract and is not resent on every call.

That caveat is part of the joke's constitution: HERESY-API may exaggerate bureaucracy, but it does not get to falsify where the bureaucracy lives.

## Modern authentication ceremony

Modern authenticated stops retain the canonical lifecycle:

```text
provision
-> store safely
-> forget where
-> search .env variants
-> find somewhere unsafe
-> rotate
-> 401
-> consider magnetic tape
```

The synthetic key marker is:

```text
LOST-IN-.env.old.backup.final2
```

It is not a secret. It is a cry for help.

## Old-school defense mode

For the technically annoying version of the joke:

```bash
python3 heresy.py --old-school-defense
```

This prints the narrow cases for TCP, UDP, and batch files together with the bill each one leaves on the table.

## Project sequence

See [`ROADMAP.md`](ROADMAP.md).

- **PR #1 — Protocol Museum:** foundation, curatorial rules, metrics, and first exhibits.
- **PR #2 — API Time Machine:** dynamic operands, full historical timeline, filtering, detailed dossiers, engineering value/caveats, UDP, CORBA, and persistent API-key tragedy.
- **PR #3 — HERESY API CALCULATOR:** offline-first plain HTML/CSS/JavaScript calculator distributed through GitHub Pages, with no backend and therefore no API key for Dave to lose.

GitHub Pages will be the display case, not a runtime dependency.

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

No runtime dependencies are required.

## Important lack of seriousness

HERESY-API is software art and technical satire.

It does **not** claim that punch cards, tape, raw sockets, FTP, RPC, CORBA, SOAP, REST, GraphQL, or agent tooling are universally better or worse than one another. They solve different problems under different constraints.

The artwork simply reserves the right to ask why your integer needed a JSON entourage.

## License

Apache-2.0. See `LICENSE`.
