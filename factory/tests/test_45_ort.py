import json
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path


def run(*args):
    return subprocess.run([sys.executable, "-m", "findings_report", *args],
                          capture_output=True, text=True)


def finding(i, ort=None, has_ort=False):
    f = {"id": "F%d" % i, "title": "Titel %d" % i, "severity": "HIGH"}
    if has_ort:
        f["ort"] = ort
    return f


def report(findings):
    return {"title": "Bericht", "verdict": "warn", "findings": findings}


class LiParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lis = []
        self.cur = None
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            self.cur = {"events": []}
            self.lis.append(self.cur)
            return
        if self.cur is not None:
            cls = (dict(attrs).get("class") or "").split()
            self.cur["events"].append(("start", tag, cls))

    def handle_endtag(self, tag):
        if tag == "li":
            self.cur = None

    def handle_data(self, data):
        if self.cur is not None:
            self.cur["events"].append(("data", data.strip(), []))


class TestOrt(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, data, name="b.json"):
        p = self.dir / name
        p.write_text(json.dumps(data), encoding="utf-8")
        return p

    def test_ak1_mit_ort_gueltig(self):
        p = self.write(report([finding(1, "render.py:42", True), finding(2), finding(3)]))
        r = run(str(p))
        self.assertEqual(r.returncode, 0, "Exit 0 erwartet")
        self.assertEqual(r.stdout.strip(), "OK: 3 Befunde")

    def test_ak2_ohne_ort_gueltig(self):
        p = self.write(report([finding(1), finding(2), finding(3)]))
        r = run(str(p))
        self.assertEqual(r.returncode, 0, "Exit 0 erwartet")
        self.assertEqual(r.stdout.strip(), "OK: 3 Befunde")

    def test_ak3_ungueltiger_ort(self):
        for bad in (42, ""):
            with self.subTest(ort=bad):
                p = self.write(report([finding(1, bad, True), finding(2)]))
                r = run(str(p))
                self.assertEqual(r.returncode, 2, "Exit 2 erwartet")
                self.assertIn("findings[0].ort", r.stdout + r.stderr)

    def render(self, data):
        p = self.write(data)
        out = self.dir / "s.html"
        r = run(str(p), str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        raw = out.read_text(encoding="utf-8")
        parser = LiParser()
        parser.feed(raw)
        return raw, parser.lis

    def data(self):
        return report([
            finding(1, "<script>x</script>", True),
            finding(2),
            finding(3, "Kapitel 3", True)])

    def li_for(self, lis, fid):
        for li in lis:
            if any(e[0] == "data" and e[1] == fid for e in li["events"]):
                return li
        self.fail("li fuer " + fid + " fehlt")

    def test_ak4_html_ort(self):
        raw, lis = self.render(self.data())
        self.assertIn("&lt;script&gt;x&lt;/script&gt;", raw)
        self.assertNotIn("<script>x</script>", raw)
        ev = self.li_for(lis, "F1")["events"]
        ort_idx = [i for i, e in enumerate(ev) if e[0] == "start" and "ort" in e[2]]
        self.assertEqual(len(ort_idx), 1, "genau ein Element mit Klasse ort")
        id_idx = [i for i, e in enumerate(ev) if e[0] == "data" and e[1] == "F1"][0]
        self.assertGreater(ort_idx[0], id_idx, "ort nach der Befund-ID")

    def test_ak5_ohne_ort_kein_element(self):
        raw, lis = self.render(self.data())
        ev = self.li_for(lis, "F2")["events"]
        self.assertFalse([e for e in ev if e[0] == "start" and "ort" in e[2]],
                         "F2 darf kein Element mit Klasse ort haben")
