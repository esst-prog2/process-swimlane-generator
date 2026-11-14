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

## Section bands (2026-11-07)

This section records the original repeated-heading implementation. The later
one-heading refinement and user feedback are recorded below; its fresh visual
check supersedes the original checklist for newly generated outputs.

Branch `feature/section-bands` starts from the viewer branch at `ef8c72b`, which
records user-reported manual viewer verification. Section proposal: `a1a8948`;
implementation: `497275b`. This feature uses the existing column B and adds no
runtime dependencies. The viewer retains the section geometry emitted by the
SVG renderer; workbook validation, CLI and publication code were not changed.

### Actual checks

- Full unittest suite: **51 tests passed in 10.825 seconds**, exit zero.
  Six new tests cover reversed workbook rows resolving to A, A, B, A; separate
  recurring runs with consistent colours; exact case/space identity; single-task,
  single-section and every-task-transition cases; wrapped repeated long headings;
  markup safety; unchanged task positions and connector paths when only grouping
  changes; background drawing order; and viewer section geometry with neutral
  label groups and unequal lane heights. Existing independent arrow-endpoint,
  workbook, viewer and publication regression checks also passed.
- Installed CLI acceptance (`tests/acceptance.py`) passed: two new SVGs (`_7` and
  `_8`), correct 12-task/four-lane/11-arrow structure, invalid input diagnostics,
  and preservation of inputs and all prior outputs.
- `openspec validate --all --strict`: **six items passed, zero failed**.
- `git diff --check`: passed.
- Generated sample inspected structurally: **36 tasks, 35 connectors, five
  bands, 36 heading instances and four dashed separators**, 15,448 by 1,556
  pixels. Section groups match exactly between SVG and HTML; frozen labels
  contain no section groups. Lane (origin, height) values are Requesting
  (164, 180), Procurement & supplier quality coordination (344, 660), Finance
  (1004, 340), and Receiving (1344, 180).

### Generated synthetic sample

```text
.qa/section_bands_36.xlsx
output/section_bands_36_swimlane.svg
output/section_bands_36_swimlane.html
```

The workbook rows are deliberately reversed. Successor order produces:

| Band | Tasks | Section |
| --- | --- | --- |
| 1 | 001–003 | Intake |
| 2 | 004–029 | `Detailed review & supplier coordination <quality assurance phase>` |
| 3 | 030–032 | Approval |
| 4 | 033–034 | Intake (same colour as band 1) |
| 5 | 035–036 | Closeout |

Reproduce with the command below. Each run selects a fresh synthetic workbook
filename and prints the exact new output paths:

```powershell
.\.venv\Scripts\python.exe tests/section_preview.py
```

Generated workbooks and outputs remain ignored; only the synthetic generation
script is committed. No confidential workplace workbook was read or used.

### Browser status and short manual checklist

Browser discovery during this change again returned **“The browser access host
is unavailable.”** No browser tabs were available. No new browser navigation or
screenshot verification was performed; the earlier native-browser policy stop
was not bypassed. **Section visual acceptance remains pending.** The prior
user-reported viewer verification does not establish correctness of these new
colours, headings, boundaries or the expanded header.

1. Open `output/section_bands_36_swimlane.html` directly in Edge or Chrome at
   100% zoom in an approximately 1200-by-800 window. At the left, check task 001,
   Intake heading, soft tint, readable arrows and neutral department labels.
2. Scroll to the middle of tasks 004–029: confirm the full review heading repeats
   and wraps above the lanes without overlap, and its `<quality assurance phase>`
   text is displayed literally. Check the tall Procurement lane and its boundary.
3. Scroll fully right: check the Approval, recurring Intake and Closeout bands,
   consistent Intake colour, dashed boundaries only at section changes, and
   complete access to task 036 and its incoming arrow.
4. At left, middle and right, scroll vertically: department labels must remain
   fixed horizontally and aligned vertically with the tinted lane boundaries.
   Return to the top to see section headings; they are not vertically sticky.
5. Open the matching SVG and repeat the phase/readability checks. Record browser
   version, tested filename, zoom and pass/fail observations before marking
   section visual acceptance passed.

Very long section names increase header height. Many distinct sections can have
similar pastels, so headings and dashed boundaries remain essential. Tiny
viewports cannot guarantee a full repeated heading at every horizontal offset.

## One heading per section band (2026-11-07)

The user manually checked the previous section-band outputs and reported that
they work, but found a heading above every task visually distracting. This is
user-reported verification of the previous rendering, not a fresh check of this
revision; no browser version or individual checklist results were supplied.

The revised SVG and HTML render exactly one complete, wrapped, escaped heading
per contiguous band, 16 pixels inside its left boundary. Recurring sections
retain separate headings and consistent colours. There are no periodic repeats
or sticky section headings. Existing header height, task labels, band colours,
separators, task order, connectors and frozen department geometry are retained.

Verification performed:

- Full suite: **52 tests passed in 11.295 seconds**, exit zero.
- Regression coverage checks one heading for a long multi-task band, three
  headings for A, A, B, A, consistent left padding and wrapped bounds, escaping,
  and the actual synthetic generator producing five headings/four separators
  in both SVG and HTML.
- Strict OpenSpec validation: **six items passed, zero failed**.
- `git diff --check`: passed.
- The regenerated sample has **36 tasks, 35 connectors, five band headings and
  four separators**. Its SVG and HTML band groups match. Comparison with the
  preserved original sample confirmed unchanged task, connector, lane,
  separator and band-background geometry; the frozen label SVG has no section
  headings.

New files (previous outputs preserved):

```text
.qa/section_bands_36_3.xlsx
output/section_bands_36_3_swimlane.svg
output/section_bands_36_3_swimlane.html
```

The fresh check was pending at refinement delivery; the user's subsequent
acceptance below supersedes that status for the three explicitly confirmed
behaviors. No automated browser verification is claimed. Original checklist:

1. Exactly one heading at each band beginning: Intake 001, review 004, Approval
   030, Intake 033 and Closeout 035. The long review band has no heading repeats
   above tasks 005–029; both Intake bands keep their matching colour.
2. Long/special text wraps completely without clipping, overlap or markup
   interpretation; all headings have the same padding inside their band.
3. Tints, dashed transitions, arrows, task section text and first/last tasks stay
   readable. In HTML, department labels remain neutral, horizontally frozen and
   vertically aligned while scrolling. Section headings scroll normally.

## Homework 7 and Homework 8 final acceptance

On 2026-11-07 the user reports manually inspecting the latest example and
confirms frozen department labels in HTML, section colours and dashed
separators, and exactly one heading per contiguous section band. Those specific
checks are accepted, including the heading refinement in `3cd6727`. No browser
version, viewport, zoom, screenshot capture or automated browser result is
inferred. The user referred to the latest example without supplying a filename;
the latest generated pair recorded above is `section_bands_36_3_swimlane.svg`
and `.html`, but that is not independent evidence of which file was inspected.

The final README demo uses screenshots for presentation and the named synthetic
workbook `.qa/section_bands_36.xlsx`. A read-only workbook inspection confirmed
36 tasks, four exact departments, five contiguous section runs, 35 successor
connections, start 001 and end 036. `examples/invalid_loop.xlsx` exists. No count
or filename correction was needed. `tests/section_preview.py` recreates the
data from source, selecting the base name when absent or the next numbered name
when occupied, and invokes normal paired generation. Generated inputs and
outputs remain ignored and prior files are preserved.

This finalization changes documentation only. The latest relevant test evidence
remains **52 tests passed in 11.295 seconds** for the heading refinement; the
suite was not rerun. Prior installed-CLI acceptance verified loop rejection and
output preservation. Final strict OpenSpec validation and `git diff --check`
passed. Automated browser verification remains unperformed; individual checks
not explicitly confirmed (such as opening a copied HTML alone, File Explorer
association, font fallback, or forced-termination recovery) are not newly marked
passed. No Canvas submission is part of this work.

## HW9 fresh-clone reproduction — 2026-11-14

GitHub main was updated without force from 4187f4e to merge commit
89e4083e79cc3a27d64614727b1fd01d94bf7f9a. No PR was required.
The single --no-ff merge of feature/section-bands includes the frozen viewer
(branch tip ef8c72b), section bands, HW9 setup 936ebb4 and inspection fdf62a1.
The unrelated untracked .Rhistory in the original checkout was preserved.
Remote main was independently confirmed with git ls-remote before cloning.

Fresh Windows clone (no local files copied):
`C:\Users\User\AppData\Local\Temp\hw9-fresh-20261114-89e4083`

Cloned origin main at 89e4083; initial and post-demo git status were clean.
The Python launcher and python command were unavailable on PATH, so the README's
full-path fallback was used: `C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe`.
It reported Python 3.13.0. Creating `.venv` and running
`.\.venv\Scripts\python.exe -m pip install .` succeeded (exit 0), installing
process-swimlane-generator 0.1.0, openpyxl 3.1.5 and et-xmlfile 2.0.0.
`.\.venv\Scripts\process-map.exe --help` displayed the --viewer option.

`.\.venv\Scripts\python.exe tests\section_preview.py` exited 0, recreated
`.qa\section_bands_36.xlsx`, validated 36 tasks and generated:

- `output\section_bands_36_swimlane.svg` (36,293 bytes)
- `output\section_bands_36_swimlane.html` (37,963 bytes)

`.\.venv\Scripts\process-map.exe examples\invalid_loop.xlsx` exited 1:

```text
Error: could not validate process: Process: Not a valid linear workflow: expected one start and one end; found 0 starts and 0 ends (possible loop or disconnected chains).
```

Before/after output file paths and SHA-256 hashes were identical: no output
created or modified by the invalid-loop run. Only the demo SVG and HTML existed.
No full automated regression suite was rerun for this reproduction.

Chrome launch was requested successfully using its installed executable and
the fresh clone's HTML file URL. This is launch evidence, not visual acceptance.
On 2026-11-14, the user reported checking the Chrome example: frozen department
labels work, sections are clearly separated, and the example looks good.
The manual visual check passed for those explicitly reported behaviors.
This is user-reported acceptance of the fresh-clone demo, not automated browser
verification. Exact heading counts, individual arrow checks, browser version,
viewport and zoom were not separately reported.
