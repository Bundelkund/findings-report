import subprocess
import sys
import unittest


def run(*args):
    return subprocess.run(
        [sys.executable, "-m", "findings_report", *args],
        capture_output=True,
        text=True,
    )


class TestHelp(unittest.TestCase):
    def test_ak1_help_stdout_und_exit0(self):
        r = run("--help")
        self.assertEqual(r.returncode, 0, "Exit-Code 0 erwartet")
        zeilen = [
            z for z in r.stdout.splitlines()
            if z.startswith("Verwendung:") and "<bericht.json>" in z
        ]
        self.assertTrue(
            zeilen,
            "mindestens eine Zeile mit 'Verwendung:' am Anfang und '<bericht.json>' erwartet",
        )

    def test_ak2_help_stderr_leer(self):
        r = run("--help")
        self.assertEqual(r.stderr, "", "stderr muss leer sein")

    def test_ak3_ohne_argumente(self):
        r = run()
        self.assertEqual(r.returncode, 2, "Exit-Code 2 erwartet")
        zeilen = r.stderr.splitlines()
        self.assertEqual(len(zeilen), 1, "genau eine Zeile auf stderr erwartet")
        self.assertTrue(zeilen[0].startswith("Verwendung:"), "Zeile beginnt mit 'Verwendung:'")
        self.assertIn("<bericht.json>", zeilen[0], "Zeile enthaelt <bericht.json>")


if __name__ == "__main__":
    unittest.main()
