# Process Swimlane Generator

A Windows Python command-line tool that converts an Excel task table into a
horizontal department swimlane SVG. The MVP supports one complete linear
process, including a process with just one task.

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

## Run the demo

```powershell
.\.venv\Scripts\process-map.exe examples/purchase_request.xlsx
```

The synthetic example has **12 tasks, four departments, and 11 connections**.
Success prints the output path and returns exit code zero. Open
`output/purchase_request_swimlane.svg` in Edge or another browser. At native
scale, scroll horizontally through the process. Long labels wrap inside task
boxes; the diagram is not limited to one printed page.

Run again to create `purchase_request_swimlane_2.svg`, then `_3.svg`, and so on.
The first available filename is used. The `output/` directory is relative to
the directory from which you run the command. Existing diagrams are never
overwritten. Validation and rendering finish before publication; failed runs
preserve previous diagrams.

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

## Future work only

Other input formats, flexible input layouts, combining multiple process sheets,
branches/gateways/loops, full BPMN, graphical editing, manual layout, automatic
comparison, company integrations, collaboration, accounts, online deployment,
macOS/Linux support, and a standalone executable remain outside the MVP.
No ideal layout is promised for arbitrarily large workflows.
