"""Command-line entry point."""

import argparse
from pathlib import Path
import sys

from .workbook import read_workbook
from .validation import validate_process
from .render import render_svg
from .output import publish_svg


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate a swimlane SVG from a Process worksheet.")
    parser.add_argument("workbook", help="Path to the .xlsx workbook")
    args = parser.parse_args(argv)
    stage = "read workbook"
    try:
        tasks = read_workbook(args.workbook)
        stage = "validate process"
        ordered = validate_process(tasks)
        stage = "render diagram"
        svg = render_svg(ordered)
        stage = "write diagram"
        destination = publish_svg(svg, Path(args.workbook).stem)
    except Exception as error:
        print(f"Error: could not {stage}: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(ordered)} tasks. Created {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
