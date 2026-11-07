## Why

Column B already identifies workflow phases, but readers must inspect individual task boxes to see them. Section bands make phase transitions and recurring phases visible while following a wide process.

## What Changes

- Group consecutive exact section values in validated successor order, without moving tasks; A, A, B, A produces three bands.
- Add consistent soft section colours, exactly one wrapped heading near the beginning of each contiguous band with consistent left padding, vertical tinting and light dashed transition boundaries in SVG and HTML. Do not repeat or make section headings sticky.
- Keep task section text, arrows, department boundaries and the neutral frozen label column readable.
- Preserve workbook validation, six-column contract, CLI, output numbering and publication behavior; add no dependencies.
- The user reports the previous outputs working but requests less heading repetition. The one-heading refinement requires fresh visual verification; tests and visual evidence are recorded separately.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `swimlane-svg`: Extend section display beyond task text to ordered visual bands in both SVG and its HTML viewer; supersede the earlier prohibition on separate section grouping.

## Impact

Renderer, regression tests, synthetic preview generator and documentation. The viewer consumes the same SVG geometry. Branch dependency: feature/section-bands starts from feature/sticky-department-labels at ef8c72b; the unarchived sticky-department-labels change remains a prerequisite. No branching workflows, editing, hosting, new workbook fields or confidential examples.
