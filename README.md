# Process Swimlane Generator

A Windows Python command-line tool that converts an Excel task table into a
horizontal department swimlane SVG, with an optional offline HTML viewer for
frozen department labels. The MVP supports one complete linear process,
including a process with just one task.

## Install on Windows

Tested with Python 3.13.0, openpyxl 3.1.5, and Excel 16.0 on Windows.
Install Python 3.13 or newer with pip, then open PowerShell in this repository:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install .
.\.venv\Scripts\process-map.exe --help
```

If Python is not on PATH, use its full executable path for the first command.
No environment activation, Graphviz, or Excel automation is required to run the
generator. Excel is used to edit inputs and calculate and save formula results.

## The demo

The demo generates a diagram, opens its HTML viewer, and scrolls right while
department labels remain visible beside their lanes.

```powershell
.\.venv\Scripts\process-map.exe examples/purchase_request.xlsx --viewer
```

The synthetic example has **12 tasks, four departments, and 11 connections**.
Success prints both output paths and returns exit code zero. Open the printed
**HTML** file in Edge or Chrome (double-click it in Windows File Explorer, or
use **Open with**). On a fresh output directory this is
`output/purchase_request_swimlane.html`, alongside the SVG of the same name.
The viewer contains all graphics and styles: no server, network connection,
external assets, or extra runtime dependencies are needed. Scroll horizontally
through tasks and vertically through departments. Long labels wrap; the diagram
is not limited to one printed page. Focus the diagram to scroll with arrow keys.

The viewer is implemented and automated regression tests pass. **Actual browser
scrolling and File Explorer opening have not yet been visually verified** because
browser automation was blocked. See [verification and manual checks](VERIFICATION.md#frozen-department-viewer-2026-11-07)
for the evidence and remaining visual acceptance checks.

Omit `--viewer` for the compatible SVG-only command:

```powershell
.\.venv\Scripts\process-map.exe examples/purchase_request.xlsx
```

Open that `.svg` for the standalone export; frozen labels are an HTML viewer
feature.

Repeated viewer runs use matching `_2.svg` / `_2.html`, then `_3.svg` / `_3.html`,
and so on. The first suffix free in **both formats** is used; an existing SVG or
HTML reserves that suffix for paired generation. SVG-only runs retain their
original SVG-only numbering. The `output/` directory is relative to the directory
from which you run the command. Existing files are never overwritten.

Validation and both renders finish before publication. Handled publication
failures remove newly created members and preserve previous files. If Windows
also denies cleanup, the error identifies leftover files for manual removal.
Two separate files are not a crash-atomic transaction: forced termination or
power loss between publications can leave one member; only terminal success
confirms that the pair was completed.

## Prepare your workbook

Copy `examples/purchase_request.xlsx` as a reusable template. Its data is entirely
invented; no confidential workplace mappings or code are included.

Use a worksheet named **Process** with these literal headers in row 1:

| Column | Header | Cell values |
| --- | --- | --- |
| A | `task_id` | Required unique text ID, e.g. `001` or `PR-01` |
| B | `section` | Required nonblank text, shown inside the task |
| C | `task` | Required nonblank task description |
| D | `department` | Required nonblank text, determining the lane |
| E | `annual_frequency` | Optional finite non-negative number, including decimals and zero |
| F | `next_task_id` | Exact next task ID as text; blank for the final task |

Tasks begin in row 2. Other worksheets and columns after F are ignored, so notes
can remain there. Empty A-F rows are ignored, including gaps; partially filled
rows must be valid. Do not merge cells in A-F or rename/reorder the headers.

The template's A and F columns are formatted as **Text**. When adding or pasting
rows, retain Text formatting and enter IDs as text. Formatting an existing number
as Text does not recover leading zeros: re-enter the original identifier.
Numeric IDs are rejected even if Excel displays 1 as `001`. Matching is exact,
including case and surrounding spaces; no trimming or conversion occurs.
Department labels are exact too, so use consistent spelling.

Frequency accepts Excel numbers or dot-decimal text such as `0.5`. Localized
Excel number display does not change the stored numeric value. Blank means not
provided; zero is displayed as zero occurrences per year. Negatives, booleans,
nonnumeric text, and non-finite values are rejected.

### Formulas

Input formulas use their **saved calculated values**. Recalculate and save in
Excel before running the generator. It does not evaluate formulas, refresh links,
or determine whether saved values are stale. Formula results obey normal column
rules, including text-only IDs.

Unavailable saved values and Excel errors produce a cell-specific message asking
you to recalculate and save. A reader-exposed empty string counts as blank in an
optional cell. Some blank formula results are exposed as no saved value instead
and are reported as unavailable. Use a **literal blank cell** for an optional
field in that case. The MVP does not inspect internal XLSX XML/cache states.

## Validation and diagrams

The successor links determine order independently of worksheet row order.
There must be one start, one end, unique IDs, valid references, and one connected
chain. Branches, merges, loops, and disconnected tasks are invalid. A successor
cell names one exact ID, not a list. One task with no successor is valid; zero
tasks are not.

Department lanes follow first appearance in the linked sequence. Every task
shows its ID, description, section, and frequency when provided.

Errors appear only in the terminal, with row/cell/task context where possible.
Invalid input returns a nonzero exit code and creates no new SVG. Try:

```powershell
.\.venv\Scripts\process-map.exe examples/invalid_missing_department.xlsx
.\.venv\Scripts\process-map.exe examples/invalid_multiple_successors.xlsx
.\.venv\Scripts\process-map.exe examples/invalid_loop.xlsx
```

## Development and verification

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests cover workbook and formula rules, chain validation, SVG structure, CLI
exit codes, numbering, collisions, failure cleanup, and preservation of previous
diagrams and input files. An Excel-saved regression fixture is included; Excel
is not needed to run the suite. Developer scripts in `tests/` rebuild synthetic
examples and verify editing through Excel. See `VERIFICATION.md` for acceptance
results and their provenance.

## Homework 4 spike results

We examined 5 anonymized real workplace processes: **4/5** were faithfully
representable as single linear chains, a pass rate of **80.0%**, with a median
process length of **14 tasks**. Neither issue #3 threshold was crossed
(roughly below 50% passing or a median above 25 tasks), supporting the current
linear MVP's usefulness for these sampled processes.

P03 confirmed that yes/no branching is a real limitation: its flattened workbook
passed the CLI, but its true process structure did not pass. Branching remains
an important future capability. See the [spike evidence](spike/processes.csv)
and [measurement notes](spike/README.md).

## Future work only

Other input formats, flexible input layouts, combining multiple process sheets,
branches/gateways/loops, full BPMN, graphical editing, manual layout, automatic
comparison, company integrations, collaboration, accounts, online deployment,
macOS/Linux support, and a standalone executable remain outside the MVP.
No ideal layout is promised for arbitrarily large workflows.
