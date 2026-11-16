# HW9 office-hours follow-up

Date: 2026-11-16
Mode: Builder; focused review of an already published and submitted page.
Status: Approach B and proposed copy selected by the user.

## Finding and decision

Árpád's feedback: newcomers encounter a stress test with labels such as
“Synthetic task 001” before they see a recognizable process. The original
opening explains features but gives visitors no familiar story to follow.

The installed gstack-office-hours skill's builder guidance informed the
audience, premise challenge, alternatives and proposed copy. This was a
focused adaptation, not the full startup interview, external research,
cross-model review or visual-mockup workflow. The source page and workbook
were inspected; fetching the published page failed.

- Audience: people who document a straightforward process in Excel and need
  to explain departmental handoffs to colleagues.
- User selected B: explain the example before the viewer, using a compact
  Excel-to-diagram introduction and the purchase-request workbook. Retain the
  36-task synthetic example lower down as a labelled stress test.
- Preserve the selected Paper layout and existing local Windows workflow.
- A (demo/copy swap only) and C (HW9 learning story) were offered but not selected.

## Approved opening copy

**See who does what, from an Excel task list.**

Turn a linear workflow into a diagram that shows each step, the department
responsible, and what happens next. Generate an SVG and an offline HTML
viewer locally on Windows.

Actions: **Follow a purchase request** and **Set up on Windows**.

Setup requires Python 3.13+ and PowerShell. The setup link opens the
installation instructions.

**From a request for supplies to delivery**

Follow a fictional purchase request through Requesting, Purchasing, Finance
and Receiving. See where responsibility changes hands.

**12 steps · 4 departments · Invented example data**

## Implementation and evidence

Reuse the existing generator and examples/purchase_request.xlsx. Show the
first three workbook tasks with selected columns, alongside a simplified
reading guide explicitly distinguished from the generated diagram. Offer
the full viewer, SVG and workbook as relative links. Keep demo.html and
sample.svg unchanged for the stress test.

The CLI validated 12 tasks and generated a new SVG/HTML pair successfully.
The published-directory copies match the generated files byte for byte;
the downloadable workbook matches the source. All local links and fragment
targets resolve, and the source order puts the introduction before the
viewer and the stress test last. git diff --check passed.

Browser rendering and narrow-screen usability have not been verified in
this follow-up. The earlier reported phone-width limitation is not marked
resolved. No push or deployment is part of this commit.

## Next real-world check

Show the revised opening to Árpád or another first-time visitor. Before
they scroll the full viewer, ask them to identify the example process and
the first change of department. Check the same opening at phone width.
Success means they can explain the handoff from Requesting to Purchasing
without needing the stress-test labels explained.
