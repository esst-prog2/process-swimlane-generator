# MVP verification

Verified on Windows on 2026-09-26 with Python 3.13.0, openpyxl 3.1.5,
and Microsoft Excel 16.0.

- Full unittest suite after the annual-frequency display follow-up: **32 tests passed**.
- Clean virtual environment: normal `pip install .` and installed
  `process-map --help` passed (in addition to the editable development install).
- Installed CLI demo produced `output/purchase_request_swimlane.svg` with
  **12 task boxes, four department lanes, and 11 directed connections**.
- Second demo run produced `output/purchase_request_swimlane_2.svg`.
- All three invalid examples returned nonzero with terminal diagnostics.
  Byte comparisons confirmed all existing outputs and the source template were
  unchanged; no additional output appeared during invalid runs.
- Collision, numbering gaps, rendering failures, and publication failures are
  covered by automated tests, including temporary-file cleanup.
- The synthetic formula fixture was recalculated and saved in Excel 16.0;
  saved text IDs and numeric results passed reader tests.
- A disposable template copy was opened in Excel, its first description edited,
  and a thirteenth task added. After Excel saved the copy, the generator
  successfully produced `output/excel_edited_swimlane.svg` with 13 tasks.

## Visual verification provenance

The user manually inspected both `.qa/preview_12.svg` and `.qa/preview_40.svg`
and confirmed the overall layout, while subsequently reporting that annual
frequency was not visible. The earlier 12-task Edge inspection confirmed no
clipping or overlapping boxes, correct arrows, and horizontal scrolling; the
user explicitly accepted task 4.4 as manually verified. Automated browser
inspection was blocked by Computer Use policy; no automated browser-verification
claim is made.

## Annual-frequency display follow-up

Inspection found that each original preview had only one nonblank frequency,
displayed as `Per year: 0.5` on task 001; all other preview tasks had no frequency
data. The renderer already preserved numeric zero via an explicit None check.
The label is now `Annual frequency:` to identify the field clearly. Preview data
cycles through 120, 0.5, 0, and blank so all required cases are visible.

Both preview files were regenerated. The 12-task preview has nine frequency
labels; the 40-task preview has 30. Blank values have no label. Tests assert
values within each task group, including zero, and check wrapped label bounds,
box containment within lanes, and separation between task boxes with long
descriptions and long frequency values. All 32 tests and strict OpenSpec
validation passed. The regenerated previews have automated structural/bounds
verification; the earlier manual inspection applies to the previous files.

## Reproduce

Run the installation, tests, and demo commands in README.md. For the combined
CLI acceptance checks, run:

```powershell
.\.venv\Scripts\python.exe tests/acceptance.py
```

This creates two new numbered demo diagrams and checks invalid examples without
deleting existing outputs. `tests/verify_excel_edit.ps1` exercises Excel editing
on a disposable `.qa` copy; it requires Excel and is not part of the normal CLI.
