"""Command-line interface for validating reports."""

import json
import sys
from pathlib import Path

from .validate import ValidationError, validate_report


def main(argv):
    """Main entry point for the command-line interface.
    
    Args:
        argv: Command line arguments (excluding program name)
        
    Returns:
        Exit code (0 for success, 2 for validation errors)
    """
    # Configure stdout/stderr for UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    
    if len(argv) != 1:
        print("Verwendung: python -m findings_report <bericht.json>", file=sys.stderr)
        return 2
    
    file_path = Path(argv[0])
    
    try:
        # Check if file exists
        if not file_path.exists():
            print(f"Datei nicht gefunden: {file_path}", file=sys.stderr)
            return 2
        
        # Read and parse JSON
        try:
            content = file_path.read_text(encoding='utf-8')
            data = json.loads(content)
        except json.JSONDecodeError:
            print("kein gültiges JSON", file=sys.stderr)
            return 2
        
        # Validate the report structure
        validate_report(data)
        
        # Success - print exactly one line with the count
        count = len(data["findings"])
        print(f"OK: {count} Befunde")
        return 0
        
    except ValidationError as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))