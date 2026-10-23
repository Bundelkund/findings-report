import html
import collections

def render_html(report):
    title = html.escape(report.get('title', ''), quote=True)
    verdict = html.escape(report.get('verdict', ''), quote=True)
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
            margin-bottom: 0;
        }}
        .summary {{
            margin-top: 0.5em;
            margin-bottom: 1em;
            font-weight: bold;
            overflow-wrap: anywhere;
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
        .finding {{
            margin-bottom: 1em;
            padding: 10px;
            border-left: 3px solid #ccc;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p class="summary">{html.escape(summary_text, quote=True)}</p>
    <p>Verdict: {verdict}</p>
    <div class="findings">
'''
    
    for finding in sorted_findings:
        finding_id = html.escape(finding.get('id', ''), quote=True)
        finding_title = html.escape(finding.get('title', ''), quote=True)
        finding_severity = html.escape(finding.get('severity', ''), quote=True)
        severity_class = f"badge-{finding_severity.lower()}"
        
        html_content += f'''        <div class="finding" id="{finding_id}">
            <span class="badge {severity_class}">{finding_severity}</span>
            {finding_title}
        </div>
'''
    
    html_content += '''    </div>
</body>
</html>'''
    
    return html_content

def summary_line(findings):
    if not findings:
        return "keine Funde"
    
    severity_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
    counter = collections.Counter()
    
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