import subprocess
import sys
import unittest
from pathlib import Path


class VersionTest(unittest.TestCase):
    def test_ak1_version_ausgabe(self):
        r = subprocess.run(
            [sys.executable, "-c",
             "import findings_report; print(findings_report.__version__)"],
            capture_output=True, text=True, cwd=str(Path.cwd()),
        )
        self.assertEqual(r.returncode, 0, "Exit-Code 0 erwartet: " + r.stderr)
        self.assertEqual(r.stdout.strip(), "0.1.0", "Version 0.1.0 erwartet")

    def test_ak2_version_ist_str(self):
        import findings_report
        self.assertIsInstance(findings_report.__version__, str,
                              "__version__ muss ein str sein")


if __name__ == "__main__":
    unittest.main()
