## Context

See proposal.md for motivation. render_svg already computes wrapped labels, lane origins and heights, and task/connector geometry. output.py stages bytes and uses Windows no-replace rename; cli.py separates validation, rendering and publication diagnostics.

## Goals / Non-Goals

**Goals:** Reuse the emitted SVG as the geometry source; preserve default output and keep the viewer dependency-free.

**Non-Goals:** No independent HTML lane sizing, JavaScript scroll synchronization, workbook changes or SVG layout redesign.

## Decisions

- Parse the already-rendered SVG with ElementTree. Copy lane rectangles and wrapped text into a narrow label SVG; crop the task SVG viewBox at the existing LEFT boundary. This avoids duplicating layout calculations or refactoring the established renderer.
- Put both native-scale SVGs side by side inside one scroll container. Apply sticky left positioning only to the label column, with an opaque background. Both SVGs share the same vertical origin and height, so vertical scrolling cannot desynchronize them. Replace the SVG page heading with a static HTML heading/instructions.
- Serialize workbook content through XML escaping and use only static HTML/CSS around it. No string interpolation of workbook fields into HTML.
- Add a separate paired publisher to preserve the existing SVG-only path. Stage both complete files before publication, check both destinations, publish with Windows no-replace rename, and roll back only members published by this attempt. On a collision, restore staged bytes and retry the next suffix. On other errors, remove owned outputs and staging and report failure.

## Risks / Trade-offs

- Two flat files cannot be atomically committed as one filesystem transaction. Handled failures roll back; abrupt process termination or power loss between renames can leave one file. Cleanup denial must be explicitly reported rather than hidden as success. No crash-atomic guarantee is claimed.
- Browser sticky behavior needs actual browser verification, not just structural tests. Use synthetic 45-task data with unequal lane heights and a long department name; record left/middle/right and vertical results or exact manual steps if tooling is unavailable.
- Existing font fallback and extreme-label limitations remain; SVG text rendering and wrapping are reused without introducing a second font layout system.

## Migration Plan

Commit proposal/demo target, then implementation and regression tests, then contemporaneous verification and documentation. No migration is required: existing commands and SVG files remain usable. Reverting the feature restores SVG-only behavior without changing saved artifacts.
