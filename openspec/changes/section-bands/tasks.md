## 1. Shared section rendering

- [x] 1.1 Implement ordered contiguous bands, recurring colours, wrapped repeated headings, shared header sizing, tints and separators in SVG; verify fixed run/boundary expectations, exact text safety and edge cases with regression tests.
- [x] 1.2 Verify HTML retains identical section geometry and neutral frozen labels with unequal lane heights; test task/connection preservation and viewer alignment without changing validation or publication.

## 2. Verification and delivery

- [x] 2.1 Generate a synthetic multi-section example with a wide long-name section, recurrence and unequal lanes; verify both output files and record their paths.
- [x] 2.2 Run all tests, strict OpenSpec validation and git diff --check; record actual outcomes, attempt available browser verification or document limitation and short manual checklist with visual acceptance pending.
- [x] 2.3 Update usage/demo, append decisions and evidence, and commit implementation and verification in logical stages; verify clean Git status without push, merge or branch deletion.

Visual acceptance remains pending. Task 2.2 used its explicit unavailable-browser
path: browser host unavailable, structural checks passed, and exact sample paths
plus manual checks recorded in VERIFICATION.md. The earlier user-reported viewer
verification does not verify the new section bands.
