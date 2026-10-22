import json
import re
import subprocess
import sys
import tempfile
import unittest
import html as html_mod
from html.parser import HTMLParser
from pathlib import Path

CANARY = {
    "title": "Canary",
    "verdict": "warn",
    "findings": [
        {"id": "F1", "title": "Passwort im Klartext", "severity": "CRITICAL"},
        {"id": "F2", "title": "Abhaengigkeit veraltet", "severity": "HIGH"},
        {"id": "F3", "title": "Fehlermeldung zeigt Pfade", "severity": "MEDIUM"},
        {"id": "F4", "title": "Kommentar veraltet", "severity": "LOW"},
        {"id": "F5", "title": "Hinweis: Tests laufen 3 s", "severity": "INFO"},
    ],
}

SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]


class BadgeParser(HTMLParser):
    """Sammelt alle span-Elemente, deren class 'badge' enthaelt, mit ihrem Text."""

    def __init__(self):
        super().__init__()
        self.badges = []
        self._stack = []

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            classes = dict(attrs).get("class", "")
            self._stack.append(("badge" in classes.split(), classes, []))
        else:
            self._stack.append((False, "", []))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if self._stack:
            is_badge, classes, data = self._stack.pop()
            if is_badge:
                self.badges.append((classes, "".join(data).strip()))

    def handle_data(self, data):
        if self._stack:
            self._stack[-1][2].append(data)


def run_report(payload):
    """Fuehrt python -m findings_report mit dem Payload aus, liefert (proc, Ausgabe-Text)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        inp = tmpdir / "in.json"
        outp = tmpdir / "out.html"
        inp.write_text(json.dumps(payload), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-m", "findings_report", str(inp), str(outp)],
            capture_output=True,
            text=True,
        )
        content = outp.read_text(encoding="utf-8") if outp.exists() else ""
    return proc, content


def style_block(content):
    m = re.search(r"<style[^>]*>(.*?)</style>", content, re.S | re.I)
    return m.group(1) if m else ""


def rule_for(style, cls):
    m = re.search(r"\." + re.escape(cls) + r"\s*\{([^}]*)\}", style)
    return m.group(1) if m else ""


def css_color(rule, prop):
    m = re.search(prop + r"\s*:\s*(#[0-9a-fA-F]{3,6})", rule)
    return m.group(1) if m else None


def hex_to_rgb(value):
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    return tuple(int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def relative_luminance(value):
    r, g, b = hex_to_rgb(value)

    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast_ratio(fg, bg):
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


class BadgeTests(unittest.TestCase):
    def test_ak1_badge_elemente_mit_schweregrad(self):
        proc, content = run_report(CANARY)
        self.assertEqual(proc.returncode, 0, "python -m findings_report muss mit Exitcode 0 laufen")
        self.assertTrue(content, "Es muss eine HTML-Ausgabedatei erzeugt werden")
        parser = BadgeParser()
        parser.feed(content)
        gefunden = {}
        for classes, text in parser.badges:
            gefunden[text] = classes
        for sev in SEVERITIES:
            self.assertIn(sev, gefunden, "Badge-Text %s muss in der Seite stehen" % sev)
            cl = gefunden[sev].split()
            self.assertIn("badge", cl, "Badge-Element fuer %s muss Klasse 'badge' haben" % sev)
            self.assertIn("badge-" + sev.lower(), cl, "Badge fuer %s muss Klasse 'badge-%s' haben" % (sev, sev.lower()))

    def test_ak2_badge_vor_titel_im_quelltext(self):
        proc, content = run_report(CANARY)
        self.assertEqual(proc.returncode, 0, "python -m findings_report muss mit Exitcode 0 laufen")
        for f in CANARY["findings"]:
            escaped = html_mod.escape(f["title"])
            idx_title = content.find(escaped)
            self.assertGreaterEqual(idx_title, 0, "Escapter Titel %r muss in der Seite stehen" % escaped)
            badge_vorhanden = False
            for m in re.finditer(r'<span\s+class="([^"]*)"[^>]*>([^<]*)</span>', content):
                classes = m.group(1).split()
                text = m.group(2).strip()
                if "badge" in classes and text == f["severity"] and m.start() < idx_title:
                    badge_vorhanden = True
                    break
            self.assertTrue(badge_vorhanden, "Badge %s muss im Quelltext vor dem Titel %r stehen" % (f["severity"], escaped))

    def test_ak3_hintergrundfarben_der_badge_klassen(self):
        proc, content = run_report(CANARY)
        self.assertEqual(proc.returncode, 0, "python -m findings_report muss mit Exitcode 0 laufen")
        style = style_block(content)
        import colorsys

        erwartet = {
            "badge-critical": "rot",
            "badge-high": "orange",
            "badge-medium": "gelb",
            "badge-low": "grau",
            "badge-info": "grau",
        }
        for cls, farbe in erwartet.items():
            rule = rule_for(style, cls)
            bg = css_color(rule, "background(?:-color)?")
            self.assertIsNotNone(bg, "Klasse %s braucht eine Hintergrundfarbe als Hex-Wert" % cls)
            r, g, b = hex_to_rgb(bg)
            h, l, s = colorsys.rgb_to_hls(r, g, b)
            hue = h * 360.0
            if farbe == "rot":
                ok = hue >= 345.0 or hue <= 15.0
            elif farbe == "orange":
                ok = 16.0 <= hue <= 45.0
            elif farbe == "gelb":
                ok = 46.0 <= hue <= 65.0
            else:
                ok = s < 0.15
            self.assertTrue(ok, "Hintergrundfarbe %s von %s muss %s sein (Hue=%.1f, Saettigung=%.3f)" % (bg, cls, farbe, hue, s))

    def test_ak4_kontrast_mindestens_45(self):
        proc, content = run_report(CANARY)
        self.assertEqual(proc.returncode, 0, "python -m findings_report muss mit Exitcode 0 laufen")
        style = style_block(content)
        for cls in ["badge-critical", "badge-high", "badge-medium", "badge-low", "badge-info"]:
            rule = rule_for(style, cls)
            fg = css_color(rule, "(?<!-)color")
            bg = css_color(rule, "background(?:-color)?")
            self.assertIsNotNone(fg, "Klasse %s braucht eine Textfarbe als Hex-Wert" % cls)
            self.assertIsNotNone(bg, "Klasse %s braucht eine Hintergrundfarbe als Hex-Wert" % cls)
            ratio = contrast_ratio(fg, bg)
            self.assertGreaterEqual(ratio, 4.5, "Kontrast von %s (%s auf %s) muss >= 4.5:1 sein, ist %.2f" % (cls, fg, bg, ratio))

    def test_ak5_viewport_und_maximale_breite(self):
        proc, content = run_report(CANARY)
        self.assertEqual(proc.returncode, 0, "python -m findings_report muss mit Exitcode 0 laufen")
        m = re.search(r"<meta[^>]*name=\"viewport\"[^>]*>", content, re.I)
        self.assertIsNotNone(m, "Seite braucht ein meta-viewport-Tag")
        self.assertIn("width=device-width", m.group(0), "meta-viewport muss width=device-width enthalten")
        for val in re.findall(r"(?:min-)?width\s*:\s*(\d+(?:\.\d+)?)px", content):
            self.assertLessEqual(float(val), 390, "Keine (min-)width-Angabe mit px-Wert ueber 390 erlaubt, gefunden: %spx" % val)

    def test_ak6_titel_escaped(self):
        payload = {
            "title": "Escape",
            "verdict": "warn",
            "findings": [
                {"id": "F1", "title": '<script>alert(1)</script> & "x"', "severity": "HIGH"}
            ],
        }
        proc, content = run_report(payload)
        self.assertEqual(proc.returncode, 0, "python -m findings_report muss mit Exitcode 0 laufen")
        self.assertIn("&lt;script&gt;", content, "Der Titel muss als &lt;script&gt; escaped sein")
        self.assertIn("&amp;", content, "Das & im Titel muss als &amp; escaped sein")
        self.assertNotIn("<script>alert(1)</script>", content, "Der rohe String <script>alert(1)</script> darf nicht vorkommen")


if __name__ == "__main__":
    unittest.main()
