import contextlib
import io
import json
import unittest

import heresy


class HeresyTimeMachineTests(unittest.TestCase):
    def test_canonical_intent_is_stable(self) -> None:
        self.assertEqual(heresy.CANONICAL_INTENT, b"ADD 2 2")
        self.assertEqual(len(heresy.CANONICAL_INTENT), 7)

    def test_intent_is_dynamic_and_result_is_deterministic(self) -> None:
        intent = heresy.Intent(17, -3)
        self.assertEqual(intent.text, "ADD 17 -3")
        self.assertEqual(intent.payload, b"ADD 17 -3")
        self.assertEqual(intent.result, 14)

    def test_intent_rejects_values_outside_signed_int32(self) -> None:
        with self.assertRaises(ValueError):
            heresy.Intent(2**31, 0)
        with self.assertRaises(ValueError):
            heresy.Intent(0, -(2**31) - 1)

    def test_punch_card_fields_cover_full_signed_int32_range(self) -> None:
        for intent in (
            heresy.Intent(heresy.INT32_MAX, heresy.INT32_MAX),
            heresy.Intent(heresy.INT32_MIN, heresy.INT32_MIN),
        ):
            exhibit = next(
                item for item in heresy.build_exhibits(intent) if item.slug == "punch-card"
            )
            record = exhibit.payload.decode("ascii")
            self.assertEqual(len(record), 80)
            self.assertEqual(record[:8].strip(), "ADD")
            self.assertEqual(record[8:19].strip(), str(intent.left))
            self.assertEqual(record[19:30].strip(), str(intent.right))

    def test_time_machine_contains_every_roadmap_exhibit(self) -> None:
        slugs = [exhibit.slug for exhibit in heresy.build_exhibits()]
        self.assertEqual(
            slugs,
            [
                "punch-card",
                "magnetic-tape",
                "raw-tcp",
                "udp",
                "ftp-batch",
                "rpc",
                "corba",
                "soap",
                "rest",
                "graphql",
                "agent-tool",
            ],
        )

    def test_exhibits_are_deterministic_and_bind_the_same_intent(self) -> None:
        intent = heresy.Intent(9, 4)
        first = heresy.build_exhibits(intent)
        second = heresy.build_exhibits(intent)
        self.assertEqual(first, second)
        self.assertTrue(all(exhibit.intent == "ADD 9 4" for exhibit in first))
        self.assertTrue(all(exhibit.payload for exhibit in first))

    def test_udp_and_tcp_binary_frames_are_explicit(self) -> None:
        exhibits = {exhibit.slug: exhibit for exhibit in heresy.build_exhibits()}
        self.assertEqual(exhibits["udp"].payload_bytes, 9)
        self.assertEqual(exhibits["raw-tcp"].payload_bytes, 11)
        self.assertEqual(exhibits["raw-tcp"].payload[:2], b"\x00\x09")
        self.assertEqual(exhibits["raw-tcp"].payload[2:], exhibits["udp"].payload)

    def test_rest_and_graphql_exhibits_are_validly_framed_http_11(self) -> None:
        exhibits = {exhibit.slug: exhibit for exhibit in heresy.build_exhibits()}
        for slug in ("rest", "graphql"):
            payload = exhibits[slug].payload
            headers, body = payload.split(b"\r\n\r\n", 1)
            header_lines = headers.split(b"\r\n")
            self.assertTrue(header_lines[0].startswith(b"POST "))
            self.assertIn(b"Host: example.invalid", header_lines)
            self.assertIn(
                b"X-API-Key: LOST-IN-.env.old.backup.final2",
                header_lines,
            )
            content_length = next(
                line for line in header_lines if line.startswith(b"Content-Length: ")
            )
            self.assertEqual(int(content_length.split(b": ", 1)[1]), len(body))
            json.loads(body.decode("utf-8"))

    def test_corba_caveat_does_not_claim_idl_is_resent(self) -> None:
        exhibit = next(item for item in heresy.build_exhibits() if item.slug == "corba")
        self.assertIn("not resent on every invocation", exhibit.caveat)
        self.assertIn("GIOP-ish", exhibit.caveat)

    def test_every_exhibit_explains_value_and_caveat(self) -> None:
        for exhibit in heresy.build_exhibits():
            self.assertTrue(exhibit.punchline)
            self.assertTrue(exhibit.value_purchased)
            self.assertTrue(exhibit.caveat)
            self.assertGreater(exhibit.payload_bytes, 0)
            self.assertGreater(exhibit.estimated_tokens, 0)
            self.assertGreater(exhibit.ceremony_ratio, 0)

    def test_modern_modes_keep_the_lost_api_key_gag(self) -> None:
        modern = [item for item in heresy.build_exhibits() if item.authenticated]
        self.assertEqual([item.slug for item in modern], ["rest", "graphql", "agent-tool"])
        self.assertTrue(all("401" in item.auth_status for item in modern))
        self.assertEqual(heresy.API_KEY_LIFECYCLE[-1], "consider magnetic tape")

    def test_agent_tool_schema_matches_signed_int32_contract(self) -> None:
        exhibit = next(
            item for item in heresy.build_exhibits() if item.slug == "agent-tool"
        )
        payload = json.loads(exhibit.payload.decode("utf-8"))
        properties = payload["tool"]["input_schema"]["properties"]
        for name in ("a", "b"):
            self.assertEqual(properties[name]["type"], "integer")
            self.assertEqual(properties[name]["minimum"], heresy.INT32_MIN)
            self.assertEqual(properties[name]["maximum"], heresy.INT32_MAX)

    def test_style_selection_preserves_timeline_order(self) -> None:
        exhibits = heresy.build_exhibits()
        selected = heresy.select_exhibits(exhibits, ["agent-tool", "udp", "soap"])
        self.assertEqual([item.slug for item in selected], ["udp", "soap", "agent-tool"])

    def test_style_selection_rejects_unknown_slug(self) -> None:
        with self.assertRaises(ValueError):
            heresy.select_exhibits(heresy.build_exhibits(), ["carrier-pigeon"])

    def test_serialization_contains_required_time_machine_fields(self) -> None:
        rows = heresy.serialize(heresy.build_exhibits(), result=4)
        encoded = json.dumps(rows)
        self.assertIn('"intent"', encoded)
        self.assertIn('"payload_bytes"', encoded)
        self.assertIn('"estimated_tokens"', encoded)
        self.assertIn('"ceremony_ratio"', encoded)
        self.assertIn('"punchline"', encoded)
        self.assertIn('"caveat"', encoded)
        self.assertIn('"value_purchased"', encoded)
        self.assertIn('"payload_hex"', encoded)
        self.assertNotIn('"payload":', encoded)

    def test_table_and_empty_timeline_render(self) -> None:
        rendered = heresy.render_table(heresy.build_exhibits())
        self.assertIn("API TIME MACHINE", rendered)
        self.assertIn("INTENT", rendered)
        self.assertIn("CEREMONY", rendered)

        empty = heresy.render_table([])
        self.assertIn("EXHIBIT", empty)
        self.assertIn("ERA / STYLE", empty)

    def test_details_show_every_required_curatorial_field(self) -> None:
        selected = heresy.select_exhibits(heresy.build_exhibits(), ["rest"])
        rendered = heresy.render_details(selected, result=4)
        self.assertIn("Mathematics: 4", rendered)
        self.assertIn("Useful semantic intent:", rendered)
        self.assertIn("Application payload bytes:", rendered)
        self.assertIn("Approximate tokens:", rendered)
        self.assertIn("Ceremony Ratio:", rendered)
        self.assertIn("Punchline:", rendered)
        self.assertIn("What the ceremony buys:", rendered)
        self.assertIn("Engineering caveat:", rendered)
        self.assertIn("API KEY LIFECYCLE", rendered)
        self.assertIn("consider magnetic tape", rendered)

    def test_cli_json_supports_custom_operands_and_style(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = heresy.main(
                ["--left", "10", "--right", "-7", "--style", "udp", "--json"]
            )
        self.assertEqual(status, 0)
        document = json.loads(output.getvalue())
        self.assertEqual(document["intent"], "ADD 10 -7")
        self.assertEqual(document["result"], 3)
        self.assertEqual([row["slug"] for row in document["exhibits"]], ["udp"])

    def test_old_school_defense_remains_explicitly_conditional(self) -> None:
        rendered = heresy.render_transport_defense()
        self.assertIn("TCP:", rendered)
        self.assertIn("UDP:", rendered)
        self.assertIn("FTP / batch files:", rendered)
        self.assertIn("Price:", rendered)


if __name__ == "__main__":
    unittest.main()