import json
import re
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

SEVERITIES = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']

EXAMPLE_FINDINGS = [
    {'id': 'F1', 'title': 'Passwort im Klartext', 'severity': 'CRITICAL'},
    {'id': 'F2', 'title': 'Zweites kritisches Problem', 'severity': 'CRITICAL'},
    {'id': 'F3', 'title': 'Abhaengigkeit veraltet', 'severity': 'HIGH'},
    {'id': 'F4', 'title': 'Fehlermeldung zeigt Pfade', 'severity': 'MEDIUM'},
    {'id': 'F5', 'title': 'Doppelte Funktion', 'severity': 'MEDIUM'},
    {'id': 'F6', 'title': 'Hinweis: Tests laufen 3 s', 'severity': 'INFO'},
]


class _AfterTitleParser(HTMLParser):
    """Sammelt den sichtbaren Text zwischen schliessendem h1 und der Befund-Liste."""

    def __init__(self):
        super().__init__()
        self.past_h1 = False
        self.hit_finding = False
        self.done = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        classes = (dict(attrs).get('class') or '').split()
        if 'finding' in classes:
            self.hit_finding = True

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.past_h1 = True
        elif self.past_h1 and self.parts and tag in ('p', 'div', 'section'):
            self.done = True

    def handle_data(self, data):
        if self.past_h1 and not self.hit_finding and not self.done and data.strip():
            self.parts.append(data.strip())


def summary_variants(html_text):
    parser = _AfterTitleParser()
    parser.feed(html_text)
    space = ' '.join(' '.join(parser.parts).split())
    plain = ' '.join(''.join(parser.parts).split())
    return space, plain


class TestZusammenfassungszeile(unittest.TestCase):

    def render(self, findings):
        report = {'title': 'Zusammenfassung', 'verdict': 'warn', 'findings': findings}
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / 'eingabe.json'
            out = Path(tmp) / 'seite.html'
            inp.write_text(json.dumps(report), encoding='utf-8')
            proc = subprocess.run(
                [sys.executable, '-m', 'findings_report', str(inp), str(out)],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0,
                'findings_report sollte mit Exit 0 enden, stderr: ' + str(proc.stderr))
            self.assertTrue(out.exists(), 'die Ausgabe-HTML-Datei sollte erzeugt werden')
            return out.read_text(encoding='utf-8')

    def test_ak1_zusammenfassungszeile_unter_titel(self):
        html_text = self.render(EXAMPLE_FINDINGS)
        space, plain = summary_variants(html_text)
        expected = '2 CRITICAL, 1 HIGH, 2 MEDIUM, 1 INFO'
        self.assertTrue(expected in (space, plain),
            'direkt unter dem Titel sollte als erstes sichtbarer Text die Zeile '
            + expected + ' stehen, gefunden: ' + repr(space))

    def test_ak2_ohne_funde_nicht_erwahnen(self):
        html_text = self.render(EXAMPLE_FINDINGS)
        space, _ = summary_variants(html_text)
        self.assertNotIn('LOW', space,
            'Schweregrad LOW hat keine Funde und darf nicht in der Zeile stehen: ' + repr(space))
        html2 = self.render([{'id': 'F1', 'title': 'Abhaengigkeit veraltet', 'severity': 'HIGH'}])
        space2, plain2 = summary_variants(html2)
        self.assertTrue('1 HIGH' in (space2, plain2),
            'mit nur einem HIGH-Fund muss die Zeile genau 1 HIGH lauten, gefunden: ' + repr(space2))

    def test_ak3_keine_funde(self):
        html_text = self.render([])
        space, plain = summary_variants(html_text)
        self.assertTrue('keine Funde' in (space, plain),
            'ohne Funde muss direkt nach dem Titel der Text keine Funde stehen, gefunden: ' + repr(space))
        for severity in SEVERITIES:
            self.assertNotIn(severity, space,
                'ohne Funde darf kein Schweregradname in der Zeile stehen: ' + repr(space))

    def test_ak4_breite_390(self):
        html_text = self.render(EXAMPLE_FINDINGS)
        meta = re.search(r'<meta[^>]*viewport[^>]*>', html_text)
        self.assertIsNotNone(meta, 'meta name=viewport fehlt im HTML')
        self.assertIn('width=device-width', meta.group(0),
            'viewport-meta muss width=device-width enthalten')
        for value in re.findall(r'(?<![a-z-])(?:min-)?width\s*:\s*([0-9]+(?:\.[0-9]+)?)px', html_text):
            self.assertLessEqual(float(value), 390,
                'CSS-Breite %s px ueberschreitet 390 px' % value)


if __name__ == '__main__':
    unittest.main()
