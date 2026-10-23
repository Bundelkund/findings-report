from collections import Counter
from html import escape


SEVERITIES = ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO")


def summary_line(findings):
    counts = Counter(finding["severity"] for finding in findings)
    parts = [f"{counts[severity]} {severity}" for severity in SEVERITIES if counts[severity] > 0]
    return ", ".join(parts) if parts else "keine Funde"


def render_html(report):
    severity_order = {severity: index for index, severity in enumerate(SEVERITIES)}
    findings = sorted(report["findings"], key=lambda finding: severity_order[finding["severity"]])
    summary = summary_line(report["findings"])
    finding_items = "\n".join(
        f'      <li><span class="badge badge-{escape(finding["severity"].lower(), quote=True)}">'
        f'{escape(finding["severity"], quote=True)}</span> '
        f'<strong>{escape(finding["title"], quote=True)}</strong> '
        f'<code>{escape(finding["id"], quote=True)}</code></li>'
        for finding in findings
    )
    return f'''<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(report["title"], quote=True)}</title>
  <style>
    body {{ font-family: sans-serif; margin: 1rem; overflow-wrap: anywhere; }}
    .summary {{ overflow-wrap: anywhere; }}
    .badge {{ display: inline-block; padding: 0.2em 0.5em; border-radius: 0.25em; font-weight: bold; }}
    .badge-critical {{ background-color: #b00020; color: #ffffff; }}
    .badge-high {{ background-color: #fb8c00; color: #000000; }}
    .badge-medium {{ background-color: #ffd600; color: #000000; }}
    .badge-low {{ background-color: #555555; color: #ffffff; }}
    .badge-info {{ background-color: #e0e0e0; color: #000000; }}
  </style>
</head>
<body>
  <h1>{escape(report["title"], quote=True)}</h1>
  <p class="summary">{escape(summary, quote=True)}</p>
  <p>{escape(report["verdict"], quote=True)}</p>
  <ul>
{finding_items}
  </ul>
</body>
</html>
'''
