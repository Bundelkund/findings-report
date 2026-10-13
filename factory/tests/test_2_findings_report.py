import unittest
import subprocess
import json
import tempfile
import os
import sys
from pathlib import Path


class TestFindingsReport(unittest.TestCase):
    """Tests for findings_report module."""

    def run_module(self, filepath):
        """Run python -m findings_report <filepath> and return (returncode, stdout, stderr)."""
        result = subprocess.run(
            [sys.executable, "-m", "findings_report", str(filepath)],
            cwd=Path.cwd(),
            capture_output=True,
            text=True
        )
        return result.returncode, result.stdout, result.stderr

    def test_ak1_valid_report(self):
        """AK1: Gültiger Bericht mit zwei Findings → Exit-Code 0 und 'OK: 2 Befunde'."""
        valid_report = {
            "title": "Security Report",
            "verdict": "pass",
            "findings": [
                {"id": 1, "title": "Minor issue", "severity": "LOW"},
                {"id": 2, "title": "Another issue", "severity": "INFO"}
            ]
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(valid_report, f)
            temp_path = f.name
        try:
            returncode, stdout, stderr = self.run_module(temp_path)
            self.assertEqual(returncode, 0, f"Expected exit code 0, got {returncode}. stdout: {stdout}, stderr: {stderr}")
            expected_line = "OK: 2 Befunde\n"
            self.assertEqual(stdout, expected_line, f"Expected stdout '{expected_line.rstrip(chr(10))}', got '{stdout.rstrip(chr(10))}'")
        finally:
            os.unlink(temp_path)

    def test_ak2_file_not_found(self):
        """AK2: Datei existiert nicht → Exit-Code 2 und Dateiname in Meldung."""
        nonexistent = "fehlt_xyz.json"
        returncode, stdout, stderr = self.run_module(nonexistent)
        self.assertEqual(returncode, 2, f"Expected exit code 2, got {returncode}. stdout: {stdout}, stderr: {stderr}")
        combined = stdout + stderr
        self.assertIn(nonexistent, combined, f"Expected filename '{nonexistent}' in output, got: {combined}")

    def test_ak3_invalid_json(self):
        """AK3: Datei ist kein gültiges JSON → Exit-Code 2 und 'kein gültiges JSON' in Meldung."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{kaputt")
            temp_path = f.name
        try:
            returncode, stdout, stderr = self.run_module(temp_path)
            self.assertEqual(returncode, 2, f"Expected exit code 2, got {returncode}. stdout: {stdout}, stderr: {stderr}")
            combined = stdout + stderr
            self.assertIn("kein gültiges JSON", combined, f"Expected 'kein gültiges JSON' in output, got: {combined}")
        finally:
            os.unlink(temp_path)

    def test_ak4_missing_title(self):
        """AK4: Fehlendes Feld 'title' → Exit-Code 2 und Feldname in Meldung."""
        report = {
            "verdict": "pass",
            "findings": [{"id": 1, "title": "Test", "severity": "LOW"}]
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(report, f)
            temp_path = f.name
        try:
            returncode, stdout, stderr = self.run_module(temp_path)
            self.assertEqual(returncode, 2, f"Expected exit code 2, got {returncode}. stdout: {stdout}, stderr: {stderr}")
            combined = stdout + stderr
            self.assertIn("title", combined, f"Expected 'title' in output, got: {combined}")
        finally:
            os.unlink(temp_path)

    def test_ak4_missing_verdict(self):
        """AK4: Fehlendes Feld 'verdict' → Exit-Code 2 und Feldname in Meldung."""
        report = {
            "title": "Report",
            "findings": [{"id": 1, "title": "Test", "severity": "LOW"}]
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(report, f)
            temp_path = f.name
        try:
            returncode, stdout, stderr = self.run_module(temp_path)
            self.assertEqual(returncode, 2, f"Expected exit code 2, got {returncode}. stdout: {stdout}, stderr: {stderr}")
            combined = stdout + stderr
            self.assertIn("verdict", combined, f"Expected 'verdict' in output, got: {combined}")
        finally:
            os.unlink(temp_path)

    def test_ak4_missing_findings(self):
        """AK4: Fehlendes Feld 'findings' → Exit-Code 2 und Feldname in Meldung."""
        report = {
            "title": "Report",
            "verdict": "pass"
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(report, f)
            temp_path = f.name
        try:
            returncode, stdout, stderr = self.run_module(temp_path)
            self.assertEqual(returncode, 2, f"Expected exit code 2, got {returncode}. stdout: {stdout}, stderr: {stderr}")
            combined = stdout + stderr
            self.assertIn("findings", combined, f"Expected 'findings' in output, got: {combined}")
        finally:
            os.unlink(temp_path)

    def test_ak5_invalid_verdict(self):
        """AK5: Ungültiges verdict 'maybe' → Exit-Code 2 und Werte in Meldung."""
        report = {
            "title": "Report",
            "verdict": "maybe",
            "findings": []
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(report, f)
            temp_path = f.name
        try:
            returncode, stdout, stderr = self.run_module(temp_path)
            self.assertEqual(returncode, 2, f"Expected exit code 2, got {returncode}. stdout: {stdout}, stderr: {stderr}")
            combined = stdout + stderr
            self.assertIn("maybe", combined, f"Expected 'maybe' in output, got: {combined}")
            self.assertIn("pass", combined, f"Expected 'pass' in output, got: {combined}")
            self.assertIn("warn", combined, f"Expected 'warn' in output, got: {combined}")
            self.assertIn("fail", combined, f"Expected 'fail' in output, got: {combined}")
        finally:
            os.unlink(temp_path)

    def test_ak5_invalid_severity(self):
        """AK5: Ungültige severity 'HUGE' → Exit-Code 2 und Werte in Meldung."""
        report = {
            "title": "Report",
            "verdict": "pass",
            "findings": [{"id": 1, "title": "Test", "severity": "HUGE"}]
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(report, f)
            temp_path = f.name
        try:
            returncode, stdout, stderr = self.run_module(temp_path)
            self.assertEqual(returncode, 2, f"Expected exit code 2, got {returncode}. stdout: {stdout}, stderr: {stderr}")
            combined = stdout + stderr
            self.assertIn("HUGE", combined, f"Expected 'HUGE' in output, got: {combined}")
            self.assertIn("CRITICAL", combined, f"Expected 'CRITICAL' in output, got: {combined}")
            self.assertIn("HIGH", combined, f"Expected 'HIGH' in output, got: {combined}")
            self.assertIn("MEDIUM", combined, f"Expected 'MEDIUM' in output, got: {combined}")
            self.assertIn("LOW", combined, f"Expected 'LOW' in output, got: {combined}")
            self.assertIn("INFO", combined, f"Expected 'INFO' in output, got: {combined}")
        finally:
            os.unlink(temp_path)
