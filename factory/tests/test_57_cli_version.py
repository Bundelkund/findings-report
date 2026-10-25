import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def run(*args):
    return subprocess.run(
        [sys.executable, "-m", "findings_report", *args],
        capture_output=True,
        text=True,
        cwd=Path.cwd(),
    )


class TestCliVersion(unittest.TestCase):
    def test_ak1_version_stdout_and_exit(self):
        r = run("--version")
        self.assertEqual(r.returncode, 0, "Exit-Code 0 erwartet")
        self.assertEqual(r.stdout.rstrip("\n"), "findings_report 0.1.0",
                         "genau die Zeile 'findings_report 0.1.0' erwartet")
        self.assertEqual(len(r.stdout.splitlines()), 1, "genau eine Zeile erwartet")

    def test_ak2_version_stderr_empty(self):
        r = run("--version")
        self.assertEqual(r.stderr, "", "stderr muss leer sein")

    def test_ak3_report_file_unchanged(self):
        report = {
            "title": "Testbericht",
            "verdict": "pass",
            "findings": [
                {"id": "F1", "title": "Ein Fund", "severity": "LOW"}
            ],
        }
        with tempfile.TemporaryDirectory(dir="/tmp") as d:
            p = Path(d) / "bericht.json"
            p.write_text(json.dumps(report), encoding="utf-8")
            r = run(str(p))
        self.assertEqual(r.returncode, 0, "Exit-Code 0 erwartet")
        self.assertEqual(r.stderr, "", "stderr muss leer sein")
        self.assertNotEqual(r.stdout, "findings_report 0.1.0\n",
                            "Ausgabe darf nicht die Versionszeile sein")
        self.assertNotEqual(r.stdout.strip(), "", "Berichtsausgabe erwartet")

if __name__ == "__main__":
    unittest.main()
