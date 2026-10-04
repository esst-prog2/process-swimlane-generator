## Purpose

Ensure that each accepted task mapping describes exactly one complete linear workflow before any diagram is produced.

## ADDED Requirements

### Requirement: Exact unique task references
Task IDs SHALL be unique. Every nonblank next_task_id SHALL name exactly one existing task using exact text matching. A successor value SHALL be interpreted as one ID, not split into multiple successor IDs.

#### Scenario: Duplicate task ID
- **WHEN** two task rows have the exact same task_id
- **THEN** validation reports the duplicate ID with the relevant rows

#### Scenario: Unknown or inexact successor
- **WHEN** a next_task_id differs from every task ID, including by case, whitespace, or leading zeros
- **THEN** validation reports the referring row or task and the unresolved reference

#### Scenario: Attempted successor list
- **WHEN** next_task_id contains `A,B` and no task has the exact ID `A,B`
- **THEN** validation rejects the unknown single reference instead of treating it as a branch

### Requirement: One complete linear chain
The process SHALL have exactly one starting task, one ending task with a blank successor, no task with multiple predecessors, no loops, and no disconnected tasks. Following successors from the start SHALL visit every task exactly once. The order SHALL be determined by next_task_id rather than worksheet row order.

#### Scenario: Rows out of sequence
- **WHEN** a valid 12-task chain is supplied in shuffled worksheet rows
- **THEN** validation returns the same linked sequence as when the rows were ordered

#### Scenario: Merge
- **WHEN** two tasks point to the same successor
- **THEN** validation rejects the process as non-linear and identifies the involved tasks where possible

#### Scenario: Loop
- **WHEN** a task points to itself or successors form a cycle
- **THEN** validation reports that the input is not a valid linear workflow

#### Scenario: Disconnected process
- **WHEN** rows form multiple chains or a valid chain plus a disconnected cycle
- **THEN** validation rejects the input rather than rendering only the reachable chain

### Requirement: Smallest valid process
The generator SHALL accept one task with a blank successor and SHALL reject a workbook with no tasks.

#### Scenario: Single task
- **WHEN** the only task has valid required fields and no successor
- **THEN** it is both the start and end of a valid process

#### Scenario: No tasks
- **WHEN** the workbook has headers but no nonempty task rows
- **THEN** validation reports that at least one task is required
