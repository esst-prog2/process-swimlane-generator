## Purpose

Present a validated linear process as a readable SVG showing department responsibilities and task sequence.

## ADDED Requirements

### Requirement: Horizontal department lanes
The diagram SHALL contain one horizontal lane for each distinct exact department label. Lanes SHALL be ordered top to bottom by first appearance in the linked process sequence. Every task SHALL appear exactly once in its department's lane, progressing left to right in process order independently of worksheet row order.

#### Scenario: Demo layout
- **WHEN** the valid synthetic process has 12 tasks across four departments
- **THEN** the SVG contains exactly 12 task boxes and four department lanes, ordered by their first occurrence in the linked sequence

### Requirement: Complete task labels
Each task SHALL display its exact task ID, description, and section, plus annual frequency when provided. Section SHALL appear as text inside the task rather than a separate visual grouping. Zero frequency SHALL be displayed and absent frequency SHALL be omitted. Long labels SHALL wrap with sufficient space rather than be truncated.

#### Scenario: Task metadata
- **WHEN** a task has ID `001`, a section, a description, and frequency 0.5
- **THEN** all four values are visible within its task box

#### Scenario: Zero versus absent
- **WHEN** one task has frequency zero and another has blank frequency
- **THEN** zero appears on the first task and no frequency value appears on the second

#### Scenario: Long or special text
- **WHEN** a description contains long text, accented characters, or XML-significant characters
- **THEN** the full readable text is preserved in a valid SVG without overflowing its task box

### Requirement: Sequence arrows
The SVG SHALL connect each task to its successor with a directed arrow, including transitions between department lanes. A process of N tasks SHALL have N minus one connections, with no arrows passing through unrelated task boxes.

#### Scenario: Twelve-task chain
- **WHEN** the 12-task demo is rendered
- **THEN** it has exactly 11 directed connections matching the specified successors

#### Scenario: One task
- **WHEN** a single-task process is rendered
- **THEN** the SVG has one task box and no sequence arrows

### Requirement: Scrollable diagram extent
The SVG SHALL grow to accommodate process length and label content without a single printed-page constraint. Users SHALL be able to view the diagram at native scale and scroll through it in a Windows browser.

#### Scenario: Long process
- **WHEN** a valid process is wider than the browser viewport
- **THEN** the diagram retains all tasks at readable native scale and can be viewed by scrolling, without clipping tasks to a page
