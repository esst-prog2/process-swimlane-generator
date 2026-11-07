"""Command-line entry point."""

import argparse
from pathlib import Path
import sys

from .workbook import read_workbook
from .validation import validate_process
from .render import render_svg
from .output import publish_svg
from .output import publish_pair
from .viewer import render_viewer


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate a swimlane SVG from a Process worksheet.")
    parser.add_argument("workbook", help="Path to the .xlsx workbook")
    parser.add_argument("--viewer", action="store_true", help="Also create an offline HTML viewer with frozen department labels")
    args = parser.parse_args(argv)
    stage = "read workbook"
    try:
        tasks = read_workbook(args.workbook)
        stage = "validate process"
        ordered = validate_process(tasks)
        stage = "render diagram"
        svg = render_svg(ordered)
        html = render_viewer(svg) if args.viewer else None
        stage = "write diagram"
        if args.viewer:
            destination, viewer = publish_pair(svg, html, Path(args.workbook).stem)
        else:
            destination = publish_svg(svg, Path(args.workbook).stem)
    except Exception as error:
        print(f"Error: could not {stage}: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(ordered)} tasks. Created {destination}")
    if args.viewer:
        print(f"Created {viewer}. Open this HTML file for frozen department labels.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
