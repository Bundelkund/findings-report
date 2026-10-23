import html
from collections import Counter


def render_html(report):
    """Render a report as a complete HTML page."""
    title = html.escape(str(report.get('title', '')), quote=True)
    verdict = html.escape(str(report.get('verdict', '')), quote=True)
    findings = report.get('findings', [])
    
    severity_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
    
    # Sort findings by severity and input order
    def severity_key(finding):
        severity = finding.get('severity', '')
        try:
            return severity_order.index(severity)
        except ValueError:
            return len(severity_order)
    
    sorted_findings = sorted(findings, key=severity_key)
    
    # Generate summary line
    summary_text = summary_line(findings)
    
    html_content = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            max-width: 390px;
            box-sizing: border-box;
        }}
        h1 {{
            margin: 0 0 10px 0;
        }}
        .summary {{
            margin: 0 0 20px 0;
            font-weight: bold;
            overflow-wrap: anywhere;
        }}
        .verdict {{
            margin: 0 0 20px 0;
            font-weight: bold;
        }}
        .finding {{
            margin: 0 0 15px 0;
            padding: 0;
        }}
        .badge {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 8px;
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
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p class="summary">{html.escape(summary_text, quote=True)}</p>
    <p class="verdict">Urteil: {verdict}</p>
    '''
    
    for finding in sorted_findings:
        finding_id = html.escape(str(finding.get('id', '')), quote=True)
        finding_title = html.escape(str(finding.get('title', '')), quote=True)
        severity = finding.get('severity', '')
        badge_class = f"badge badge-{severity.lower()}"
        
        html_content += f'''
    <div class="finding">
        <span class="{badge_class}">{html.escape(severity, quote=True)}</span>
        <strong>{finding_id}</strong>: {finding_title}
    </div>
        '''
    
    html_content += '''
</body>
</html>'''
    
    return html_content


def summary_line(findings):
    """Generate summary line with counts per severity."""
    if not findings:
        return "keine Funde"
    
    severity_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
    counter = Counter()
    
    for finding in findings:
        severity = finding.get('severity')
        if severity in severity_order:
            counter[severity] += 1
    
    parts = []
    for severity in severity_order:
        count = counter.get(severity, 0)
        if count > 0:
            parts.append(f"{count} {severity}")
    
    return ", ".join(parts)