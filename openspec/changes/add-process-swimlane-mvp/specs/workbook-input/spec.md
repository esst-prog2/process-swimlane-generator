## Purpose

Let process owners maintain a small, fixed Excel workbook and supply its saved task values without exporting to CSV.

## ADDED Requirements

### Requirement: Fixed workbook contract
The generator SHALL accept .xlsx input containing a worksheet named `Process`, literal headers `task_id`, `section`, `task`, `department`, `annual_frequency`, `next_task_id` in A1-F1 respectively, and data beginning at row 2. It SHALL reject missing or misplaced headers and merged cells intersecting Process A-F. It SHALL ignore other worksheets and columns after F, including populated cells and formulas, without validating their content. Formatting-only cells SHALL NOT count as data.

#### Scenario: Supported workbook
- **WHEN** a workbook has the fixed worksheet and all six headers in their required positions
- **THEN** its task rows are read with their original worksheet row numbers

#### Scenario: Missing department header
- **WHEN** D1 is empty or does not contain `department`
- **THEN** validation reports the expected `department` header and its location

#### Scenario: Unsupported layout
- **WHEN** the workbook lacks a worksheet named Process or has merged cells intersecting its A-F input area
- **THEN** validation explains the required Process worksheet and fixed A-F input layout

#### Scenario: Additional worksheets and notes
- **WHEN** a valid Process worksheet is accompanied by other worksheets and populated columns G onward, including formulas with unavailable saved values
- **THEN** only Process A-F supplies task data and the additional content does not cause validation errors or affect the diagram

### Requirement: Literal and cached formula values
The generator SHALL accept literal values and formula cells in all six data columns when usable saved values are available through the workbook reader. It SHALL read those saved calculated values without evaluating formulas. An unavailable or unusable saved value, including an Excel error result, SHALL produce a cell-specific error instructing the user to recalculate and save in Excel. Saved values SHALL also satisfy the ordinary column validation rules. The MVP SHALL NOT require custom XLSX XML/cache inspection or guaranteed distinction of all formula-cache states.

#### Scenario: Saved formula result
- **WHEN** a task description formula has a saved text result
- **THEN** the description uses that text rather than the formula expression

#### Scenario: Missing cache
- **WHEN** a formula cell has no cached calculated result
- **THEN** validation names the cell and asks the user to recalculate and save the workbook in Excel before rerunning

#### Scenario: Formula error
- **WHEN** a formula's cached result is an Excel error such as `#VALUE!`
- **THEN** validation identifies the cell and gives the recalculation and save guidance

#### Scenario: Empty string exposed by the reader
- **WHEN** the workbook reader exposes an empty string for annual_frequency or the final task's next_task_id formula
- **THEN** that result is accepted as blank

#### Scenario: Ambiguous blank formula result
- **WHEN** the workbook reader exposes no saved value for a formula, even if Excel displays a blank result
- **THEN** validation gives the recalculation/save message without requiring custom cache inspection; documentation explains the limitation and using a literal blank for an optional field

### Requirement: Text identifiers
The generator SHALL require task_id and nonblank next_task_id effective values to be text, preserving their exact values without numeric conversion, trimming, or case folding. Numeric literal or cached ID values SHALL be rejected with a message that task IDs must be stored as text.

#### Scenario: Leading zeros and named IDs
- **WHEN** text IDs `001` and `PR-01` occur in the workbook
- **THEN** they remain exactly `001` and `PR-01` for display and reference matching

#### Scenario: Numeric ID despite display formatting
- **WHEN** an ID cell stores the number 1, even if Excel displays it as `001`
- **THEN** validation rejects it and explains that task IDs must be stored as text

#### Scenario: Formula-generated ID
- **WHEN** an ID formula caches the text `001`
- **THEN** the ID is accepted as text, whereas a numeric cached result is rejected

### Requirement: Required values and annual frequency
Every task row SHALL contain nonblank text values for task_id, section, task, and department. Whitespace-only required values SHALL be invalid. Annual frequency SHALL be blank or a finite non-negative number, including decimals and zero; numeric Excel cells and dot-decimal text SHALL be accepted, while booleans, negative numbers, and nonnumeric text SHALL be rejected. A blank value means not provided, whereas zero means zero occurrences per year.

#### Scenario: Optional and fractional frequency
- **WHEN** rows contain blank frequency, 0, and 0.5 respectively
- **THEN** all three are valid and remain distinguishable as absent, zero, and fractional frequency

#### Scenario: Invalid row values
- **WHEN** a row lacks its section or has a negative or nonnumeric annual frequency
- **THEN** validation identifies the offending row and column

### Requirement: Empty rows
The generator SHALL ignore completely empty A-F data rows, including gaps, and validate partially filled rows. It SHALL check formula caches before deciding whether a formula-containing row can be ignored; a formula with missing cache SHALL NOT disappear as an empty row.

#### Scenario: Gap between tasks
- **WHEN** row 3 is empty and valid task rows occur at rows 2 and 4
- **THEN** both tasks are read and diagnostics retain their original row numbers

#### Scenario: Notes-only row
- **WHEN** a row is empty in A-F but has notes or formulas after F
- **THEN** the row is ignored as task input

#### Scenario: Partial row
- **WHEN** a row contains a department but no task ID
- **THEN** validation reports the missing required value instead of silently skipping the row

### Requirement: Reusable synthetic template
The project SHALL provide a reusable .xlsx example/template with the fixed structure and both ID columns formatted as Text. It SHALL contain 12 sequential invented tasks across four departments and SHALL include no confidential company data or code. Documentation SHALL explain adding rows while retaining Text formatting and recalculating/saving formulas.

#### Scenario: Edit and rerun
- **WHEN** a user edits or adds valid process rows in the supplied workbook, saves it, and runs the generator
- **THEN** the workbook can be used directly without CSV export or rebuilding its structure
