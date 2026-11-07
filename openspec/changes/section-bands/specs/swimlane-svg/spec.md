## MODIFIED Requirements

### Requirement: Complete task labels
Each task SHALL display its exact task ID, description, and section, plus annual frequency when provided. Section SHALL remain as text inside the task in addition to section bands. Zero frequency SHALL be displayed and absent frequency SHALL be omitted. Long labels SHALL wrap with sufficient space rather than be truncated.

#### Scenario: Task metadata
- **WHEN** a task has ID `001`, a section, a description, and frequency 0.5
- **THEN** all four values are visible within its task box

#### Scenario: Zero versus absent
- **WHEN** one task has frequency zero and another has blank frequency
- **THEN** zero appears on the first task and no frequency value appears on the second

#### Scenario: Long or special text
- **WHEN** a description contains long text, accented characters, or XML-significant characters
- **THEN** the full readable text is preserved in a valid SVG without overflowing its task box

## ADDED Requirements

### Requirement: Ordered section bands
Consecutive tasks with exactly equal section values SHALL form one band in validated successor order, never worksheet order. Tasks SHALL NOT be reordered. Each distinct section SHALL have a consistent soft colour within the diagram; nonconsecutive occurrences SHALL remain separate bands using the same colour. Column B and the workbook contract SHALL remain unchanged.

#### Scenario: Recurring phase and shuffled rows
- **WHEN** shuffled workbook rows resolve to sections A, A, B, A
- **THEN** the diagram has three bands spanning tasks 1-2, 3 and 4 in that order, and both A bands use the same colour

#### Scenario: Small and frequently changing processes
- **WHEN** the process has one task, one section across many tasks, or a different section at every task
- **THEN** all tasks and arrows remain accessible with one band per consecutive section run and no spurious transition within a run

### Requirement: Readable section presentation in both outputs
Both standalone SVG and HTML viewer SHALL show full wrapped, safely escaped section headings above bands, subtle vertical task-area tints and light dashed separators between bands. Wide bands SHALL repeat headings at bounded intervals for horizontal scrolling. Task text, arrows and department boundaries SHALL remain readable. Both formats SHALL share section and lane geometry; the viewer SHALL retain frozen, vertically aligned, visually neutral department labels. Colour SHALL NOT be the sole indication of grouping.

#### Scenario: Wide section with long or special text
- **WHEN** a section has a long name with markup-significant characters and spans many tasks
- **THEN** its complete name is escaped and wrapped in repeated headings without overlap with task lanes or neighboring headings, and the matching section text remains in task boxes

#### Scenario: Viewer and export parity
- **WHEN** a diagram with multiple sections and unequal department lane heights is exported and viewed in HTML
- **THEN** band boundaries and headings have the same geometry in both outputs, section colour does not enter the frozen label column, and labels remain aligned while scrolling horizontally and vertically
