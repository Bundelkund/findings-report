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

    def _run_module(self, file_path):
        command = [sys.executable, "-m", "findings_report", str(file_path)]
        return subprocess.run(command, capture_output=True, text=True, cwd=Path.cwd())

    def test_ak1_valid_report_exit_code_and_output(self):
        report_content = {
            "title": "Test Report",
            "verdict": "pass",
            "findings": [
                {"id": "F1", "title": "Finding 1", "severity": "HIGH"},
                {"id": "F2", "title": "Finding 2", "severity": "MEDIUM"},
                {"id": "F3", "title": "Finding 3", "severity": "LOW"}
            ]
        }
        report_path = self.temp_dir / "valid_report.json"
        with open(report_path, "w") as f:
            json.dump(report_content, f)

        result = self._run_module(report_path)

        self.assertEqual(result.returncode, 0, f"Expected exit code 0 for valid report, got {result.returncode}. Stderr: {result.stderr}")
        self.assertEqual(result.stdout.strip(), "OK: 3 Befunde", f"Expected 'OK: 3 Befunde', got '{result.stdout.strip()}'")

    def test_ak2_file_not_exists_exit_code_and_message(self):
        non_existent_path = self.temp_dir / "gibt_es_nicht_123.json"
        result = self._run_module(non_existent_path)

        self.assertEqual(result.returncode, 2, f"Expected exit code 2 for non-existent file, got {result.returncode}. Stderr: {result.stderr}")
        output = result.stdout + result.stderr
        self.assertIn(str(non_existent_path), output, f"Expected filename '{non_existent_path}' in output, got '{output}'")

    def test_ak3_invalid_json_exit_code_and_message(self):
        invalid_json_path = self.temp_dir / "invalid.json"
        with open(invalid_json_path, "w") as f:
            f.write("{kaputt")

        result = self._run_module(invalid_json_path)

        self.assertEqual(result.returncode, 2, f"Expected exit code 2 for invalid JSON, got {result.returncode}. Stderr: {result.stderr}")
        output = result.stdout + result.stderr
        self.assertIn("kein gültiges JSON", output, f"Expected 'kein gültiges JSON' in output, got '{output}'")

    def test_ak4_missing_title_field(self):
        report_content = {
            "verdict": "pass",
            "findings": []
        }
        report_path = self.temp_dir / "missing_title.json"
        with open(report_path, "w") as f:
            json.dump(report_content, f)

        result = self._run_module(report_path)

        self.assertEqual(result.returncode, 2, f"Expected exit code 2 for missing 'title', got {result.returncode}. Stderr: {result.stderr}")
        output = result.stdout + result.stderr
        self.assertIn("title", output, f"Expected 'title' in output, got '{output}'")

    def test_ak4_missing_verdict_field(self):
        report_content = {
            "title": "Test Report",
            "findings": []
        }
        report_path = self.temp_dir / "missing_verdict.json"
        with open(report_path, "w") as f:
            json.dump(report_content, f)

        result = self._run_module(report_path)

        self.assertEqual(result.returncode, 2, f"Expected exit code 2 for missing 'verdict', got {result.returncode}. Stderr: {result.stderr}")
        output = result.stdout + result.stderr
        self.assertIn("verdict", output, f"Expected 'verdict' in output, got '{output}'")

    def test_ak4_missing_findings_field(self):
        report_content = {
            "title": "Test Report",
            "verdict": "pass"
        }
        report_path = self.temp_dir / "missing_findings.json"
        with open(report_path, "w") as f:
            json.dump(report_content, f)

        result = self._run_module(report_path)

        self.assertEqual(result.returncode, 2, f"Expected exit code 2 for missing 'findings', got {result.returncode}. Stderr: {result.stderr}")
        output = result.stdout + result.stderr
        self.assertIn("findings", output, f"Expected 'findings' in output, got '{output}'")

    def test_ak5_invalid_verdict_value(self):
        report_content = {
            "title": "Test Report",
            "verdict": "maybe",
            "findings": []
        }
        report_path = self.temp_dir / "invalid_verdict.json"
        with open(report_path, "w") as f:
            json.dump(report_content, f)

        result = self._run_module(report_path)

        self.assertEqual(result.returncode, 2, f"Expected exit code 2 for invalid verdict, got {result.returncode}. Stderr: {result.stderr}")
        output = result.stdout + result.stderr
        self.assertIn("maybe", output, f"Expected 'maybe' in output, got '{output}'")
        self.assertIn("pass", output, f"Expected 'pass' in output, got '{output}'")
        self.assertIn("warn", output, f"Expected 'warn' in output, got '{output}'")
        self.assertIn("fail", output, f"Expected 'fail' in output, got '{output}'")

    def test_ak5_invalid_severity_value(self):
        report_content = {
            "title": "Test Report",
            "verdict": "pass",
            "findings": [
                {"id": "F1", "title": "Finding 1", "severity": "URGENT"}
            ]
        }
        report_path = self.temp_dir / "invalid_severity.json"
        with open(report_path, "w") as f:
            json.dump(report_content, f)

        result = self._run_module(report_path)

        self.assertEqual(result.returncode, 2, f"Expected exit code 2 for invalid severity, got {result.returncode}. Stderr: {result.stderr}")
        output = result.stdout + result.stderr
        self.assertIn("URGENT", output, f"Expected 'URGENT' in output, got '{output}'")
        self.assertIn("CRITICAL", output, f"Expected 'CRITICAL' in output, got '{output}'")
        self.assertIn("HIGH", output, f"Expected 'HIGH' in output, got '{output}'")
        self.assertIn("MEDIUM", output, f"Expected 'MEDIUM' in output, got '{output}'")
        self.assertIn("LOW", output, f"Expected 'LOW' in output, got '{output}'")
        self.assertIn("INFO", output, f"Expected 'INFO' in output, got '{output}'")
