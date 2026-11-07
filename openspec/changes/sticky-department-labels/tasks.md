## 1. Viewer and CLI

- [x] 1.1 Build the self-contained viewer from existing SVG geometry; verify wrapped/escaped labels, matching lane bounds and preserved task/connector geometry with regression tests.
- [x] 1.2 Add opt-in --viewer and paired publication with collision retry, rollback and explicit cleanup errors; verify CLI compatibility, naming gaps, either-extension races, render/stage/publish failures and preservation tests.

## 2. Verification and delivery

- [x] 2.1 Run the full existing and new unittest suite and strict OpenSpec validation; record actual results.
- [x] 2.2 Generate a synthetic 45-task process with several departments, unequal lane heights and a long name; attempt available browser verification at left/middle/right and vertical scroll, recording evidence or tooling limitations and exact manual steps.
- [x] 2.3 Update usage and verification evidence, record planning decisions, run git diff --check and commit implementation and verification separately without private inputs, push, merge or branch deletion.

- [x] 2.4 Record the user's latest manual acceptance of frozen department labels in the combined example; retain the distinction from automated browser verification and unrelated unperformed checks.

Frozen department labels are user-accepted in the latest example. Task 2.2 used
the tooling-limitation path; automated browser verification remains unperformed.
See VERIFICATION.md, Homework 7 and Homework 8 final acceptance.
