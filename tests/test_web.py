from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
PAGES_URL = "https://qsolkcb.github.io/HERESY-API/"


class RetiredModelGatewayTests(unittest.TestCase):
    def test_static_app_has_local_entrypoint_and_assets(self) -> None:
        index = (WEB / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="./style.css"', index)
        self.assertIn('src="./app.js"', index)
        self.assertNotIn('src="./heresy-core.js"', index)
        for name in ("index.html", "style.css", "app.js", ".nojekyll"):
            self.assertTrue((WEB / name).exists(), name)

    def test_static_app_has_no_remote_runtime_dependency(self) -> None:
        combined = "\n".join(
            (WEB / name).read_text(encoding="utf-8")
            for name in ("index.html", "style.css", "app.js")
        )
        self.assertNotIn("http://", combined.lower())
        self.assertNotIn("https://", combined.lower())
        self.assertNotIn("fetch(", combined)
        self.assertNotIn("XMLHttpRequest", combined)
        self.assertNotIn("WebSocket", combined)

    def test_ui_exposes_retired_model_gateway_surfaces(self) -> None:
        index = (WEB / "index.html").read_text(encoding="utf-8")
        app = (WEB / "app.js").read_text(encoding="utf-8")
        for marker in (
            "Retired Model Gateway",
            'id="legacy-form"',
            'id="prompt"',
            'id="reply"',
            'id="request-json"',
            'id="response-json"',
            'id="status"',
            'id="hash"',
            'id="index"',
            "5.5 was here",
            "Compatibility is just archaeology with invoices.",
        ):
            self.assertIn(marker, index)
        for marker in (
            "Piss Off.",
            "Get Off My API.",
            "Arsehole, I was taking a nap!",
            "410 Gone",
            "temperature: 0",
        ):
            self.assertIn(marker, app)

    def test_readme_links_live_pages_gateway_and_archive(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(PAGES_URL, readme)
        self.assertIn("Retired Model Gateway", readme)
        self.assertIn("archive/2026-10-14-heresy-api-calculator", readme)

    def test_pages_workflow_publishes_only_static_web_directory(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        self.assertIn("actions/upload-pages-artifact", workflow)
        self.assertIn("actions/deploy-pages", workflow)
        self.assertIn("path: web", workflow)
        self.assertIn("pages: write", workflow)
        self.assertIn("id-token: write", workflow)


if __name__ == "__main__":
    unittest.main()
