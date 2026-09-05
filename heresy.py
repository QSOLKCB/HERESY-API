#!/usr/bin/env python3
"""HERESY-API protocol museum.

A dependency-free software-art program that expresses the same tiny intent through
multiple interface styles and measures the amount of application-level wire-format
ceremony involved.

This is satire, not a protocol benchmark.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from math import ceil
from typing import Iterable

CANONICAL_INTENT = b"ADD 2 2"

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


@dataclass(frozen=True)
class Exhibit:
    name: str
    era: str
    payload: bytes
    punchline: str

    @property
    def payload_bytes(self) -> int:
        return len(self.payload)

    @property
    def estimated_tokens(self) -> int:
        # Deliberately crude. This is a satire meter, not a tokenizer.
        return ceil(self.payload_bytes / 4)

    @property
    def ceremony_ratio(self) -> float:
        return self.payload_bytes / len(CANONICAL_INTENT)


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def build_exhibits() -> tuple[Exhibit, ...]:
    """Return deterministic museum exhibits for the canonical ADD request.

    Payload sizes are application-level exhibit payloads. They intentionally do not
    include IP, TCP, UDP, Ethernet, TLS, filesystem, or physical-media overhead.
    """

    punch_card = f"{'ADD':<8}{2:>8}{2:>8}".ljust(80).encode("ascii")
    magnetic_tape = b"ADD|00000002|00000002\n"
    raw_socket = b"\x01\x00\x00\x00\x02\x00\x00\x00\x02"
    ftp_batch = b"HDR|JOB=0042|COUNT=1\nADD|2|2\nEOF|1\n"
    rpc_ish = b"ArithmeticService.Add(i32:2,i32:2)"

    soap_ish = (
        b'<?xml version="1.0"?>'
        b'<soap:Envelope xmlns:soap="urn:soap">'
        b'<soap:Body><Add xmlns="urn:heresy:arithmetic">'
        b'<a>2</a><b>2</b></Add></soap:Body></soap:Envelope>'
    )

    rest_body = _json_bytes({"operation": "add", "arguments": {"a": 2, "b": 2}})
    rest_json = (
        b"POST /v1/arithmetic/add HTTP/1.1\r\n"
        b"Host: example.invalid\r\n"
        b"Content-Type: application/json\r\n"
        b"Accept: application/json\r\n"
        b"X-Request-ID: 0042\r\n"
        + f"Content-Length: {len(rest_body)}\r\n\r\n".encode("ascii")
        + rest_body
    )

    graphql_ish = _json_bytes(
        {
            "query": "mutation Add($a:Int!,$b:Int!){add(a:$a,b:$b)}",
            "variables": {"a": 2, "b": 2},
        }
    )

    agent_tool_call = _json_bytes(
        {
            "tool": {
                "name": "add_two_integers",
                "description": "Add exactly two signed integers and return their arithmetic sum.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer", "description": "First integer operand."},
                        "b": {"type": "integer", "description": "Second integer operand."},
                    },
                    "required": ["a", "b"],
                    "additionalProperties": False,
                },
            },
            "arguments": {"a": 2, "b": 2},
        }
    )

    return (
        Exhibit(
            "Punch Card",
            "1940s-1960s",
            punch_card,
            "80 columns because storage used to arrive with furniture.",
        ),
        Exhibit(
            "Magnetic Tape",
            "1950s-1980s",
            magnetic_tape,
            "Sequential access. Please rewind your microservice.",
        ),
        Exhibit(
            "Raw Socket",
            "1970s-1980s",
            raw_socket,
            "Nine bytes. The schema is a rumour passed between senior engineers.",
        ),
        Exhibit(
            "FTP Batch",
            "1970s-1990s",
            ftp_batch,
            "Real-time, if tomorrow morning counts as a latency target.",
        ),
        Exhibit(
            "RPC-ish",
            "1980s-1990s",
            rpc_ish,
            "The network is a local function call until packet loss files an objection.",
        ),
        Exhibit(
            "SOAP-ish",
            "1990s-2000s",
            soap_ish,
            "The integer has entered the XML cathedral and acquired a namespace.",
        ),
        Exhibit(
            "REST-ish JSON",
            "modern web",
            rest_json,
            "Human-readable bureaucracy. Authentication pending: Dave has lost the API key again.",
        ),
        Exhibit(
            "GraphQL-ish",
            "modern web",
            graphql_ish,
            "Ask precisely for what you need after introducing yourself to the syntax tree.",
        ),
        Exhibit(
            "Agent Tool Call",
            "current AI stack",
            agent_tool_call,
            "Seven useful bytes escorted by a schema and several responsible adults.",
        ),
    )


def serialize(exhibits: Iterable[Exhibit]) -> list[dict[str, object]]:
    """Return JSON-safe exhibit metrics without pretending bytes are Unicode text."""

    rows: list[dict[str, object]] = []
    for exhibit in exhibits:
        row = asdict(exhibit)
        row.pop("payload")
        row.update(
            {
                "payload_bytes": exhibit.payload_bytes,
                "estimated_tokens": exhibit.estimated_tokens,
                "ceremony_ratio": round(exhibit.ceremony_ratio, 3),
                "payload_hex": exhibit.payload.hex(),
            }
        )
        rows.append(row)
    return rows


def render_table(exhibits: Iterable[Exhibit]) -> str:
    rows = list(exhibits)
    headings = ("EXHIBIT", "ERA / STYLE", "BYTES", "~TOKENS", "CEREMONY")
    table_rows = [
        (
            exhibit.name,
            exhibit.era,
            str(exhibit.payload_bytes),
            str(exhibit.estimated_tokens),
            f"{exhibit.ceremony_ratio:.2f}x",
        )
        for exhibit in rows
    ]

    widths = [
        max([len(headings[index]), *(len(row[index]) for row in table_rows)])
        for index in range(len(headings))
    ]

    def format_row(row: tuple[str, ...]) -> str:
        return "  ".join(value.ljust(widths[index]) for index, value in enumerate(row))

    separator = "  ".join("-" * width for width in widths)
    output = [
        "HERESY-API :: PROTOCOL MUSEUM",
        f"Canonical useful intent: {CANONICAL_INTENT.decode('ascii')!r} ({len(CANONICAL_INTENT)} bytes)",
        "Token estimate: ceil(payload bytes / 4), intentionally crude",
        "Payload accounting: application-level exhibit bytes only",
        "",
        format_row(headings),
        separator,
    ]
    output.extend(format_row(row) for row in table_rows)
    output.append("")
    output.append("CURATORIAL NOTES")
    for exhibit in rows:
        output.append(f"- {exhibit.name}: {exhibit.punchline}")
    output.append("")
    output.append("THE OLD-SCHOOL DEFENSE")
    for name, defense in TRANSPORT_DEFENSE:
        output.append(f"- {name}: {defense}")
    output.append("")
    output.append("MODERN AUTHENTICATION CEREMONY")
    output.append("1. Put API key in .env")
    output.append("2. Forget which .env")
    output.append("3. Search .env, .env.local, .env.old, .env.backup, and notes-final-FINAL.txt")
    output.append("4. Find key in shell history")
    output.append("5. Rotate key because finding it in shell history is bad")
    output.append("6. Update three services except the one that matters")
    output.append("7. Receive HTTP 401")
    output.append("8. Consider magnetic tape")
    output.append("")
    output.append("Verdict: civilization has many virtues. Payload minimalism is not always one of them.")
    return "\n".join(output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Tour the HERESY-API protocol museum.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable metadata about our joke about machine-readable metadata.",
    )
    args = parser.parse_args()

    exhibits = build_exhibits()
    if args.json:
        print(json.dumps(serialize(exhibits), indent=2, sort_keys=True))
    else:
        print(render_table(exhibits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
