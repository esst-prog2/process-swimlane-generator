## 1. Package and test foundation

- [x] 1.1 Create the Python package and `process-map` entry point with openpyxl as the workbook dependency; verify installation and `process-map --help` in a clean Windows virtual environment and record the tested Python version.
- [x] 1.2 Define task records retaining original rows and structured diagnostics; verify unit tests preserve exact IDs and source coordinates through the processing pipeline.

## 2. Workbook input

- [x] 2.1 Implement selection of Process A-F, fixed-header checks, and empty-row handling; verify missing Process, missing/misplaced headers, and merged input cells fail while additional worksheets, populated columns after F, and notes-only rows are ignored; also verify formatting-only cells, row gaps, and partially filled rows.
- [x] 2.2 Implement saved formula-value reading from one input snapshot using normal workbook-reader APIs only; verify usable text/numeric results pass, unavailable results and Excel errors produce recalculation/save guidance, exposed empty strings follow optional-field rules, and input formula rows are not silently skipped. Verify formulas in ignored sheets/columns are not validated; do not add custom XLSX XML/cache inspection.
- [x] 2.3 Implement text-ID and field-value validation; verify numeric literal/formula IDs fail with corrective guidance, leading zeros and exact text survive, required text is nonblank, and annual frequency accepts blank/zero/non-negative decimals while rejecting booleans, negatives, non-finite values, and invalid text.
- [x] 2.4 Verify saved-value reading against a synthetic workbook recalculated and saved in Excel; retain a documented regression fixture, confirm unavailable values produce clear errors without formula evaluation, and document how reader-exposed blank results are handled without trying to distinguish every cache state.

## 3. Linear workflow validation

- [x] 3.1 Implement duplicate-ID and exact successor checks; verify duplicate rows, case/whitespace/leading-zero mismatches, missing references, and list-like successor values produce useful diagnostics.
- [x] 3.2 Implement start/end, predecessor, cycle, and full-reachability validation; verify valid shuffled rows yield the same sequence and merges, multiple chains, self-loops, full cycles, and a disconnected cycle fail.
- [x] 3.3 Verify boundary behavior with an empty workbook and a single valid task: no tasks fail and a single task with no successor succeeds.

## 4. SVG rendering

- [x] 4.1 Implement deterministic horizontal lanes and left-to-right task placement; verify the 12-task/four-department case, department first-occurrence order, and invariance to worksheet row order.
- [x] 4.2 Add task metadata, wrapping, XML escaping, and dimensions that grow with content; verify exact IDs, section labels, zero versus absent frequency, accented characters, special XML text, and long descriptions remain complete. Follow-up verified explicit Annual frequency labels for positive/fractional/zero values, omission for blank values, and wrapping/box/lane bounds; regenerated both 12-task and 40-task previews with all frequency cases.
- [x] 4.3 Route directed successor arrows between slots; verify 11 connections for 12 tasks, zero for one task, and connections across lanes that do not intersect unrelated task boxes.
- [x] 4.4 Visually inspect the demo and a longer synthetic process in a Windows browser at native scale; verify readable labels, no clipping/overlap, and scrolling beyond one viewport, recording the checked examples.

## 5. CLI and safe output

- [x] 5.1 Connect input, validation, and rendering with terminal diagnostics and exit codes; verify subprocess tests report row/cell/task context where available, success reports the output path, and invalid or unreadable input returns nonzero without a new SVG.
- [x] 5.2 Implement output-directory creation and numbered publication after successful rendering; verify base, _2, _3, and filename-gap cases and confirm existing diagrams remain byte-identical.
- [x] 5.3 Implement staging cleanup and no-replace publication on Windows; verify simulated validation/render/write failures leave no partial published SVG and a destination collision retries without overwriting.

## 6. Examples, documentation, and end-to-end acceptance

- [x] 6.1 Create the reusable synthetic `examples/purchase_request.xlsx` with 12 linked tasks, four departments, all six headers, and Text-formatted ID columns; verify template structure and the edit/add/save/rerun workflow in Excel without CSV export.
- [x] 6.2 Add small synthetic invalid .xlsx examples for a missing department header, attempted multiple successors, and a loop; verify each is rejected with terminal feedback and no output.
- [x] 6.3 Update README.md to reflect the superseding Excel decisions and document Windows Python/pip installation, the Process A-F contract, ignored sheets/extra columns, text IDs, saved formula values and ambiguous-blank limitation/workaround, output numbering, and browser viewing; verify the documented commands in a clean environment and keep later levels described only as future work.
- [x] 6.4 Run the full unit and integration suite plus the documented demo on Windows; confirm 12 tasks, four lanes, 11 arrows, a second numbered output, unchanged previous diagrams after an invalid run, and no changes to input workbook bytes.
