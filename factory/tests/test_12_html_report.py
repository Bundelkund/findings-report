import unittest
import subprocess
import sys
import os
import json
from pathlib import Path
import re

class TestHtmlReport(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path('/tmp/findings_report_tests')
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.report_path = self.temp_dir / 'report.json'
        self.output_html_path = self.temp_dir / 'output.html'
        self.invalid_report_path = self.temp_dir / 'invalid_report.json'
        self.non_existent_report_path = self.temp_dir / 'non_existent.json'

    def tearDown(self):
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def _run_tool(self, args, input_file=None):
        cmd = [sys.executable, '-m', 'findings_report'] + args
        if input_file:
            with open(input_file, 'r') as f:
                result = subprocess.run(cmd, capture_output=True, text=True, stdin=f)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def _create_valid_report(self, title="Test Report", verdict="pass", findings=None):
        report_data = {
            "title": title,
            "verdict": verdict,
            "findings": findings if findings is not None else []
        }
        with open(self.report_path, 'w') as f:
            json.dump(report_data, f)

    def _create_invalid_report(self):
        with open(self.invalid_report_path, 'w') as f:
            f.write('{"title": "Invalid", "verdict": "invalid_verdict"}')

    def test_ak1_valid_report_generates_html(self):
        self._create_valid_report()
        result = self._run_tool([str(self.report_path), str(self.output_html_path)])

        self.assertEqual(result.returncode, 0, f"Expected exit code 0, got {result.returncode}. Stderr: {result.stderr}")
        self.assertTrue(self.output_html_path.exists(), "Expected output HTML file to exist.")
        self.assertEqual(result.stdout.strip(), f"OK: {self.output_html_path}", "Expected specific stdout message.")

    def test_ak2_page_contains_title_and_verdict(self):
        test_title = "My Awesome Report"
        test_verdict = "warn"
        self._create_valid_report(title=test_title, verdict=test_verdict)
        self._run_tool([str(self.report_path), str(self.output_html_path)])

        self.assertTrue(self.output_html_path.exists(), "Output HTML file was not created.")
        with open(self.output_html_path, 'r') as f:
            content = f.read()

        self.assertIn(f"<h1>{test_title}</h1>", content, "Expected report title in h1 tag.")
        self.assertIn(test_verdict, content, "Expected report verdict to be present.")

    def test_ak3_findings_sorted_by_severity_and_input_order(self):
        findings_data = [
            {"id": "F003", "title": "Medium Finding 1", "severity": "MEDIUM"},
            {"id": "F001", "title": "Critical Finding 1", "severity": "CRITICAL"},
            {"id": "F005", "title": "Low Finding 1", "severity": "LOW"},
            {"id": "F002", "title": "Critical Finding 2", "severity": "CRITICAL"},
            {"id": "F004", "title": "Medium Finding 2", "severity": "MEDIUM"},
            {"id": "F006", "title": "Info Finding 1", "severity": "INFO"},
            {"id": "F007", "title": "High Finding 1", "severity": "HIGH"}
        ]
        self._create_valid_report(findings=findings_data)
        self._run_tool([str(self.report_path), str(self.output_html_path)])

        self.assertTrue(self.output_html_path.exists(), "Output HTML file was not created.")
        with open(self.output_html_path, 'r') as f:
            content = f.read()

        # Expected order: F001 (CRITICAL), F002 (CRITICAL), F007 (HIGH), F003 (MEDIUM), F004 (MEDIUM), F005 (LOW), F006 (INFO)
        expected_order_ids = ["F001", "F002", "F007", "F003", "F004", "F005", "F006"]
        last_pos = -1
        for finding_id in expected_order_ids:
            current_pos = content.find(finding_id)
            self.assertGreater(current_pos, last_pos, f"Finding {finding_id} is not in the expected order.")
            last_pos = current_pos

    def test_ak4_summary_shows_finding_counts_per_severity(self):
        findings_data = [
            {"id": "F1", "title": "C1", "severity": "CRITICAL"},
            {"id": "F2", "title": "C2", "severity": "CRITICAL"},
            {"id": "F3", "title": "H1", "severity": "HIGH"},
            {"id": "F4", "title": "M1", "severity": "MEDIUM"},
            {"id": "F5", "title": "M2", "severity": "MEDIUM"},
            {"id": "F6", "title": "L1", "severity": "LOW"}
        ]
        self._create_valid_report(findings=findings_data)
        self._run_tool([str(self.report_path), str(self.output_html_path)])

        self.assertTrue(self.output_html_path.exists(), "Output HTML file was not created.")
        with open(self.output_html_path, 'r') as f:
            content = f.read()

        self.assertIn("CRITICAL: 2", content, "Expected summary for CRITICAL findings.")
        self.assertIn("HIGH: 1", content, "Expected summary for HIGH findings.")
        self.assertIn("MEDIUM: 2", content, "Expected summary for MEDIUM findings.")
        self.assertIn("LOW: 1", content, "Expected summary for LOW findings.")
        self.assertNotIn("INFO: 0", content, "Expected no summary for INFO findings if count is 0.")
        self.assertNotIn("INFO: ", content, "Expected no summary for INFO findings if not present.")

    def test_ak5_input_texts_are_html_escaped(self):
        evil_title = "<script>alert(1)</script>"
        evil_finding_title = "XSS <img src=x onerror=alert(1)>"
        findings_data = [
            {"id": "F001", "title": evil_finding_title, "severity": "INFO"}
        ]
        self._create_valid_report(title=evil_title, findings=findings_data)
        result = self._run_tool([str(self.report_path), str(self.output_html_path)])

        self.assertEqual(result.returncode, 0, f"Expected exit code 0, got {result.returncode}. Stderr: {result.stderr}")
        self.assertTrue(self.output_html_path.exists(), "Output HTML file was not created.")
        with open(self.output_html_path, 'r') as f:
            content = f.read()

        self.assertNotIn('<script', content.lower(), "Expected no unescaped <script tag in HTML.")
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', content, "Expected escaped script tag in title.")
        self.assertIn('XSS &lt;img src=x onerror=alert(1)&gt;', content, "Expected escaped img tag in finding title.")

    def test_ak6_template_contains_no_scripts_or_external_resources(self):
        # Report without any addresses or scripts in its text content
        report_data = {
            "title": "Clean Report",
            "verdict": "pass",
            "findings": [
                {"id": "F001", "title": "Simple finding", "severity": "INFO"}
            ]
        }
        with open(self.report_path, 'w') as f:
            json.dump(report_data, f)

        result = self._run_tool([str(self.report_path), str(self.output_html_path)])

        self.assertEqual(result.returncode, 0, f"Expected exit code 0, got {result.returncode}. Stderr: {result.stderr}")
        self.assertTrue(self.output_html_path.exists(), "Output HTML file was not created.")
        with open(self.output_html_path, 'r') as f:
            content = f.read()

        self.assertIn('<style>', content, "Expected a style block in the HTML.")
        self.assertNotIn('<script', content.lower(), "Expected no <script tag in the HTML template.")
        self.assertNotIn('http://', content.lower(), "Expected no http:// addresses in the HTML template.")
        self.assertNotIn('https://', content.lower(), "Expected no https:// addresses in the HTML template.")

    def test_ak7_invalid_report_or_missing_input_file_exit_code_2(self):
        # Test with invalid report
        self._create_invalid_report()
        result_invalid = self._run_tool([str(self.invalid_report_path), str(self.output_html_path)])

        self.assertEqual(result_invalid.returncode, 2, f"Expected exit code 2 for invalid report, got {result_invalid.returncode}. Stderr: {result_invalid.stderr}")
        self.assertFalse(self.output_html_path.exists(), "Expected no output HTML file for invalid report.")

        # Get expected error message from single-file validation
        result_validation_invalid = self._run_tool([str(self.invalid_report_path)])
        expected_error_invalid = result_validation_invalid.stderr.strip()
        self.assertIn(expected_error_invalid, result_invalid.stderr, "Expected same error message as single-file validation for invalid report.")

        # Test with non-existent input file
        result_non_existent = self._run_tool([str(self.non_existent_report_path), str(self.output_html_path)])

        self.assertEqual(result_non_existent.returncode, 2, f"Expected exit code 2 for non-existent report, got {result_non_existent.returncode}. Stderr: {result_non_existent.stderr}")
        self.assertFalse(self.output_html_path.exists(), "Expected no output HTML file for non-existent report.")

        # Get expected error message from single-file validation for non-existent file
        result_validation_non_existent = self._run_tool([str(self.non_existent_report_path)])
        expected_error_non_existent = result_validation_non_existent.stderr.strip()
        self.assertIn(expected_error_non_existent, result_non_existent.stderr, "Expected same error message as single-file validation for non-existent report.")

    def test_ak8_single_file_call_and_argument_handling(self):
        # Test single file call (old behavior)
        self._create_valid_report(findings=[{"id": "F1", "title": "T1", "severity": "INFO"}])
        result_single_file = self._run_tool([str(self.report_path)])

        self.assertEqual(result_single_file.returncode, 0, f"Expected exit code 0 for single file call, got {result_single_file.returncode}. Stderr: {result_single_file.stderr}")
        self.assertEqual(result_single_file.stdout.strip(), "OK: 1 Befunde", "Expected 'OK: <n> Befunde' for single file call.")
        self.assertFalse(self.output_html_path.exists(), "Expected no HTML file created for single file call.")

        # Test no arguments
        result_no_args = self._run_tool([])
        self.assertEqual(result_no_args.returncode, 2, f"Expected exit code 2 for no arguments, got {result_no_args.returncode}. Stderr: {result_no_args.stderr}")
        self.assertIn('python -m findings_report <bericht.json> [<ausgabe.html>]', result_no_args.stderr, "Expected usage message for no arguments.")

        # Test too many arguments
        result_too_many_args = self._run_tool([str(self.report_path), str(self.output_html_path), "extra_arg"])
        self.assertEqual(result_too_many_args.returncode, 2, f"Expected exit code 2 for too many arguments, got {result_too_many_args.returncode}. Stderr: {result_too_many_args.stderr}")
        self.assertIn('python -m findings_report <bericht.json> [<ausgabe.html>]', result_too_many_args.stderr, "Expected usage message for too many arguments.")
