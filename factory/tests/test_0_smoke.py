"""Smoke test of the skeleton: the package imports and carries a version string.

Not an issue test: own tests of an issue live in factory/tests/test_<issue>_*.py (issue numbers start at 1),
so this file never counts as a branch's own tests and a branch without them stays red in factory-ci.
"""

import re
import unittest

import findings_report


class SmokeTest(unittest.TestCase):
    def test_version_string(self) -> None:
        self.assertRegex(findings_report.__version__, re.compile(r"^\d+\.\d+\.\d+"))


if __name__ == "__main__":
    unittest.main()
