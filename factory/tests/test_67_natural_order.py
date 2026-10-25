import re
import unittest

from findings_report.render import render_html


def make_page(items):
    findings = [
        {"id": fid, "title": "Titel " + str(n), "severity": sev}
        for n, (fid, sev) in enumerate(items)
    ]
    return render_html({"title": "T", "verdict": "warn", "findings": findings})


def id_order(page, ids):
    found = re.findall(r"<code>([^<]*)</code>", page)
    return [x for x in found if x in ids]


class NaturalOrderTest(unittest.TestCase):
    def test_ak1_natural_numbers(self):
        page = make_page([("F10", "HIGH"), ("F2", "HIGH"), ("F1", "HIGH")])
        self.assertEqual(id_order(page, ["F1", "F2", "F10"]), ["F1", "F2", "F10"],
                         "erwartet F1, F2, F10")

    def test_ak2_case_insensitive(self):
        page = make_page([("F2", "MEDIUM"), ("f1", "MEDIUM")])
        self.assertEqual(id_order(page, ["f1", "F2"]), ["f1", "F2"],
                         "erwartet f1 vor F2")

    def test_ak3_ids_without_digits_last(self):
        page = make_page([("zeta", "LOW"), ("Alpha", "LOW"), ("F3", "LOW")])
        self.assertEqual(id_order(page, ["F3", "Alpha", "zeta"]),
                         ["F3", "Alpha", "zeta"],
                         "erwartet F3, Alpha, zeta")

    def test_ak4_severity_still_first(self):
        page = make_page([("F1", "HIGH"), ("F99", "CRITICAL")])
        self.assertEqual(id_order(page, ["F99", "F1"]), ["F99", "F1"],
                         "erwartet CRITICAL F99 vor HIGH F1")


if __name__ == "__main__":
    unittest.main()
