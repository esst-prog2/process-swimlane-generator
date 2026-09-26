## Context

See proposal.md for motivation. This is a greenfield repository: README.md describes the initial CSV concept, while the later append-only PLANNING_LOG.md decisions replace CSV with a fixed Excel workbook. There is no application code or existing test suite to migrate. This design is planning only.

## Goals / Non-Goals

**Goals:** Keep workbook interpretation, graph validation, rendering, and publication independently testable. Preserve input values and previous output files. Make a Windows pip installation sufficient to run the generator without automating Excel.

**Non-Goals:** No general graph-layout engine, formula calculation engine, configuration UI, or framework for later project levels. Future scope is listed only in proposal.md.

## Decisions

### 1. Small Python pipeline

Use a packaged CLI with `argparse`, a typed task record (original worksheet row, exact ID, section, description, department, optional frequency, optional successor), and separate reader, validator, renderer, and output modules. Return validated tasks in linked sequence before rendering. This is simpler than a service or interactive application. Use standard-library unittest for automated checks; choose and document a tested Python version when setting up the implementation environment rather than claiming an untested compatibility range now.

### 2. Excel reading and cached formula values

Use openpyxl for the fixed workbook and template, reading the same input snapshot in formula and cached-value modes. Its documented `data_only` option exposes saved values rather than formula expressions: [openpyxl reader documentation](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.reader.excel.html). Never save or recalculate the user's workbook.

Keep cell coordinate, cell type, formula presence, and effective value separate, using openpyxl's normal APIs only. For formula cells in Process A-F, an unavailable saved value (including None), an Excel error value, or an unusable result produces a coordinate-specific recalculation/save message. A usable saved value still passes the normal column rules: a numeric ID result is a text-ID error, not an instruction to convert the number silently. Do not skip a formula-bearing input row before checking its saved values. Do not validate formulas in ignored sheets or columns.

Do not implement custom XLSX XML/cache inspection to distinguish formula-cache states. If the reader exposes an empty string, accept it as blank for annual_frequency or the final next_task_id. If it exposes None instead, report the unavailable saved value even if Excel displays the formula as blank. This replaces the earlier guarantee of distinguishing saved empty strings from missing caches. Document literal blank cells as the workaround for optional fields when a formula's blank result is unavailable through the reader. No Excel COM automation or formula evaluator is required.

### 3. Fixed structure and conservative value handling

The worksheet and header contract is defined in workbook-input. Preserve identifiers without trimming, case folding, or numeric conversion. Empty and whitespace-only required values fail; surrounding whitespace on otherwise nonblank IDs remains significant. A nonblank next_task_id names one exact ID; do not split it on punctuation, because punctuation can be part of an ID. Thus a list-like value that does not equal an existing ID fails as an unknown reference.

Require a worksheet named Process and read only its A-F input area; ignore other worksheets regardless of their order and ignore all columns after F, including notes and formulas. Require literal header labels and reject merged cells intersecting the Process A-F input area. Ignore formatting-only cells. Treat department labels as exact text for lane identity. Accept annual frequency as a finite non-negative Excel numeric value (excluding booleans) or dot-decimal text; blank is absent, zero is present. Decimal commas in a text cell are not parsed; Excel's localized display formatting does not change a stored numeric value. Ignore physically empty A-F rows even when notes exist after F; formula-bearing A-F rows must undergo saved-value and field validation. These rules retain a fixed input table while allowing unrelated workbook content.

### 4. Linear graph validation

Validate structure and cell values before building an ID map. Reject duplicates and unknown references. Compute predecessor counts; require one zero-predecessor start, one empty-successor end, and exactly one predecessor for every other task. Follow successor links while recording visited IDs. Reject revisits and require all tasks to be visited. The one-task case satisfies both start and end conditions. This detects merges, cycles (including disconnected cycles), disconnected chains, and invalid references without depending on row order. Preserve original row numbers in errors.

### 5. Deterministic SVG without an external layout executable

Generate SVG with Python's XML facilities rather than adding Graphviz or a plotting framework. Assign one horizontal slot per task in sequence and one horizontal lane per exact department, ordered by first appearance. Place each task farther right than its predecessor. Route connectors in the gap between adjacent slots so they do not pass through task boxes. Escape XML text through the serializer. Wrap descriptions and other labels; size boxes and lanes from wrapped content rather than truncate text. Use fixed font metrics conservatively and verify visually in a Windows browser. Give the SVG intrinsic dimensions so long diagrams remain scrollable at native scale instead of forcing them onto one page. No extra web viewer is planned.

### 6. Publish only complete, non-overwriting outputs

Resolve `output/` relative to the current working directory and use the input filename stem. Render and check complete SVG bytes before publishing. Try the base filename, then ascending suffixes starting at 2, selecting the first unused filename. Stage bytes in a temporary file in the output directory and publish with a Windows no-replace move; retry the next suffix if another process claims the name. Do not use an overwrite-capable replace operation. Clean staging files on ordinary failures; never delete or modify existing diagrams. Tests must cover collisions, write failures, and preservation of existing file bytes. Crash recovery for orphaned temporary files is not an MVP feature.

### 7. Documentation and examples

Provide `examples/purchase_request.xlsx` as a reusable 12-task, four-department synthetic workbook with both ID columns formatted as Text, plus small invalid workbooks. Document how to extend rows while retaining Text formatting, save/recalculate formulas, install in a Windows virtual environment with pip, run the command, and open the SVG. Update the README's obsolete CSV passages during implementation. No workbook files or application code are created by this proposal.

## Risks / Trade-offs

- Saved formula results can be stale even when present -> document that the generator uses saved values and cannot prove freshness; users recalculate and save in Excel.
- Reader APIs may collapse missing and empty caches -> report unavailable results consistently, document the limitation and literal-blank workaround, and keep tests at the reader API level without custom XML inspection.
- Long labels and many lanes can create large diagrams -> wrap labels, grow dimensions, and visually check long-label and multi-lane examples; no claim of ideal layout at arbitrary scale.
- Text-formatted columns alone cannot prevent numeric values being pasted -> validate stored types and report corrective guidance.
- Windows publication and locked files can fail -> test no-replace behavior on Windows and return a terminal error while preserving previous outputs.

## Migration Plan

No deployed data or application needs migration. Implement and test in a Windows virtual environment, supply the synthetic examples, then document the pip installation and demo. CSV users follow the provided XLSX template; no CSV compatibility layer is planned. Rollback consists of uninstalling the package; generated diagrams and source workbooks remain user files.
