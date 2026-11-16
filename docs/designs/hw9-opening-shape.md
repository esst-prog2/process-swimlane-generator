# HW9 opening: approved shape brief

Date: 2026-11-16
Status: User selected A: phone guide plus link to the full viewer.
Target: docs/index.html and its existing Paper styling.
Visitor mode: Persuade.
Basis: approved copy and purchase-request example from office-hours commit 9a99e13.

- **Job and proof:** Help first-time visitors who document processes in Excel recognize a purchase request and explain the first change of responsibility before opening the full diagram. Preserve the approved headline, explanatory copy, actions, setup requirements, and invented-data label. Use the actual first three tasks from the 12-step, four-department example.
- **Focal moment:** Group 001 (Identify the required supplies) and 002 (Describe quantities and purpose) under Requesting, then visibly connect 002 to 003 under Purchasing (Check the request is complete). Use department labels and an arrow, not colour alone. Explicitly identify this as a simplified reading guide, separate from the generated diagram.
- **Sequence and style:** Approved introduction, purchase-request title, workbook excerpt and handoff guide, then full viewer. On desktop, keep excerpt and guide alongside each other and emphasize the department change. Preserve Paper's ivory background, green palette and serif headline. Keep the 36-task stress test lower on the page.
- **Phone layout (A):** Tighten opening spacing, allow natural headline wrapping, and place the vertical handoff guide before the workbook excerpt. Keep text readable without sideways page scrolling. Show a clear link to the full viewer instead of the embedded viewer on phones; retain the desktop embed and existing workbook/SVG access. The full viewer remains a separately scrollable exploration surface.
- **Acceptance and boundaries:** Check the rendered opening at 320, 375 and 390 pixels wide and at desktop width. Verify readable task/department labels, no horizontal page overflow, usable actions and keyboard focus, and logical reading order. Ask a first-time visitor to identify the process and Requesting-to-Purchasing handoff before opening the viewer. Preserve task data, generated assets and the Windows workflow. No generator redesign, new claims or replacement visual style is included.

## Evidence and remaining work

Impeccable's shape workflow reviewed AGENTS.md, PROCESS.md, the office-hours
follow-up, page HTML, CSS and generated viewer source. The current guide gives
all three steps similar emphasis; the phone source order puts the table before
the guide. The viewer has a fixed 184-pixel department column, restricting the
space available for tasks on narrow screens.

These are source findings, not a rendered-browser acceptance result. This shape
step records the approved plan only. Page implementation, responsive checks
and first-time visitor comprehension testing remain pending. The previously
reported phone-width issue is not yet marked resolved.
