# HERESY-API Roadmap

The museum expands in deliberately sequenced acts of software heresy.

## PR #2 — API TIME MACHINE

Turn the protocol museum into an interactive historical comparison engine for the same tiny intent.

### Core idea

Start with a microscopic operation such as:

```text
ADD 2 2
```

Then send the same semantic intent through historical and modern interface styles so the user can watch the ceremony accumulate.

### Planned exhibits

- punch-card / fixed-width representation
- magnetic-tape / sequential record representation
- raw TCP-style binary framing
- UDP-style datagram framing
- FTP / batch-file exchange
- RPC-ish invocation
- CORBA / IDL bureaucracy theatre
- SOAP-ish XML escalation
- REST-ish HTTP + JSON
- GraphQL-ish request envelopes
- contemporary agent/tool-call schema ceremony

### Output

For every exhibit, show at least:

- useful semantic intent
- application payload bytes
- deliberately crude approximate token count
- Ceremony Ratio
- protocol-specific punchline
- honest engineering caveat

The point is not to prove that old protocols are universally better. The point is to make every abstraction explain what value its extra ceremony purchased.

### Running gag

Modern authenticated modes retain the API-key lifecycle:

```text
provision -> store safely -> forget where -> search .env variants -> find somewhere unsafe -> rotate -> 401 -> consider magnetic tape
```

## PR #3 — HERESY API CALCULATOR

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
