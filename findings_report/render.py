from collections import Counter
from html import escape


SEVERITIES = ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO")


def _ort_html(ort):
    if ort.startswith("https://"):
        return '<a href="' + escape(ort, quote=True) + '">' + escape(ort, quote=True) + '</a>'
    return escape(ort, quote=True)


def summary_line(findings):
    counts = Counter(finding["severity"] for finding in findings)
    parts = [
        f"{counts[severity]} {severity}"
        for severity in SEVERITIES
        if counts[severity] > 0
    ]
    return ", ".join(parts) if parts else "keine Funde"


def render_html(report):
    findings = report["findings"]
    severity_index = {severity: index for index, severity in enumerate(SEVERITIES)}
    sorted_findings = sorted(
        findings, key=lambda finding: severity_index[finding["severity"]]
    )
    title = escape(str(report["title"]), quote=True)
    verdict = escape(str(report["verdict"]), quote=True)
    summary = escape(summary_line(findings), quote=True)
    legacy_summary = ", ".join(
        f"{severity}: {sum(finding['severity'] == severity for finding in findings)}"
        for severity in SEVERITIES
        if any(finding["severity"] == severity for finding in findings)
    )
    items = "\n".join(
        "      <li data-id=\"{finding_id}\"><span class=\"badge badge-{severity_class}\">{severity}</span> "
        "<strong>{finding_title}</strong> <code>{finding_id}</code>{ort}</li>".format(
            severity_class=escape(finding["severity"].lower(), quote=True),
            severity=escape(finding["severity"], quote=True),
            finding_title=escape(str(finding["title"]), quote=True),
            finding_id=escape(str(finding["id"]), quote=True),
            ort=(" <span class=\"ort\">{}</span>".format(_ort_html(finding["ort"]))
                 if "ort" in finding else ""),
        )
        for finding in sorted_findings
    )
    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{ font-family: sans-serif; margin: 1rem; overflow-wrap: anywhere; }}
    .summary {{ overflow-wrap: anywhere; }}
    .badge {{ display: inline-block; padding: 0.15em 0.4em; border-radius: 0.2em; font-weight: bold; }}
    .badge-critical {{ background-color: #b00020; color: #ffffff; }}
    .badge-high {{ background-color: #fb8c00; color: #000000; }}
    .badge-medium {{ background-color: #ffd600; color: #000000; }}
    .badge-low {{ background-color: #555555; color: #ffffff; }}
    .badge-info {{ background-color: #e0e0e0; color: #000000; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p class="summary">{summary}</p>
  <p class="verdict">Urteil: {verdict}</p>
  <p class="legacy-summary">{escape(legacy_summary, quote=True)}</p>
  <ul>
{items}
  </ul>
</body>
</html>
"""
