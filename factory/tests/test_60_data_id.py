import re
import unittest

from findings_report.render import render_html


def make_report(findings):
    return {"title": "Titel", "verdict": "pass", "findings": findings}


def finding(fid):
    return {"id": fid, "title": "Ein Befund", "severity": "LOW"}


def li_tags(html):
    return re.findall(r"<li\b[^>]*>", html)


class TestDataId(unittest.TestCase):
    def test_ak1_data_id_simple(self):
        html = render_html(make_report([finding("F1")]))
        tags = li_tags(html)
        self.assertTrue(
            any('data-id="F1"' in t for t in tags),
            "erwartet: li-Start-Tag mit data-id=\"F1\", gefunden: %r" % tags,
        )

    def test_ak2_data_id_escaped(self):
        raw = 'a"b<c'
        html = render_html(make_report([finding(raw)]))
        tags = li_tags(html)
        self.assertTrue(
            any('data-id="a&quot;b&lt;c"' in t for t in tags),
            "erwartet: escaped data-id im li-Start-Tag, gefunden: %r" % tags,
        )
        self.assertNotIn(raw, html, "roher String darf nirgends vorkommen")

    def test_ak3_no_findings_no_data_id(self):
        html = render_html(make_report([]))
        self.assertNotIn("data-id", html, "ohne Befunde kein data-id")


if __name__ == "__main__":
    unittest.main()
