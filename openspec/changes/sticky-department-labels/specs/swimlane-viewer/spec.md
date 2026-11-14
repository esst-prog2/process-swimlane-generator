## Purpose

Let users read wide process diagrams with a persistent department reference in a portable offline browser viewer.

## ADDED Requirements

### Requirement: Offline frozen department column
The HTML viewer SHALL open directly from Windows File Explorer without a server, network, external assets or additional runtime dependencies. Department labels SHALL remain fixed horizontally in a left column while the task area scrolls, and SHALL stay exactly aligned with their lanes during vertical scrolling, including unequal lane heights. Viewer and export SHALL share layout geometry.

#### Scenario: Wide and tall process
- **WHEN** a synthetic wide process with several departments, unequal lane heights and a long department name is viewed at left, middle and far-right horizontal positions and scrolled vertically
- **THEN** labels remain horizontally fixed and vertically aligned with the matching lanes, and all tasks and connectors including the first and last task are reachable

### Requirement: Safe complete labels
The viewer SHALL wrap full department names and safely display workbook content as text in HTML and SVG without interpreting markup or scripts.

#### Scenario: Special and long text
- **WHEN** workbook fields contain long department names, ampersands, quotes, angle brackets or script-like text
- **THEN** their full text remains present and wrapped without introducing executable markup
