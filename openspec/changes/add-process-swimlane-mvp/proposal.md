## Why

Process owners need to turn a simple Excel task mapping into a readable department swimlane diagram without manually drawing it. The first release will support one complete linear process, making the result independently useful while keeping implementation and installation small.

## What Changes

- Provide a Windows Python command-line tool installed with pip: `process-map examples/purchase_request.xlsx`.
- Read columns A-F of the required `Process` worksheet with six fixed headers, exact text IDs, optional non-negative annual frequency, and usable saved formula results. Ignore other worksheets and columns after F.
- Use saved formula values exposed by the workbook reader without evaluating formulas or adding custom XLSX cache inspection; report unavailable or unusable results with guidance to recalculate and save in Excel.
- Validate a connected linear workflow independently of worksheet row order; report failures in the terminal without creating a diagram.
- Generate a horizontal SVG with department lanes, left-to-right tasks, task metadata, and sequence arrows; allow scrolling through long diagrams.
- Preserve previous diagrams by creating numbered output filenames after successful validation and rendering.
- Supply a reusable synthetic Excel template/example, invalid examples, tests, and Windows installation and usage documentation.
- Replace the README's earlier CSV plan with the later Excel decisions during implementation. This change currently creates planning artifacts only.

## Capabilities

### New Capabilities

- `workbook-input`: Fixed Excel structure, typed values, saved formula results, and reusable template.
- `linear-workflow-validation`: Required values, exact references, and complete linear-process validation.
- `swimlane-svg`: Deterministic horizontal department layout, metadata, and arrows.
- `generator-cli`: Windows installation, terminal feedback, and non-overwriting SVG output.

### Modified Capabilities

None. The repository contains no existing capability specifications or application implementation.

## Impact

Implementation will add a Python package, CLI entry point, workbook reader, validator, SVG renderer, synthetic workbooks, and tests. No existing application APIs or company systems are affected. Excel input supersedes the earlier CSV decision in the append-only planning log; the README is not being edited in this planning change.

## Non-goals and future work

CSV and other input formats, flexible input layouts within Process A-F, combining process data from multiple worksheets, formula evaluation, custom XLSX/cache inspection, standalone executables, macOS/Linux support, graphical editing, branches/merges/loops/gateways, full BPMN, automated comparison, company integrations, collaboration, accounts, and online deployment are outside this MVP. Additional worksheets and columns after F are allowed but ignored. Later project levels remain future work only: this change creates no requirements, capability specs, or implementation tasks for them. Examples must use invented data and no confidential workplace code or mappings.
