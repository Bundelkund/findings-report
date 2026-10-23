import json
import re
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path.cwd()

ISSUE_EXAMPLE = {
    "title": "Zusammenfassung",
    "verdict": "warn",
    "findings": [
        {"id": "F1", "title": "Passwort im Klartext", "severity": "CRITICAL"},
        {"id": "F2", "title": "Zweites kritisches Problem", "severity": "CRITICAL"},
        {"id": "F3", "title": "Abhaengigkeit veraltet", "severity": "HIGH"},
        {"id": "F4", "title": "Fehlermeldung zeigt Pfade", "severity": "MEDIUM"},
        {"id": "F5", "title": "Doppelte Funktion", "severity": "MEDIUM"},
        {"id": "F6", "title": "Hinweis: Tests laufen 3 s", "severity": "INFO"},
    ],
}

ALL_SEVERITIES = {
    "title": "Alle Schweregrade",
    "verdict": "warn",
    "findings": [
        {"id": "A1", "title": "Kritisch", "severity": "CRITICAL"},
        {"id": "A2", "title": "Hoch", "severity": "HIGH"},
        {"id": "A3", "title": "Mittel", "severity": "MEDIUM"},
        {"id": "A4", "title": "Niedrig", "severity": "LOW"},
        {"id": "A5", "title": "Info", "severity": "INFO"},
    ],
}

EMPTY_FINDINGS = {"title": "Leer", "verdict": "pass", "findings": []}

VOID_TAGS = {"meta", "br", "hr", "img", "link", "input"}


class ElementParser(HTMLParser):
    """Collects (tag, text) for every non-void element in document order."""

    def __init__(self):
        super().__init__()
        self.elements = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return
        self.stack.append([tag, []])

    def handle_endtag(self, tag):
        while self.stack:
            top = self.stack.pop()
            self.elements.append((top[0], "".join(top[1]).strip()))
            if top[0] == tag:
                return

    def handle_data(self, data):
        if self.stack:
            self.stack[-1][1].append(data)


class MetaParser(HTMLParser):
    """Collects the attrs of all meta elements."""

    def __init__(self):
        super().__init__()
        self.metas = []

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            self.metas.append(dict(attrs))


def run_report(payload):
    """Runs python -m findings_report on a payload dict, returns (proc, out_path, html_text)."""
    tmp = Path(tempfile.mkdtemp(prefix="issue35_"))
    inp = tmp / "eingabe.json"
    inp.write_text(json.dumps(payload), encoding="utf-8")
    out = tmp / "ausgabe.html"
    proc = subprocess.run(
        [sys.executable, "-m", "findings_report", str(inp), str(out)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    html_text = out.read_text(encoding="utf-8") if out.exists() else ""
    return proc, out, html_text


def text_after_h1(html_text):
    """Returns the text of the first element after the h1 title element."""
    parser = ElementParser()
    parser.feed(html_text)
    parser.close()
    tags = [tag for tag, _ in parser.elements]
    if "h1" not in tags:
        return None
    idx = tags.index("h1")
    if idx + 1 >= len(parser.elements):
        return None
    return parser.elements[idx + 1][1]


class TestZusammenfassungszeile(unittest.TestCase):
    def test_ak1_alle_fuenf_schweregrade(self):
        proc, out, html_text = run_report(ALL_SEVERITIES)
        self.assertEqual(proc.returncode, 0, "python -m findings_report sollte fehlerfrei laufen")
        self.assertTrue(out.exists(), "die Ausgabe-HTML-Datei sollte geschrieben werden")
        text = text_after_h1(html_text)
        self.assertIsNotNone(text, "unter dem h1-Titel sollte ein weiteres Element stehen")
        self.assertEqual(
            text,
            "1 CRITICAL, 1 HIGH, 1 MEDIUM, 1 LOW, 1 INFO",
            "erwartet Zusammenfassungszeile '1 CRITICAL, 1 HIGH, 1 MEDIUM, 1 LOW, 1 INFO' direkt unter dem Titel",
        )

    def test_ak2_ohne_funde_weglassen(self):
        proc, out, html_text = run_report(ISSUE_EXAMPLE)
        self.assertEqual(proc.returncode, 0, "python -m findings_report sollte fehlerfrei laufen")
        self.assertTrue(out.exists(), "die Ausgabe-HTML-Datei sollte geschrieben werden")
        text = text_after_h1(html_text)
        self.assertIsNotNone(text, "unter dem h1-Titel sollte ein weiteres Element stehen")
        self.assertEqual(
            text,
            "2 CRITICAL, 1 HIGH, 2 MEDIUM, 1 INFO",
            "erwartet Zusammenfassungszeile '2 CRITICAL, 1 HIGH, 2 MEDIUM, 1 INFO' (LOW entfaellt, keine Funde)",
        )
        self.assertNotIn("LOW", text, "Schweregrad ohne Funde (LOW) darf nicht in der Zeile stehen")

    def test_ak3_keine_funde(self):
        proc, out, html_text = run_report(EMPTY_FINDINGS)
        self.assertEqual(proc.returncode, 0, "python -m findings_report sollte fehlerfrei laufen")
        self.assertTrue(out.exists(), "die Ausgabe-HTML-Datei sollte geschrieben werden")
        text = text_after_h1(html_text)
        self.assertIsNotNone(text, "unter dem h1-Titel sollte ein weiteres Element stehen")
        self.assertEqual(
            (text or "").strip(),
            "keine Funde",
            "ohne Funde sollte die Zeile nach dem Titel 'keine Funde' sein",
        )

    def test_ak4_390px_breite(self):
        proc, out, html_text = run_report(ISSUE_EXAMPLE)
        self.assertEqual(proc.returncode, 0, "python -m findings_report sollte fehlerfrei laufen")
        self.assertTrue(out.exists(), "die Ausgabe-HTML-Datei sollte geschrieben werden")
        meta_parser = MetaParser()
        meta_parser.feed(html_text)
        meta_parser.close()
        self.assertTrue(
            any(
                (m.get("name") or "").lower() == "viewport"
                and "width=device-width" in (m.get("content") or "")
                for m in meta_parser.metas
            ),
            "erwartet ein meta-Element name='viewport' mit 'width=device-width'",
        )
        for match in re.finditer(r"(?:min-)?width\s*:\s*([0-9]+(?:\.[0-9]+)?)px", html_text):
            value = float(match.group(1))
            self.assertLessEqual(
                value,
                390,
                "keine feste width/min-width in px groesser als 390 erlaubt, gefunden: %spx" % match.group(1),
            )

    def test_ak5_befehl_bsp_eingabe(self):
        tmp = Path(tempfile.mkdtemp(prefix="issue35_cli_"))
        inp = tmp / "b.json"
        inp.write_text(json.dumps(ISSUE_EXAMPLE), encoding="utf-8")
        out = tmp / "seite.html"
        proc = subprocess.run(
            [sys.executable, "-m", "findings_report", str(inp), str(out)],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(proc.returncode, 0, "Rueckgabecode 0 erwartet, stderr: %s" % proc.stderr)
        self.assertTrue(out.exists(), "die Ausgabedatei sollte geschrieben werden")


if __name__ == "__main__":
    unittest.main()
