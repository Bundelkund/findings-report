"""Command-line interface for validating and rendering reports."""

import json
import sys
from pathlib import Path

from .validate import ValidationError, validate_report
from .render import render_html


USAGE = "Verwendung: python -m findings_report <bericht.json> [<ausgabe.html>]"


def main(argv):
    """Main entry point for the command-line interface.
    
    Args:
        argv: Command line arguments (excluding program name)
        
    Returns:
        Exit code (0 for success, 2 for validation errors)
    """
    if argv == ['--version']:
        from findings_report import __version__
        print(f'findings_report {__version__}')
        return 0

    # Configure stdout/stderr for UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    
    # Handle different argument counts
    if argv == ['--help']:
        print(USAGE)
        return 0

    if len(argv) == 0 or len(argv) > 2:
        print(USAGE, file=sys.stderr)
        return 2
    
    if len(argv) == 1:
        # Single file mode: validate only
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
    
    else:  # len(argv) == 2
        # Two files mode: validate and render
        input_path = Path(argv[0])
        output_path = Path(argv[1])
        
        try:
            # Check if input file exists
            if not input_path.exists():
                print(f"Datei nicht gefunden: {input_path}", file=sys.stderr)
                return 2
            
            # Read and parse JSON
            try:
                content = input_path.read_text(encoding='utf-8')
                data = json.loads(content)
            except json.JSONDecodeError:
                print("kein gültiges JSON", file=sys.stderr)
                return 2
            
            # Validate the report structure
            validate_report(data)
            
            # Render HTML
            html_content = render_html(data)
            
            # Write output file
            output_path.write_text(html_content, encoding='utf-8')
            
            # Success - print exactly one line with output path
            print(f"OK: {output_path}")
            return 0
            
        except ValidationError as e:
            print(str(e), file=sys.stderr)
            return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
