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

## Frozen department viewer (2026-11-07)

Implemented on Windows with Python 3.13.0 and openpyxl 3.1.5; no runtime
dependencies added. Proposal commit: `4c4946b`. Implementation: `e5ce7a1`.
Historical results above apply to the earlier MVP, not this viewer.

### Executed checks

- Baseline suite: 36 tests passed in 9.367 seconds.
- Expanded suite: **45 tests passed in 10.952 seconds**, exit code zero.
  Nine new tests cover shared lane bounds and unchanged task/connector geometry,
  full wrapped/escaped labels, HTML markup safety, CLI opt-in/default behavior,
  matching suffixes with gaps, either-extension collisions (including races at
  either rename), both staging and publication failures, rollback, explicit
  cleanup-denial diagnostics, and invalid-input preservation.
- The first expanded run failed one overly broad assertion that rejected
  harmless `onload="..."` label text. The corrected check parses HTML and rejects
  actual event attributes and script elements; the production escaping did not
  need changing.
- Installed `process-map.exe --help` includes `--viewer`. Installed CLI viewer
  demo generated `output/purchase_request_swimlane_3.svg` and
  `output/purchase_request_swimlane_3.html`, preserving existing outputs.
- Existing `tests/acceptance.py` passed: two SVG-only outputs (`_4` and `_5`),
  12 tasks, four lanes, 11 arrows; invalid examples preserved all output files
  and the input workbook.
- `openspec validate --all --strict`: five items passed, zero failed.
- `git diff --check`: passed.
- `tests/viewer_preview.py` generated the synthetic 45-task/four-department
  workbook in ignored `.qa/` and the SVG/HTML pair in ignored `output/`.
  The export measures 19,264 by 1,352 pixels with 44 connectors. Lane origins
  and heights are: Requesting (100, 160), International procurement & supplier
  quality coordination (260, 600), Finance (860, 300), Receiving (1160, 160).
  These are structural measurements, not proof of browser scrolling behavior.

### Browser verification limitation

Browser access discovery reported **“The browser access host is unavailable.”**
Native Chrome selection was then stopped by Computer Use because it could not
determine the current browser URL on Windows confidently enough to enforce
policy. No viewer navigation or screenshot verification occurred. No alternative
UI automation was used after this stop.

Consequently, left/middle/far-right sticky behavior, vertical visual alignment,
final-task visual reachability, and double-click opening from File Explorer are
**pending manual verification**, not passed. Automated geometry and HTML checks
do not establish those browser behaviors. Windows CLI, no-replace collisions and
failure handling were tested on the actual Windows runtime.

### Exact manual verification procedure

1. In PowerShell at the repository root, run:

   ```powershell
   .\.venv\Scripts\python.exe tests/viewer_preview.py
   ```

   This creates `.qa/sticky_departments_45.xlsx` if absent and prints a new,
   collision-safe output pair. The pair already generated in this session is
   `output/sticky_departments_45_swimlane.svg` and
   `output/sticky_departments_45_swimlane.html`. Reruns use numbered names;
   open the exact HTML path printed by that run.

2. In Windows File Explorer, open that HTML with Edge or Chrome. No server is
   started. Use a window around 1200 by 800 pixels at 100% zoom, so both axes
   need scrolling. The HTML can also be copied alone to another local folder
   and opened there to check it has no companion-asset dependency.
3. At the far left, confirm task **001** is fully visible. Note the left edge
   of the department column. Confirm the long procurement name wraps without
   truncation and its background boundaries match the task lane boundaries.
4. Drag the horizontal scrollbar to its midpoint (around tasks **022–024**).
   Confirm the label column has exactly the same horizontal position and each
   visible lane boundary matches across the column seam.
5. Drag fully right. Confirm task **045**, including its right edge and text,
   and the connector from **044** are accessible. Department labels must still
   occupy the same left column. Return left to confirm task 001 remains reachable.
6. At each horizontal position, scroll vertically through the full height.
   Check both the top and bottom boundaries of the tall procurement lane,
   then Finance and Receiving. Labels must move vertically with their lanes
   with no gap or drift across the seam. Scroll back up and repeat.
7. Open the matching SVG separately to confirm standalone export remains
   usable. Record browser version, viewport/zoom, tested output name and the
   result of each check before marking visual acceptance as passed.

Handled pair failures are rolled back; cleanup denial is reported with paths.
Forced process termination or power loss between two renames is not crash-atomic
and has not been fault-injected. No private `spike_workbooks/` input was used.

### User-reported manual verification follow-up (2026-11-07)

The section-grouping request identifies the frozen viewer work as manually
verified. This is user-reported verification of the existing viewer, superseding
the pending overall viewer status recorded above. The user did not provide a
browser version, tested filename, viewport, or individual checklist results;
none are inferred here. Automated browser verification remains blocked as
recorded above. This report does not verify the forthcoming section bands.
