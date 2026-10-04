# generator-cli Specification

## Purpose

Provide a documented Windows command that validates an Excel process and safely publishes a new SVG without replacing previous diagrams.

## Requirements

### Requirement: Windows Python command
The project SHALL document installation using Python and pip on Windows and expose `process-map <workbook.xlsx>`. It SHALL include synthetic valid and invalid examples and a documented tested Python version. A standalone executable SHALL NOT be required.

#### Scenario: Documented demo
- **WHEN** a user follows the Windows installation instructions and runs `process-map examples/purchase_request.xlsx`
- **THEN** a valid example generates an SVG and the terminal reports success and the output path with exit code zero

### Requirement: Terminal-only diagnostics
Validation feedback SHALL be emitted in the terminal, identifying the worksheet row, cell, or task ID where possible. Invalid input SHALL result in a nonzero exit code and no new SVG. File-reading, rendering, and output-writing failures SHALL also report an actionable terminal error and return a nonzero exit code. No separate validation report file SHALL be required.

#### Scenario: Invalid input
- **WHEN** a workbook has a missing department header, numeric task ID, unusable formula cache, or non-linear process
- **THEN** the terminal explains the relevant failure, the command exits nonzero, and no new SVG is published

#### Scenario: File cannot be read
- **WHEN** the workbook is missing, unreadable, or not a valid supported workbook
- **THEN** the command reports the input-file problem without claiming generation succeeded

### Requirement: Numbered non-overwriting output
The generator SHALL create outputs in `output/` relative to the current working directory, using `<input-stem>_swimlane.svg` when available. If occupied, it SHALL try `_swimlane_2.svg`, `_swimlane_3.svg`, and ascending suffixes until the first unused filename is found. Existing diagrams SHALL never be overwritten. A new SVG SHALL be published only after successful validation and rendering.

#### Scenario: First output
- **WHEN** purchase_request.xlsx is valid and no base output exists
- **THEN** the command creates `output/purchase_request_swimlane.svg`, creating the output directory if needed

#### Scenario: Repeated generation
- **WHEN** the base output and suffix 2 already exist
- **THEN** the next successful run creates `purchase_request_swimlane_3.svg` and preserves both previous files byte for byte

#### Scenario: Failed run preserves diagrams
- **WHEN** validation, rendering, or publication fails
- **THEN** the command preserves existing diagrams and leaves no newly published partial SVG

#### Scenario: Filename claimed during generation
- **WHEN** another process creates the chosen filename before publication
- **THEN** the generator selects another unused numbered filename without overwriting the competing file
