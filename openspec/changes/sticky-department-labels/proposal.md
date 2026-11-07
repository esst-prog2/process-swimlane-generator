## Why

The Homework 5 test of a 45-task process showed that department names disappear during horizontal scrolling. Users need a persistent lane reference while reading wide diagrams.

## What Changes

- Add opt-in `--viewer` publication of a self-contained HTML viewer alongside the existing SVG; the default command stays compatible.
- Keep wrapped department labels fixed horizontally and aligned with unequal-height lanes during both horizontal and vertical scrolling, using existing SVG geometry.
- Publish matching numbered SVG/HTML pairs without replacing existing files, with cleanup and clear diagnostics on handled publication failures.
- Document the intended demo now; record implementation and actual verification separately as they happen.
- Exclude branching, editing, accounts, hosting, external assets, servers, network access, and new runtime dependencies.

## Capabilities

### New Capabilities
- `swimlane-viewer`: Offline HTML viewing with frozen department labels and complete task/connector access.

### Modified Capabilities
- `generator-cli`: Optional viewer generation, matched output numbering, publication cleanup, and clear paths.

## Impact

CLI and output publication, a small HTML renderer consuming existing SVG geometry, regression tests, README and verification evidence. Workbook format, validation, SVG export and its default CLI behavior remain compatible. This is a proposal, not a claim of completed or browser-verified behavior.

## Final demonstration scope and acceptance

The later section-bands change extends the earlier 12-task viewer demonstration
to the screenshot-based Homework 7 and Homework 8 presentation: the synthetic
`.qa/section_bands_36.xlsx` contains 36 tasks, four departments, five section
bands and 35 connections. The combined demo shows frozen labels plus one heading
per band, soft colours and dashed boundaries, and rejection of invalid_loop.xlsx
without a new diagram. Section rendering belongs to the dependent section-bands
change; this viewer's implementation scope remains unchanged. The user manually
accepts frozen labels in the latest combined example. No automated browser
verification, browser version, viewport or zoom is inferred from that report.
