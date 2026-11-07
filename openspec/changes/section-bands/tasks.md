## 1. Shared section rendering

- [x] 1.1 Implement ordered contiguous bands, recurring colours, exactly one wrapped heading per band with consistent left padding, shared header sizing, tints and separators in SVG; verify fixed run/boundary expectations, exact text safety and edge cases with regression tests.
- [x] 1.2 Verify HTML retains identical section geometry and neutral frozen labels with unequal lane heights; test task/connection preservation and viewer alignment without changing validation or publication.

## 2. Verification and delivery

- [x] 2.1 Generate a synthetic multi-section example with a wide long-name section, recurrence and unequal lanes; verify both output files and record their paths.
- [x] 2.2 Run all tests, strict OpenSpec validation and git diff --check; record actual outcomes, attempt available browser verification or document limitation and short manual checklist with visual acceptance pending.
- [x] 2.3 Update usage/demo, append decisions and evidence, and commit implementation and verification in logical stages; verify clean Git status without push, merge or branch deletion.

## 3. One-heading refinement

- [x] 3.1 Verify one heading for a long multi-task band and each recurring run, and five heading groups plus four separators in the 36-task sample, in SVG and HTML.
- [x] 3.2 Run full tests, strict OpenSpec validation and git diff --check; regenerate the synthetic sample, record exact paths and fresh visual-check status, and commit the refinement separately.

- [x] 3.3 Record latest user-reported manual acceptance of one heading per contiguous band, section colours and dashed separators, and frozen viewer labels; finalize the five-sentence screenshot-presentation demo with verified sample counts.

The user manually accepts the latest one-heading rendering, colours, dashed
separators and frozen labels. This supersedes pending status for those specific
checks only. Automated browser verification and unrelated unperformed checks
remain distinct; see VERIFICATION.md for provenance.
