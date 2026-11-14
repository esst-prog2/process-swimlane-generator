## Context

See proposal.md. render_svg receives the validated chain and owns task slots, wrapping and lane geometry. The HTML viewer extracts neutral department lane groups and crops the task half of the same SVG. Its removal of direct root heading text means section headings must be grouped with their bands. The existing workbook, CLI and publisher need no changes.

## Goals / Non-Goals

**Goals:** Add a single renderer-owned section layer and enough header space for complete names. Preserve horizontal task slots, connector routing and viewer alignment.

**Non-Goals:** No sorting by section, independent HTML layout, new input field, configurable theme, JavaScript or dependency.

## Decisions

- Compute contiguous runs in one pass through the ordered tasks. Map exact distinct values in first-appearance order to deterministic pastel HSL colours (golden-angle hue spacing, 55% saturation, 94% lightness); later runs reuse the mapping. Do not hash Python strings or collapse non-adjacent runs. Colours need not match between different diagrams.
- Keep the existing 352px task boxes and 72px gaps. Transition boundaries lie at gap midpoints; tint starts at LEFT and ends at the lane right edge. Draw tints behind tasks/arrows, redraw horizontal lane boundaries above tints, and keep all section elements outside department lane groups so the frozen label SVG remains neutral.
- Render exactly one full heading per contiguous band at its left boundary plus 16px, wrapping at the existing 40 display-unit width. This consistent padding fits even single-task bands. Allocate header height from the longest wrapped heading; shift all lanes down together. Retain existing title/summary above the section header. Do not repeat headings or introduce sticky section headings.
- Use ElementTree for exact section attributes and escaped text, and the existing wrap routine. Group section headings so the HTML viewer retains them. The viewer consumes the SVG without recomputing bands, header height or lane positions.

## Risks / Trade-offs

- Many distinct sections can have visually similar pastels: exact headings and dashed boundaries carry meaning too.
- Very long names enlarge the common header. The single heading scrolls out of view past the band beginning; task section text remains available. This deliberately reduces visual repetition in response to user feedback.
- Font fallback and actual contrast/readability require visual checks; structural tests alone do not prove browser behavior. Record blocked browser verification honestly.

## Migration Plan

No workbook migration or CLI flag is needed. Generate new numbered outputs; preserve existing exports. This branch depends on the frozen viewer branch at ef8c72b. Commit proposal, implementation and evidence separately. Keep both OpenSpec changes unarchived unless separately requested.
