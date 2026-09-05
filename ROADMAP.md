# HERESY-API Roadmap

The museum expands in deliberately sequenced acts of software heresy.

## PR #1 — PROTOCOL MUSEUM

**Status:** implemented and merged.

Established the dependency-free museum, canonical `ADD 2 2` experiment, Ceremony Ratio, approximate token satire meter, curatorial constitution, historical/modern exhibits, API-key running gag, tests, and lean CI.

## PR #2 — API TIME MACHINE

**Status:** implemented by PR #2.

Turn the protocol museum into a dynamic historical comparison engine for the same tiny semantic intent.

### Delivered contract

- custom signed-32-bit operands while retaining canonical `ADD 2 2`
- chronological punch-card through contemporary-agent timeline
- punch-card / fixed-width representation
- magnetic-tape / sequential record representation
- raw TCP-style binary framing
- UDP-style datagram framing
- FTP / batch-file exchange
- RPC-ish invocation
- CORBA / IDL bureaucracy theatre
- SOAP-ish XML escalation
- REST-ish HTTP + JSON
- GraphQL-ish HTTP request envelope
- contemporary agent/tool-call schema ceremony
- filtering by stable style slug
- compact timeline view
- detailed curatorial dossier view
- deterministic JSON output

Every exhibit reports:

- useful semantic intent
- useful bytes
- application payload bytes
- ceremony bytes relative to useful intent
- deliberately crude approximate token count
- Ceremony Ratio
- protocol-specific punchline
- what the extra ceremony buys
- honest engineering caveat
- authentication status where applicable

### Running gag

Modern authenticated modes retain the API-key lifecycle:

```text
provision -> store safely -> forget where -> search .env variants -> find somewhere unsafe -> rotate -> 401 -> consider magnetic tape
```

## PR #3 — HERESY API CALCULATOR

**Status:** next.

Build an offline-first HTML/CSS/JavaScript joke calculator and publish the same static app through GitHub Pages.

### Hard requirements

- plain HTML, CSS, and JavaScript
- no runtime framework
- no backend
- no external API dependency
- no API key required, because Dave would lose it
- works when opened directly from local disk
- works when served through GitHub Pages
- deterministic calculations
- responsive desktop/mobile layout

### Joke interaction

The user enters a tiny arithmetic operation, for example `2 + 2`, then selects an unnecessarily elaborate interface style.

The calculator shows:

1. the actual mathematical answer
2. the useful semantic request
3. the fake wire representation for the chosen era/style
4. payload bytes
5. approximate token ceremony
6. Ceremony Ratio
7. an era-specific punchline
8. a modern-authentication failure gag where appropriate

Example outcome:

```text
Mathematics: 4
Useful intent: ADD 2 2
Useful bytes: 7
Enterprise ceremony: 487
API key status: FOUND IN .env.old.backup.final2
Authentication status: 401
Recommended remediation: rewind tape
```

### GitHub Pages

The Pages deployment should publish exactly the static offline-capable application. GitHub Pages is a distribution surface, not a runtime dependency.

If the internet disappears after loading the repository, the calculator should still be able to insult APIs locally.

## Later gallery wings

- **PUNCHCARD/1.0**: visual 80-column card rendering
- **TAPE/1.0**: append-only virtual tape and rewind theatre
- **FTP-MIDNIGHT**: asynchronous overnight batch mode
- **CORBA CATHEDRAL**: generate spectacularly disproportionate IDL
- **SOAP APOCALYPSE**: progressively namespace a one-digit answer
- **TOKEN TRIBUNAL**: put useful semantics and ceremony on trial
- **NO-API MODE**: write the result to a file and instruct the user to carry it to another computer
- **KEY LOST AGAIN**: measure mean time between API-key provisioning and forgetting where it went
