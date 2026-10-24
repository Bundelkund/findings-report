"""Validation of report data structure."""


class ValidationError(Exception):
    """Raised when report data fails validation."""


ALLOWED_VERDICTS = {"pass", "warn", "fail"}
ALLOWED_SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"}


def validate_report(data):
    """Validate report data structure.
    
    Args:
        data: The parsed JSON data to validate
        
    Raises:
        ValidationError: If the data fails validation with a descriptive message
    """
    if not isinstance(data, dict):
        raise ValidationError("Bericht muss ein JSON-Objekt sein")
    
    # Check required fields
    required_fields = ["title", "verdict", "findings"]
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Pflichtfeld fehlt: {field}")
    
    # Validate title
    if not isinstance(data["title"], str) or not data["title"].strip():
        raise ValidationError("title muss nicht-leerer Text sein")
    
    # Validate verdict
    verdict = data["verdict"]
    if verdict not in ALLOWED_VERDICTS:
        allowed = ", ".join(sorted(ALLOWED_VERDICTS))
        raise ValidationError(f"unerlaubter verdict: {verdict} (erlaubt: {allowed})")
    
    # Validate findings
    findings = data["findings"]
    if not isinstance(findings, list):
        raise ValidationError("findings muss eine Liste sein")
    
    for i, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise ValidationError(f"Finding {i} muss ein Objekt sein")
        
        # Check required finding fields
        finding_fields = ["id", "title", "severity"]
        for field in finding_fields:
            if field not in finding:
                raise ValidationError(f"Pflichtfeld fehlt: findings[{i}].{field}")
        
        # Validate finding title
        if not isinstance(finding["title"], str) or not finding["title"].strip():
            raise ValidationError(f"findings[{i}].title muss nicht-leerer Text sein")
        
        # Validate severity
        severity = finding["severity"]
        if severity not in ALLOWED_SEVERITIES:
            allowed = ", ".join(sorted(ALLOWED_SEVERITIES))
            raise ValidationError(f"unerlaubter severity: {severity} (erlaubt: {allowed})")

        if "ort" in finding and (not isinstance(finding["ort"], str) or not finding["ort"].strip()):
            raise ValidationError(f"findings[{i}].ort muss nicht-leerer Text sein")
