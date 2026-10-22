import html
import collections

def render_html(report):
    """Render a report as a self-contained HTML page."""
    title = html.escape(report.get('title', ''), quote=True)
    verdict = html.escape(report.get('verdict', ''), quote=True)
    
    # Count findings by severity
    severity_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
    counter = collections.Counter()
    for finding in report.get('findings', []):
        severity = finding.get('severity', '')
        if severity in severity_order:
            counter[severity] += 1
    
    # Sort findings by severity
    findings = sorted(
        report.get('findings', []),
        key=lambda f: (severity_order.index(f.get('severity', 'INFO')) if f.get('severity') in severity_order else len(severity_order), 
                      report.get('findings', []).index(f))
    )
    
    # Build summary text
    summary_parts = []
    for severity in severity_order:
        if counter[severity] > 0:
            summary_parts.append(f"{severity}: {counter[severity]}")
    
    summary = "; ".join(summary_parts)
    
    # Build findings HTML
    findings_html = []
    for finding in findings:
        finding_id = html.escape(finding.get('id', ''), quote=True)
        finding_title = html.escape(finding.get('title', ''), quote=True)
        finding_severity = html.escape(finding.get('severity', ''), quote=True)
        severity_class = f"badge-{finding_severity.lower()}" if finding_severity else ""
        
        findings_html.append(f"""
        <div class="finding">
            <span class="badge {severity_class}">{finding_severity}</span>
            <span class="finding-title" id="{finding_id}">{finding_title}</span>
        </div>""")
    
    findings_html_str = "\n".join(findings_html)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 1rem;
            max-width: 100%;
            box-sizing: border-box;
            overflow-wrap: anywhere;
        }}
        
        h1 {{
            margin-bottom: 0.5rem;
        }}
        
        .verdict {{
            font-weight: bold;
            margin-bottom: 1rem;
        }}
        
        .summary {{
            margin-bottom: 1.5rem;
        }}
        
        .finding {{
            margin-bottom: 1rem;
            padding: 0.5rem;
            border-left: 3px solid #ccc;
        }}
        
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.875rem;
            font-weight: bold;
            margin-right: 0.5rem;
        }}
        
        .badge-critical {{
            background-color: #b00020;
            color: #ffffff;
        }}
        
        .badge-high {{
            background-color: #fb8c00;
            color: #000000;
        }}
        
        .badge-medium {{
            background-color: #ffd600;
            color: #000000;
        }}
        
        .badge-low {{
            background-color: #555555;
            color: #ffffff;
        }}
        
        .badge-info {{
            background-color: #e0e0e0;
            color: #000000;
        }}
        
        .finding-title {{
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="verdict">Verdict: {verdict}</div>
    <div class="summary">Findings: {html.escape(summary, quote=True)}</div>
    {findings_html_str}
</body>
</html>"""
