import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

WARNUNG = "Warnung: Titel hat mehr als 200 Zeichen"


def _bericht(title):
    return {
        "title": title,
        "verdict": "pass",
        "findings": [
            {"id": "F1", "title": "Ein Fund", "severity": "LOW"}
        ],
    }


class TestTitleWarning(unittest.TestCase):
    def _run(self, title, with_html=False):
        tmp = tempfile.mkdtemp(dir="/tmp")
        src = os.path.join(tmp, "bericht.json")
        out = os.path.join(tmp, "ausgabe.html")
        with open(src, "w", encoding="utf-8") as f:
            json.dump(_bericht(title), f)
        args = [sys.executable, "-m", "findings_report", src]
        if with_html:
            args.append(out)
        res = subprocess.run(args, capture_output=True, text=True,
                             encoding="utf-8", cwd=str(Path.cwd()))
        return res, out

    def test_ak1_warnung_bei_201_zeichen(self):
        res, _ = self._run("a" * 201)
        self.assertEqual(res.stderr.strip(), WARNUNG,
                         "stderr soll genau die Warnzeile enthalten")
        self.assertEqual(res.returncode, 0, "Exit-Code soll 0 sein")

    def test_ak2_keine_warnung_bei_200_zeichen(self):
        res, _ = self._run("a" * 200)
        self.assertEqual(res.stderr, "", "stderr soll leer sein")

    def test_ak3_html_mit_warnung(self):
        titel = "b" * 201
        res, out = self._run(titel, with_html=True)
        self.assertEqual(res.stderr.strip(), WARNUNG,
                         "stderr soll die Warnung enthalten")
        self.assertTrue(os.path.exists(out), "HTML-Datei soll existieren")
        with open(out, encoding="utf-8") as f:
            inhalt = f.read()
        self.assertIn(titel, inhalt, "voller Titel soll im HTML stehen")


if __name__ == "__main__":
    unittest.main()
