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
