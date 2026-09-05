import unittest

import heresy


class CodexRegressionTests(unittest.TestCase):
    def test_intent_rejects_bool_and_non_int_operands(self) -> None:
        for left, right in (
            (True, False),
            (1.0, 2),
            (1, "2"),
        ):
            with self.subTest(left=left, right=right):
                with self.assertRaises(TypeError):
                    heresy.Intent(left, right)

    def test_all_style_must_be_used_alone(self) -> None:
        exhibits = heresy.build_exhibits()
        self.assertEqual(
            heresy.select_exhibits(exhibits, ["all"]),
            exhibits,
        )
        with self.assertRaises(ValueError):
            heresy.select_exhibits(exhibits, ["all", "udp"])

    def test_all_style_does_not_mask_unknown_slug(self) -> None:
        with self.assertRaises(ValueError):
            heresy.select_exhibits(
                heresy.build_exhibits(),
                ["all", "carrier-pigeon"],
            )


if __name__ == "__main__":
    unittest.main()
