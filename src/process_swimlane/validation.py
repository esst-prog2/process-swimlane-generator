"""Validate and order one complete linear chain."""

from .model import Diagnostic, ValidationError


def validate_process(tasks):
    if not tasks:
        raise ValidationError(Diagnostic("At least one task is required."))
    by_id = {}
    errors = []
    for task in tasks:
        if task.task_id in by_id:
            errors.append(Diagnostic(f"Duplicate task ID; first seen at row {by_id[task.task_id].row}.", task.row, "A", task.task_id))
        else:
            by_id[task.task_id] = task
    if errors:
        raise ValidationError(*errors)
    predecessors = {task_id: [] for task_id in by_id}
    for task in tasks:
        if task.next_task_id is not None:
            if task.next_task_id not in by_id:
                errors.append(Diagnostic(f"Unknown successor {task.next_task_id!r}; a linear workflow requires one exact existing task ID, not a successor list.", task.row, "F", task.task_id))
            else:
                predecessors[task.next_task_id].append(task.task_id)
    if errors:
        raise ValidationError(*errors)
    for task_id, incoming in predecessors.items():
        if len(incoming) > 1:
            task = by_id[task_id]
            errors.append(Diagnostic(f"Not a valid linear workflow: multiple predecessors {incoming!r}.", task.row, "A", task_id))
    starts = [task for task in tasks if not predecessors[task.task_id]]
    ends = [task for task in tasks if task.next_task_id is None]
    if len(starts) != 1 or len(ends) != 1:
        errors.append(Diagnostic(f"Not a valid linear workflow: expected one start and one end; found {len(starts)} starts and {len(ends)} ends (possible loop or disconnected chains)."))
    if errors:
        raise ValidationError(*errors)
    ordered, visited = [], set()
    current = starts[0]
    while current is not None:
        if current.task_id in visited:
            raise ValidationError(Diagnostic("Not a valid linear workflow: loop detected.", current.row, "F", current.task_id))
        visited.add(current.task_id)
        ordered.append(current)
        current = by_id.get(current.next_task_id)
    if len(visited) != len(tasks):
        missing = [task.task_id for task in tasks if task.task_id not in visited]
        raise ValidationError(Diagnostic(f"Not a valid linear workflow: disconnected tasks or cycle {missing!r}."))
    return ordered
