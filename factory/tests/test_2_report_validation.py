import unittest
import subprocess
import sys
import json
from pathlib import Path
import tempfile

class TestReportValidation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        for f in self.temp_dir.iterdir():
            f.unlink()
        self.temp_dir.rmdir()

    def _run_tool(self, file_path):
        command = [sys.executable, "-m", "findings_report", str(file_path)]
        result = subprocess.run(command, capture_output=True, text=True)
        return result

    def test_ak1_valid_report_exit_code_and_output(self):
        """AK1: Gültiger Bericht → Exit-Code 0 und genau eine Ausgabezeile `OK: <Anzahl> Befunde`."""
        report_content = {
            "title": "Test Report",
            "verdict": "pass",
            "findings": [
                {"id": "F001", "title": "Finding 1", "severity": "HIGH"},
                {"id": "F002", "title": "Finding 2", "severity": "MEDIUM"},
                {"id": "F003", "title": "Finding 3", "severity": "LOW"}
            ]
        }
        report_path = self.temp_dir / "valid_report.json"
        with open(report_path, "w") as f:
            json.dump(report_content, f)

        result = self._run_tool(report_path)

        self.assertEqual(result.returncode, 0, "Expected exit code 0 for a valid report.")
        self.assertEqual(result.stdout.strip(), "OK: 3 Befunde", "Expected 'OK: 3 Befunde' in stdout.")
        self.assertEqual(result.stderr, "", "Expected empty stderr for a valid report.")

    def test_ak2_file_not_exists_exit_code_and_message(self):
        """AK2: Datei existiert nicht → Exit-Code 2 und eine Meldung, die den Dateinamen nennt."""
        non_existent_path = self.temp_dir / "gibt_es_nicht_123.json"

        result = self._run_tool(non_existent_path)

        self.assertEqual(result.returncode, 2, "Expected exit code 2 for non-existent file.")
        self.assertIn(str(non_existent_path), result.stdout + result.stderr, "Expected filename in output for non-existent file.")

    def test_ak3_invalid_json_exit_code_and_message(self):
        """AK3: Datei ist kein gültiges JSON → Exit-Code 2 und eine Meldung „kein gültiges JSON“."""
        invalid_json_path = self.temp_dir / "invalid.json"
        with open(invalid_json_path, "w") as f:
            f.write("{kaputt")

        result = self._run_tool(invalid_json_path)

        self.assertEqual(result.returncode, 2, "Expected exit code 2 for invalid JSON.")
        self.assertIn("kein gültiges JSON", result.stdout + result.stderr, "Expected 'kein gültiges JSON' in output.")

    def test_ak4_missing_title_field(self):
        """AK4: Ein Pflichtfeld fehlt (`title`) → Exit-Code 2 und die Meldung nennt den Namen des fehlenden Feldes."""
        report_content = {
            "verdict": "pass",
            "findings": []
        }
        report_path = self.temp_dir / "missing_title.json"
        with open(report_path, "w") as f:
            json.dump(report_content, f)

        result = self._run_tool(report_path)

        self.assertEqual(result.returncode, 2, "Expected exit code 2 for missing 'title' field.")
        self.assertIn("title", result.stdout + result.stderr, "Expected 'title' in output for missing field.")

    def test_ak4_missing_verdict_field(self):
        """AK4: Ein Pflichtfeld fehlt (`verdict`) → Exit-Code 2 und die Meldung nennt den Namen des fehlenden Feldes."""
        report_content = {
            "title": "Test Report",
            "findings": []
        }
        report_path = self.temp_dir / "missing_verdict.json"
        with open(report_path, "w") as f:
            json.dump(report_content, f)

        result = self._run_tool(report_path)

        self.assertEqual(result.returncode, 2, "Expected exit code 2 for missing 'verdict' field.")
        self.assertIn("verdict", result.stdout + result.stderr, "Expected 'verdict' in output for missing field.")

    def test_ak4_missing_findings_field(self):
        """AK4: Ein Pflichtfeld fehlt (`findings`) → Exit-Code 2 und die Meldung nennt den Namen des fehlenden Feldes."""
        report_content = {
            "title": "Test Report",
            "verdict": "pass"
        }
        report_path = self.temp_dir / "missing_findings.json"
        with open(report_path, "w") as f:
            json.dump(report_content, f)

        result = self._run_tool(report_path)

        self.assertEqual(result.returncode, 2, "Expected exit code 2 for missing 'findings' field.")
        self.assertIn("findings", result.stdout + result.stderr, "Expected 'findings' in output for missing field.")

    def test_ak5_invalid_verdict_value(self):
        """AK5: `verdict` hat einen unerlaubten Wert → Exit-Code 2 und die Meldung nennt den Wert und die erlaubten Werte."""
        report_content = {
            "title": "Test Report",
            "verdict": "maybe",
            "findings": []
        }
        report_path = self.temp_dir / "invalid_verdict.json"
        with open(report_path, "w") as f:
            json.dump(report_content, f)

        result = self._run_tool(report_path)

        self.assertEqual(result.returncode, 2, "Expected exit code 2 for invalid 'verdict' value.")
        self.assertIn("maybe", result.stdout + result.stderr, "Expected invalid verdict value 'maybe' in output.")
        self.assertIn("pass", result.stdout + result.stderr, "Expected 'pass' in output for allowed verdicts.")
        self.assertIn("warn", result.stdout + result.stderr, "Expected 'warn' in output for allowed verdicts.")
        self.assertIn("fail", result.stdout + result.stderr, "Expected 'fail' in output for allowed verdicts.")

    def test_ak5_invalid_severity_value(self):
        """AK5: `severity` hat einen unerlaubten Wert → Exit-Code 2 und die Meldung nennt den Wert und die erlaubten Werte."""
        report_content = {
            "title": "Test Report",
            "verdict": "pass",
            "findings": [
                {"id": "F001", "title": "Finding 1", "severity": "URGENT"}
            ]
        }
        report_path = self.temp_dir / "invalid_severity.json"
        with open(report_path, "w") as f:
            json.dump(report_content, f)

        result = self._run_tool(report_path)

        self.assertEqual(result.returncode, 2, "Expected exit code 2 for invalid 'severity' value.")
        self.assertIn("URGENT", result.stdout + result.stderr, "Expected invalid severity value 'URGENT' in output.")
        self.assertIn("CRITICAL", result.stdout + result.stderr, "Expected 'CRITICAL' in output for allowed severities.")
        self.assertIn("HIGH", result.stdout + result.stderr, "Expected 'HIGH' in output for allowed severities.")
        self.assertIn("MEDIUM", result.stdout + result.stderr, "Expected 'MEDIUM' in output for allowed severities.")
        self.assertIn("LOW", result.stdout + result.stderr, "Expected 'LOW' in output for allowed severities.")
        self.assertIn("INFO", result.stdout + result.stderr, "Expected 'INFO' in output for allowed severities.")
