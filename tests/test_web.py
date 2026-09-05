from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
PAGES_URL = "https://qsolkcb.github.io/HERESY-API/"


class OfflineCalculatorTests(unittest.TestCase):
    def test_static_app_has_local_entrypoint_and_assets(self) -> None:
        index = (WEB / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="./style.css"', index)
        self.assertIn('src="./heresy-core.js"', index)
        self.assertIn('src="./app.js"', index)
        for name in ("index.html", "style.css", "heresy-core.js", "app.js", ".nojekyll"):
            self.assertTrue((WEB / name).exists(), name)

    def test_static_app_has_no_remote_runtime_dependency(self) -> None:
        combined = "\n".join(
            (WEB / name).read_text(encoding="utf-8")
            for name in ("index.html", "style.css", "heresy-core.js", "app.js")
        )
        self.assertNotIn("http://", combined.lower())
        self.assertNotIn("https://", combined.lower())
        self.assertNotIn("fetch(", combined)
        self.assertNotIn("XMLHttpRequest", combined)
        self.assertNotIn("WebSocket", combined)

    def test_ui_retains_required_joke_and_measurement_surfaces(self) -> None:
        index = (WEB / "index.html").read_text(encoding="utf-8")
        core = (WEB / "heresy-core.js").read_text(encoding="utf-8")
        for marker in (
            'id="result"',
            'id="intent"',
            'id="payload"',
            'id="payload-bytes"',
            'id="tokens"',
            'id="ceremony-ratio"',
            'id="punchline"',
            'id="api-key-status"',
            'id="auth-status"',
            "NO API KEY FOR DAVE TO LOSE",
            "Nothing executes until enterprise arithmetic is committed",
        ):
            self.assertIn(marker, index)
        self.assertIn('authenticationStatus: authenticated ? "401"', core)
        self.assertIn('remediation: authenticated ? "rewind tape"', core)

    def test_readme_links_live_pages_calculator(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(PAGES_URL, readme)
        self.assertIn("COMMIT ENTERPRISE ARITHMETIC", readme)
        self.assertIn("stages", readme)

    def test_pages_workflow_publishes_only_static_web_directory(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        self.assertIn("actions/upload-pages-artifact", workflow)
        self.assertIn("actions/deploy-pages", workflow)
        self.assertIn("path: web", workflow)
        self.assertIn("pages: write", workflow)
        self.assertIn("id-token: write", workflow)


if __name__ == "__main__":
    unittest.main()
