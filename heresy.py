#!/usr/bin/env python3
"""HERESY-API API Time Machine.

A dependency-free software-art program that sends one tiny arithmetic intent
through historical and modern interface styles and measures the amount of
application-level ceremony accumulated along the way.

This is satire, not a protocol benchmark.
"""

from __future__ import annotations

import argparse
import json
import struct
from dataclasses import asdict, dataclass
from math import ceil
from typing import Iterable, Sequence

INT32_MIN = -(2**31)
INT32_MAX = 2**31 - 1
DEFAULT_LEFT = 2
DEFAULT_RIGHT = 2

TRANSPORT_DEFENSE = (
    (
        "TCP",
        "Ordered, reliable byte stream; lets a tiny custom protocol stay tiny once you "
        "define its framing. Long-lived connections can avoid rebuilding application "
        "ceremony for every request. Price: you own the protocol above the stream.",
    ),
    (
        "UDP",
        "Datagram boundaries, no transport-level connection handshake, and very little "
        "application ceremony. Excellent when timeliness matters more than retransmitting "
        "stale data. Price: reliability, ordering, authentication, and congestion behavior "
        "do not magically appear because the packet was small.",
    ),
    (
        "FTP / batch files",
        "For the extremely unglamorous job 'move this file over there', a file-transfer "
        "workflow can be wonderfully literal, scriptable, resumable, inspectable, and easy "
        "to replay. Price: plain FTP is not encrypted, and batch latency is still batch latency.",
    ),
)

API_KEY_LIFECYCLE = (
    "provision",
    "store safely",
    "forget where",
    "search .env variants",
    "find somewhere unsafe",
    "rotate",
    "401",
    "consider magnetic tape",
)


@dataclass(frozen=True)
class Intent:
    """One microscopic arithmetic request constrained to actual signed int32 values."""

    left: int = DEFAULT_LEFT
    right: int = DEFAULT_RIGHT

    def __post_init__(self) -> None:
        for name, value in (("left", self.left), ("right", self.right)):
            # bool is an int subclass in Python, but it is not part of this wire contract.
            # Requiring the exact built-in int type keeps text, JSON and binary exhibits aligned.
            if type(value) is not int:
                raise TypeError(
                    f"{name} must be an int, not {type(value).__name__}"
                )
            if not INT32_MIN <= value <= INT32_MAX:
                raise ValueError(
                    f"{name} must fit a signed 32-bit integer "
                    f"({INT32_MIN}..{INT32_MAX}); got {value}"
                )

    @property
    def text(self) -> str:
        return f"ADD {self.left} {self.right}"

    @property
    def payload(self) -> bytes:
        return self.text.encode("ascii")

    @property
    def result(self) -> int:
        return self.left + self.right


CANONICAL_INTENT = Intent().payload


@dataclass(frozen=True)
class Exhibit:
    """One stop on the API Time Machine."""

    slug: str
    name: str
    era: str
    intent: str
    payload: bytes
    punchline: str
    value_purchased: str
    caveat: str
    authenticated: bool = False
    auth_status: str = "not applicable"

    @property
    def payload_bytes(self) -> int:
        return len(self.payload)

    @property
    def estimated_tokens(self) -> int:
        # Deliberately crude. This is a satire meter, not a tokenizer.
        return ceil(self.payload_bytes / 4)

    @property
    def useful_bytes(self) -> int:
        return len(self.intent.encode("ascii"))

    @property
    def ceremony_ratio(self) -> float:
        return self.payload_bytes / self.useful_bytes

    @property
    def ceremony_bytes(self) -> int:
        return self.payload_bytes - self.useful_bytes


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _http_request(path: str, body: bytes, *, content_type: str) -> bytes:
    """Build a deterministic HTTP/1.1 exhibit request with a synthetic lost key."""

    return (
        f"POST {path} HTTP/1.1\r\n".encode("ascii")
        + b"Host: example.invalid\r\n"
        + f"Content-Type: {content_type}\r\n".encode("ascii")
        + b"Accept: application/json\r\n"
        + b"X-Request-ID: 0042\r\n"
        + b"X-API-Key: LOST-IN-.env.old.backup.final2\r\n"
        + f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
        + body
    )


def _fixed_record(intent: Intent) -> bytes:
    return f"{'ADD':<8}{intent.left:>11}{intent.right:>11}".ljust(80).encode("ascii")


def _binary_operands(intent: Intent) -> bytes:
    return struct.pack("!Bii", 0x01, intent.left, intent.right)


def build_exhibits(intent: Intent | None = None) -> tuple[Exhibit, ...]:
    """Build the chronological API Time Machine for one semantic intent."""

    intent = intent or Intent()
    text = intent.text
    wire_intent = _binary_operands(intent)

    punch_card = _fixed_record(intent)
    magnetic_tape = f"ADD|{intent.left:+011d}|{intent.right:+011d}\n".encode("ascii")
    tcp_frame = struct.pack("!H", len(wire_intent)) + wire_intent
    udp_datagram = wire_intent
    ftp_batch = (
        f"HDR|JOB=0042|COUNT=1\n{text}\nEOF|COUNT=1|CHECK=HUMAN-EYEBALL\n"
    ).encode("ascii")
    rpc_ish = f"ArithmeticService.Add(i32:{intent.left},i32:{intent.right})".encode("ascii")
    corba_ish = (
        "GIOP-ISH|IDL:heresy/Arithmetic:1.0|"
        f"operation=add|a={intent.left}|b={intent.right}|request_id=0042"
    ).encode("ascii")
    soap_ish = (
        '<?xml version="1.0"?>'
        '<soap:Envelope xmlns:soap="urn:soap">'
        '<soap:Header><RequestId>0042</RequestId></soap:Header>'
        '<soap:Body><Add xmlns="urn:heresy:arithmetic">'
        f"<a>{intent.left}</a><b>{intent.right}</b>"
        "</Add></soap:Body></soap:Envelope>"
    ).encode("ascii")

    rest_body = _json_bytes(
        {"operation": "add", "arguments": {"a": intent.left, "b": intent.right}}
    )
    rest_json = _http_request(
        "/v1/arithmetic/add", rest_body, content_type="application/json"
    )

    graphql_body = _json_bytes(
        {
            "query": "mutation Add($a:Int!,$b:Int!){add(a:$a,b:$b)}",
            "variables": {"a": intent.left, "b": intent.right},
        }
    )
    graphql_ish = _http_request(
        "/graphql", graphql_body, content_type="application/json"
    )

    agent_tool_call = _json_bytes(
        {
            "authentication": {
                "scheme": "api_key",
                "status": "lost_again",
                "last_known_location": ".env.old.backup.final2",
            },
            "tool": {
                "name": "add_two_integers",
                "description": "Add exactly two signed integers and return their arithmetic sum.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "integer",
                            "minimum": INT32_MIN,
                            "maximum": INT32_MAX,
                            "description": "First signed 32-bit integer operand.",
                        },
                        "b": {
                            "type": "integer",
                            "minimum": INT32_MIN,
                            "maximum": INT32_MAX,
                            "description": "Second signed 32-bit integer operand.",
                        },
                    },
                    "required": ["a", "b"],
                    "additionalProperties": False,
                },
            },
            "arguments": {"a": intent.left, "b": intent.right},
        }
    )

    modern_auth = (
        "401: API key last seen in .env.old.backup.final2; "
        "Dave rotated it and updated every service except this one"
    )

    return (
        Exhibit(
            "punch-card",
            "Punch Card / Fixed Width",
            "1940s-1960s",
            text,
            punch_card,
            "80 columns because storage used to arrive with furniture.",
            "A rigid physical record layout that operators and programs can agree on.",
            "Fixed width wastes space and is brittle when the record shape changes.",
        ),
        Exhibit(
            "magnetic-tape",
            "Magnetic Tape Record",
            "1950s-1980s",
            text,
            magnetic_tape,
            "Sequential access. Please rewind your microservice.",
            "Simple durable sequential records that are easy to append and batch.",
            "Random access and low-latency request/response are not the tape's hobbies.",
        ),
        Exhibit(
            "raw-tcp",
            "Raw TCP-style Frame",
            "1970s-1980s",
            text,
            tcp_frame,
            "Eleven application bytes. Documentation: two-byte length, opcode, two int32s.",
            "Reliable ordered delivery plus explicit application message framing.",
            "TCP is a byte stream, not an API design. Versioning, auth, schema evolution, "
            "timeouts, and observability remain yours.",
        ),
        Exhibit(
            "udp",
            "UDP-style Datagram",
            "1970s-1980s",
            text,
            udp_datagram,
            "The packet can simply leave. No architecture review calendar invite required.",
            "Message boundaries and tiny application framing for freshness-first workloads.",
            "Delivery, ordering, retransmission, authentication, and congestion semantics "
            "may need to be supplied elsewhere.",
        ),
        Exhibit(
            "ftp-batch",
            "FTP / Batch File",
            "1970s-1990s",
            text,
            ftp_batch,
            "Real-time, if tomorrow morning counts as a latency target.",
            "Inspectable, archivable, replayable, checksum-friendly asynchronous exchange.",
            "Plain FTP is unencrypted; secure deployments need a protected alternative. "
            "Batch is also the wrong tool when latency actually matters.",
        ),
        Exhibit(
            "rpc",
            "RPC-ish Invocation",
            "1980s-1990s",
            text,
            rpc_ish,
            "The network is a local function call until packet loss files an objection.",
            "Typed operation names and generated client/server calling conventions.",
            "Remote calls still fail in remote ways; pretending otherwise creates exciting outages.",
        ),
        Exhibit(
            "corba",
            "CORBA / IDL Theatre",
            "1990s",
            text,
            corba_ish,
            "The addition has been referred to the Object Request Broker.",
            "Language-neutral interface contracts and distributed-object interoperability.",
            "This is deliberately GIOP-ish theatre, not a byte-accurate CORBA capture. "
            "IDL is normally a build-time contract, not resent on every invocation.",
        ),
        Exhibit(
            "soap",
            "SOAP-ish XML",
            "late 1990s-2000s",
            text,
            soap_ish,
            "The integer has entered the XML cathedral and acquired a namespace.",
            "Explicit envelopes, extensible headers, typed contracts, and enterprise tooling.",
            "The illustrative envelope omits the wider WS-* universe, where additional ceremony "
            "can also purchase security, reliability, and governance.",
        ),
        Exhibit(
            "rest",
            "REST-ish HTTP + JSON",
            "modern web",
            text,
            rest_json,
            "Human-readable bureaucracy. Authentication pending: Dave lost the API key again.",
            "Ubiquitous HTTP tooling, intermediaries, debuggability, caches, and loose coupling.",
            "HTTP and JSON overhead can be disproportionate for tiny machine-to-machine messages.",
            True,
            modern_auth,
        ),
        Exhibit(
            "graphql",
            "GraphQL-ish HTTP",
            "modern web",
            text,
            graphql_ish,
            "Ask precisely for what you need after introducing yourself to the syntax tree.",
            "Client-selected response shape, schema introspection, and aggregation behind one endpoint.",
            "Query flexibility shifts complexity into schema design, resolvers, authorization, "
            "cost controls, and caching.",
            True,
            modern_auth,
        ),
        Exhibit(
            "agent-tool",
            "Agent Tool Call",
            "current AI stack",
            text,
            agent_tool_call,
            "Tiny arithmetic escorted by a schema, descriptions, arguments, and several responsible adults.",
            "Machine-readable affordances that let a model choose and call tools with validation.",
            "Tool schemas can consume substantial context repeatedly; cache/reuse and compact contracts "
            "matter when scale turns prose into a bill.",
            True,
            modern_auth,
        ),
    )


def select_exhibits(
    exhibits: Sequence[Exhibit], styles: Sequence[str] | None
) -> tuple[Exhibit, ...]:
    """Select requested style slugs while preserving chronological order.

    ``all`` is a sentinel, not a wildcard that suppresses validation: it must be
    used alone so a typo in another repeated ``--style`` argument cannot disappear.
    """

    if not styles:
        return tuple(exhibits)

    requested = set(styles)
    known = {exhibit.slug for exhibit in exhibits}
    unknown = sorted(requested - known - {"all"})
    if unknown:
        raise ValueError(
            "unknown style(s): "
            + ", ".join(unknown)
            + "; choose from: "
            + ", ".join(sorted(known))
        )
    if "all" in requested:
        if requested != {"all"}:
            raise ValueError("style 'all' must be used alone")
        return tuple(exhibits)

    return tuple(exhibit for exhibit in exhibits if exhibit.slug in requested)


def _display_payload(payload: bytes) -> str:
    """Prefer readable text, but never pretend arbitrary binary is Unicode."""

    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError:
        return "hex:" + payload.hex()

    if all(char == "\n" or char == "\r" or 32 <= ord(char) <= 126 for char in text):
        return text
    return "hex:" + payload.hex()


def serialize(
    exhibits: Iterable[Exhibit], *, result: int | None = None
) -> list[dict[str, object]]:
    """Return JSON-safe exhibit metrics."""

    rows: list[dict[str, object]] = []
    for position, exhibit in enumerate(exhibits, start=1):
        row = asdict(exhibit)
        row.pop("payload")
        row.update(
            {
                "position": position,
                "result": result,
                "useful_bytes": exhibit.useful_bytes,
                "payload_bytes": exhibit.payload_bytes,
                "ceremony_bytes": exhibit.ceremony_bytes,
                "estimated_tokens": exhibit.estimated_tokens,
                "ceremony_ratio": round(exhibit.ceremony_ratio, 3),
                "payload_hex": exhibit.payload.hex(),
                "payload_display": _display_payload(exhibit.payload),
            }
        )
        rows.append(row)
    return rows


def render_table(exhibits: Iterable[Exhibit]) -> str:
    """Render the compact chronological Time Machine table."""

    rows = list(exhibits)
    headings = ("#", "EXHIBIT", "ERA / STYLE", "INTENT", "BYTES", "~TOKENS", "CEREMONY")
    table_rows = [
        (
            str(index),
            exhibit.name,
            exhibit.era,
            exhibit.intent,
            str(exhibit.payload_bytes),
            str(exhibit.estimated_tokens),
            f"{exhibit.ceremony_ratio:.2f}x",
        )
        for index, exhibit in enumerate(rows, start=1)
    ]

    widths = [
        max([len(headings[index]), *(len(row[index]) for row in table_rows)])
        for index in range(len(headings))
    ]

    def format_row(row: tuple[str, ...]) -> str:
        return "  ".join(value.ljust(widths[index]) for index, value in enumerate(row))

    separator = "  ".join("-" * width for width in widths)
    intent_text = rows[0].intent if rows else Intent().text
    useful_bytes = len(intent_text.encode("ascii"))

    output = [
        "HERESY-API :: API TIME MACHINE",
        f"Useful semantic intent: {intent_text!r} ({useful_bytes} bytes)",
        "Token estimate: ceil(payload bytes / 4), intentionally crude",
        "Payload accounting: application-level exhibit bytes only",
        "",
        format_row(headings),
        separator,
    ]
    output.extend(format_row(row) for row in table_rows)
    output.append("")
    output.append(
        "Verdict: every abstraction may enter, but every extra byte must explain what it bought."
    )
    return "\n".join(output)


def render_details(exhibits: Iterable[Exhibit], *, result: int) -> str:
    """Render the full curatorial dossier for selected Time Machine stops."""

    rows = list(exhibits)
    output = [
        "HERESY-API :: API TIME MACHINE :: CURATORIAL DOSSIER",
        f"Mathematics: {result}",
        "",
    ]

    for position, exhibit in enumerate(rows, start=1):
        output.extend(
            [
                f"[{position:02d}] {exhibit.name} :: {exhibit.era}",
                f"Slug: {exhibit.slug}",
                f"Useful semantic intent: {exhibit.intent}",
                f"Useful bytes: {exhibit.useful_bytes}",
                f"Application payload bytes: {exhibit.payload_bytes}",
                f"Ceremony bytes vs useful intent: {exhibit.ceremony_bytes:+d}",
                f"Approximate tokens: {exhibit.estimated_tokens}",
                f"Ceremony Ratio: {exhibit.ceremony_ratio:.2f}x",
                f"Payload: {_display_payload(exhibit.payload)}",
                f"Punchline: {exhibit.punchline}",
                f"What the ceremony buys: {exhibit.value_purchased}",
                f"Engineering caveat: {exhibit.caveat}",
                f"Authentication: {exhibit.auth_status}",
                "",
            ]
        )

    output.append("MODERN API KEY LIFECYCLE")
    output.append(" -> ".join(API_KEY_LIFECYCLE))
    output.append("")
    output.append("Recommended remediation after 401: rewind tape.")
    return "\n".join(output)


def render_transport_defense() -> str:
    output = ["THE OLD-SCHOOL DEFENSE"]
    for name, defense in TRANSPORT_DEFENSE:
        output.append(f"- {name}: {defense}")
    return "\n".join(output)


def _style_help(exhibits: Sequence[Exhibit]) -> str:
    return "\n".join(f"{exhibit.slug:14} {exhibit.name}" for exhibit in exhibits)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Send one tiny ADD request through the HERESY-API Time Machine."
    )
    parser.add_argument("--left", type=int, default=DEFAULT_LEFT, help="left signed int32 operand")
    parser.add_argument("--right", type=int, default=DEFAULT_RIGHT, help="right signed int32 operand")
    parser.add_argument(
        "--style",
        action="append",
        default=[],
        metavar="SLUG",
        help="show one style; repeat for several; omit for all",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="show payload, punchline, value purchased, caveat, and auth status",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable metadata about our joke about machine-readable metadata",
    )
    parser.add_argument(
        "--list-styles",
        action="store_true",
        help="list chronological style slugs and exit",
    )
    parser.add_argument(
        "--old-school-defense",
        action="store_true",
        help="print the technically annoying case for TCP, UDP, and batch files",
    )
    args = parser.parse_args(argv)

    try:
        intent = Intent(args.left, args.right)
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))

    exhibits = build_exhibits(intent)

    if args.list_styles:
        print(_style_help(exhibits))
        return 0

    if args.old_school_defense:
        print(render_transport_defense())
        return 0

    try:
        selected = select_exhibits(exhibits, args.style)
    except ValueError as exc:
        parser.error(str(exc))

    if args.json:
        document = {
            "time_machine": "HERESY-API",
            "intent": intent.text,
            "result": intent.result,
            "api_key_lifecycle": list(API_KEY_LIFECYCLE),
            "measurement_caveat": (
                "application-level exhibit bytes only; token estimate is ceil(bytes / 4)"
            ),
            "exhibits": serialize(selected, result=intent.result),
        }
        print(json.dumps(document, indent=2, sort_keys=True))
    elif args.details:
        print(render_details(selected, result=intent.result))
    else:
        print(render_table(selected))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())