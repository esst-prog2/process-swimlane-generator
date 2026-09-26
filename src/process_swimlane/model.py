"""Source-aware records and user-facing errors."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Task:
    row: int
    task_id: str
    section: str
    description: str
    department: str
    annual_frequency: Decimal | None
    next_task_id: str | None


@dataclass(frozen=True)
class Diagnostic:
    message: str
    row: int | None = None
    column: str | None = None
    task_id: str | None = None

    def __str__(self):
        location = "Process"
        if self.row is not None:
            location += f"!{self.column}{self.row}" if self.column else f" row {self.row}"
        if self.task_id is not None:
            location += f" (task {self.task_id!r})"
        return f"{location}: {self.message}"


class ValidationError(ValueError):
    def __init__(self, *diagnostics: Diagnostic):
        self.diagnostics = diagnostics
        super().__init__("\n".join(map(str, diagnostics)))
