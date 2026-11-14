# HW9 promo page design brief

Audience: analysts and process owners documenting linear workflows in Excel.
Message: “Turn an Excel process into a swimlane diagram.” This is a local
Windows tool, with SVG export and an offline HTML viewer featuring frozen
department labels and section bands.

User direction: simple, mobile-readable, real diagram as the main visual,
with “View sample diagram” and “Try it on Windows” easy to find. The second
link opens the README installation instructions. Use only public synthetic
material, relative local asset links, and the actual 36-task HTML as demo.html.

Assistant design proposals for comparison (not yet selected by the user):

- A / Paper: warm ivory, dark green, a large editorial headline above a wide
  live diagram. A calm document-like introduction followed by output details.
- B / Workbench: dark navy introduction beside a prominent light diagram
  window, cyan accents and compact technical captions. Stack on narrow screens.

Both openings use the same real generated viewer, visible calls to action,
keyboard focus styles and responsive type. The viewer retains its own scrolling;
the surrounding page must fit mobile widths. No external fonts or dependencies.

Implementation: buildless HTML and shared CSS under docs/, suitable for GitHub
Pages. index.html is provisional layout A; alternative.html is layout B.
Reuse the verified fresh-clone synthetic output byte-for-byte as demo.html.
Serve two local previews and pause for selection before finalizing the design.

Tools: Codex shell and file editing; Sites skill local-preview guidance.
No gstack-office-hours or Impeccable tools/skills were found in the session
catalog or inspected local skill folders; proceed with the user's Codex fallback.
