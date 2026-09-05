# Curatorial Constitution

HERESY-API is technical satire. This document keeps the satire sharp enough to cut abstraction while preventing it from accidentally becoming fake engineering advice.

## 1. The recurring joke

Take a very small semantic intent and express it through several generations of software interface.

Then measure the visible ceremony.

The comedy comes from inversion: a historical interface that was objectively awkward in many ways can still make a modern interface look extravagantly dressed for a tiny job.

## 2. Punch upward at ceremony, not at useful engineering

Good targets:

- duplicated envelopes;
- metadata whose value is unclear for the demonstrated task;
- schema verbosity disproportionate to the payload;
- machine-to-machine formats optimized for human reassurance;
- abstraction layers that hide costs while adding more syntax;
- token-heavy agent/tool exchanges;
- interface designs where the request spends more bytes describing itself than doing its job.

Bad targets:

- accessibility;
- security metadata that is genuinely required;
- correctness constraints demonstrated to prevent real failures;
- interoperability requirements that the exhibit quietly depends on;
- pretending a tiny toy packet represents the operational requirements of a production distributed system.

## 3. Historical mechanisms are punchlines, not recommendations

Punch cards, tape, raw sockets, FTP batches, RPC systems, CORBA, DCOM, RMI, SOAP, and similar technologies solved problems under different constraints.

An exhibit may exaggerate their virtues for comic effect, but documentation must not quietly convert the exaggeration into a factual performance claim.

The museum's basic move is:

> "Look how little syntax this terrible old thing needed for this deliberately tiny task."

It is not:

> "Therefore build your payment system on magnetic tape."

The latter requires a different repository and considerably more insurance.

## 4. Ceremony Ratio

For any Time Machine request:

```text
useful intent bytes = len(ASCII semantic intent)
ceremony ratio = application payload bytes / useful intent bytes
```

The canonical exhibit remains:

```text
useful intent = b"ADD 2 2"
useful intent bytes = 7
```

Custom operands change the useful-intent byte count, so the denominator follows the actual semantic request rather than pretending every journey is seven bytes.

The metric is intentionally local to the artwork. It does not model latency, reliability, discoverability, compatibility, security, tooling, maintenance, versioning, observability, developer experience, or total system cost.

Those omissions are not bugs in the joke. They are why the joke is not a benchmark.

## 5. Token estimates

Until a specific tokenizer is intentionally integrated, HERESY-API uses:

```text
estimated tokens = ceil(application payload bytes / 4)
```

Every surface displaying this value must identify it as crude or approximate.

Do not present it as the output of GPT, Claude, Gemini, Llama, or any other tokenizer.

## 6. Time Machine invariants

Every exhibit in one journey must bind to the same semantic intent.

Every exhibit must expose:

- useful semantic intent;
- application payload bytes;
- approximate token count;
- Ceremony Ratio;
- protocol-specific punchline;
- what the ceremony is buying;
- an engineering caveat.

If an exhibit is illustrative rather than byte-accurate to a named historical wire protocol, it must say so.

Build-time artifacts must not be quietly counted as per-request wire bytes. In particular, CORBA IDL may be mocked as bureaucracy, but the museum must state that IDL is normally a build-time contract.

Modern authenticated exhibits may joke about lost keys only with obviously synthetic placeholders. Never put a real credential in the museum.

## 7. The invariant

Every future exhibit should preserve this contrast:

**tiny intent -> historically or culturally recognizable interface -> visible ceremony -> technically literate punchline**

If an exhibit needs a page of explanation before the joke lands, the abstraction has won.
