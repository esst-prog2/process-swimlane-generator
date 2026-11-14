## Why

Column B already identifies workflow phases, but readers must inspect individual task boxes to see them. Section bands make phase transitions and recurring phases visible while following a wide process.

## What Changes

- Group consecutive exact section values in validated successor order, without moving tasks; A, A, B, A produces three bands.
- Add consistent soft section colours, exactly one wrapped heading near the beginning of each contiguous band with consistent left padding, vertical tinting and light dashed transition boundaries in SVG and HTML. Do not repeat or make section headings sticky.
- Keep task section text, arrows, department boundaries and the neutral frozen label column readable.
- Preserve workbook validation, six-column contract, CLI, output numbering and publication behavior; add no dependencies.
- The user manually accepts the latest one-heading refinement, section colours and dashed separators, and frozen department labels. This is user-reported evidence, not automated browser verification.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `swimlane-svg`: Extend section display beyond task text to ordered visual bands in both SVG and its HTML viewer; supersede the earlier prohibition on separate section grouping.

## Impact

Renderer, regression tests, synthetic preview generator and documentation. The viewer consumes the same SVG geometry. Branch dependency: feature/section-bands starts from feature/sticky-department-labels at ef8c72b; the unarchived sticky-department-labels change remains a prerequisite. No branching workflows, editing, hosting, new workbook fields or confidential examples.

## Final Homework 7 and Homework 8 demonstration

The final screenshot-based presentation expands the earlier 12-task viewer demo
to `.qa/section_bands_36.xlsx`: 36 tasks, four departments, five contiguous bands
and 35 directed connections from 001 to 036. It demonstrates `--viewer`, frozen
labels, section tints, one heading per band and dashed boundaries, then rejects
`examples/invalid_loop.xlsx` without publishing a diagram. This supersedes the
earlier repeated-heading presentation; existing workbook and publication scope
is unchanged. The section PR targets the frozen-viewer branch, which targets main.
