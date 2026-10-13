"""HTML rendering for reports."""

import html
from collections import Counter


def render_html(report):
    """Render a complete HTML page from a validated report.
    
    Args:
        report: The validated report data
        
    Returns:
        Complete HTML string
    """
    # Escape all text content from the report
    title = html.escape(report["title"], quote=True)
    verdict = html.escape(report["verdict"], quote=True)
    
    # Count findings by severity
    severity_counter = Counter()
    for finding in report["findings"]:
        severity_counter[finding["severity"]] += 1
    
    # Sort findings by severity order
    severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
    sorted_findings = []
    for severity in severity_order:
        for finding in report["findings"]:
            if finding["severity"] == severity:
                sorted_findings.append(finding)
    
    # Build HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: sans-serif;
            line-height: 1.6;
            margin: 2rem;
            max-width: 800px;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #ccc;
            padding-bottom: 0.5rem;
        }}
        .summary {{
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 2rem;
        }}
        .finding {{
            margin-bottom: 1rem;
            padding: 0.5rem;
            border-left: 4px solid #ccc;
        }}
        .CRITICAL {{ border-left-color: #dc3545; }}
        .HIGH {{ border-left-color: #fd7e14; }}
        .MEDIUM {{ border-left-color: #ffc107; }}
        .LOW {{ border-left-color: #20c997; }}
        .INFO {{ border-left-color: #6c757d; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p><strong>Urteil:</strong> {verdict}</p>
    
    <div class="summary">
        <h2>Zusammenfassung</h2>
"""
    
    # Add summary for each severity with findings
    for severity in severity_order:
        if severity_counter[severity] > 0:
            count = severity_counter[severity]
            html_content += f"        <p>{severity}: {count}</p>\n"
    
    html_content += """    </div>
    
    <h2>Befunde</h2>
"""
    
    # Add findings in sorted order
    for finding in sorted_findings:
        finding_id = html.escape(finding["id"], quote=True)
        finding_title = html.escape(finding["title"], quote=True)
        finding_severity = html.escape(finding["severity"], quote=True)
        
        html_content += f"""    <div class="finding {finding_severity}">
        <p><strong>ID:</strong> {finding_id}</p>
        <p><strong>Titel:</strong> {finding_title}</p>
        <p><strong>Schwere:</strong> {finding_severity}</p>
    </div>
"""
    
    html_content += """</body>
</html>"""
    
    return html_content