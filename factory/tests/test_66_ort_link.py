import unittest

import findings_report.render as render


def make_html(ort):
    report = {
        "title": "T",
        "verdict": "warn",
        "findings": [
            {"id": "F1", "title": "Titel", "severity": "LOW", "ort": ort}
        ],
    }
    return render.render_html(report)


class TestOrtLink(unittest.TestCase):
    def test_ak1_https_link_escaped(self):
        out = make_html("https://example.org/a?x=1&y=2")
        erwartet = '<a href="https://example.org/a?x=1&amp;y=2">https://example.org/a?x=1&amp;y=2</a>'
        self.assertIn(erwartet, out, "erwartet escapten Link mit gleichem Linktext")

    def test_ak2_javascript_plain_text(self):
        out = make_html("javascript:alert(1)")
        self.assertIn("javascript:alert(1)", out, "Text muss vorkommen")
        self.assertNotIn('<a href="javascript:alert(1)"', out, "kein Link erlaubt")
        self.assertNotIn(">javascript:alert(1)</a>", out, "kein Linktext erlaubt")

    def test_ak3_quotes_escaped(self):
        out = make_html('https://example.org/"onmouseover="alert(1)')
        erwartet = '<a href="https://example.org/&quot;onmouseover=&quot;alert(1)">'
        self.assertIn(erwartet, out, "href muss &quot; enthalten")
        start = out.index('<a href="') + len('<a href="')
        ende = out.index('">', start)
        self.assertNotIn('"', out[start:ende], "kein rohes Anfuehrungszeichen im href")

    def test_ak4_plain_path(self):
        out = make_html("src/app.py:12")
        self.assertIn("src/app.py:12", out, "Text muss vorkommen")
        self.assertNotIn('<a href="src/app.py:12"', out, "kein Link erlaubt")
        self.assertNotIn(">src/app.py:12</a>", out, "kein Linktext erlaubt")


if __name__ == "__main__":
    unittest.main()
