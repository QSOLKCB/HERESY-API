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

For the canonical exhibit:

```text
canonical useful intent = b"ADD 2 2"
ceremony ratio = transmitted payload bytes / 7
```

The metric is intentionally local to the artwork. It does not model latency, reliability, discoverability, compatibility, security, tooling, maintenance, versioning, observability, developer experience, or total system cost.

Those omissions are not bugs in the joke. They are why the joke is not a benchmark.

## 5. Token estimates

Until a specific tokenizer is intentionally integrated, HERESY-API uses:

```text
estimated tokens = ceil(UTF-8 payload bytes / 4)
```

Every surface displaying this value must identify it as crude or approximate.

Do not present it as the output of GPT, Claude, Gemini, Llama, or any other tokenizer.

## 6. The invariant

Every future exhibit should preserve this contrast:

**tiny intent -> historically or culturally recognizable interface -> visible ceremony -> technically literate punchline**

If an exhibit needs a page of explanation before the joke lands, the abstraction has won.
