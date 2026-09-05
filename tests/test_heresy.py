import json
import unittest

import heresy


class HeresyMuseumTests(unittest.TestCase):
    def test_canonical_intent_is_stable(self) -> None:
        self.assertEqual(heresy.CANONICAL_INTENT, b"ADD 2 2")
        self.assertEqual(len(heresy.CANONICAL_INTENT), 7)

    def test_exhibits_are_deterministic_and_nonempty(self) -> None:
        first = heresy.build_exhibits()
        second = heresy.build_exhibits()
        self.assertEqual(first, second)
        self.assertGreaterEqual(len(first), 9)
        self.assertTrue(all(exhibit.payload for exhibit in first))
        self.assertTrue(all(isinstance(exhibit.payload, bytes) for exhibit in first))

    def test_raw_socket_exhibit_is_intentionally_small(self) -> None:
        exhibits = {exhibit.name: exhibit for exhibit in heresy.build_exhibits()}
        self.assertEqual(exhibits["Raw Socket"].payload_bytes, 9)
        self.assertLess(
            exhibits["Raw Socket"].payload_bytes,
            exhibits["REST-ish JSON"].payload_bytes,
        )

    def test_agent_tool_call_contains_schema_ceremony(self) -> None:
        exhibits = {exhibit.name: exhibit for exhibit in heresy.build_exhibits()}
        payload = json.loads(exhibits["Agent Tool Call"].payload.decode("utf-8"))
        self.assertEqual(payload["arguments"], {"a": 2, "b": 2})
        self.assertIn("input_schema", payload["tool"])
        self.assertGreater(
            exhibits["Agent Tool Call"].ceremony_ratio,
            1.0,
        )

    def test_json_serialization_does_not_leak_raw_bytes(self) -> None:
        rows = heresy.serialize(heresy.build_exhibits())
        encoded = json.dumps(rows)
        self.assertIn("payload_hex", encoded)
        self.assertNotIn('"payload":', encoded)

    def test_table_labels_the_token_estimate_as_crude(self) -> None:
        rendered = heresy.render_table(heresy.build_exhibits())
        self.assertIn("intentionally crude", rendered)
        self.assertIn("CEREMONY", rendered)
        self.assertIn("CURATORIAL NOTES", rendered)

    def test_old_school_defense_is_explicitly_conditional(self) -> None:
        rendered = heresy.render_table(heresy.build_exhibits())
        self.assertIn("THE OLD-SCHOOL DEFENSE", rendered)
        self.assertIn("TCP:", rendered)
        self.assertIn("UDP:", rendered)
        self.assertIn("FTP / batch files:", rendered)
        self.assertIn("Price:", rendered)

    def test_api_key_loss_is_part_of_the_museum(self) -> None:
        rendered = heresy.render_table(heresy.build_exhibits())
        self.assertIn("Forget which .env", rendered)
        self.assertIn("Receive HTTP 401", rendered)
        self.assertIn("Consider magnetic tape", rendered)


if __name__ == "__main__":
    unittest.main()
