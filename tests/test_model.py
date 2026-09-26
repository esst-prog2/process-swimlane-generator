import unittest
from decimal import Decimal

from process_swimlane.model import Diagnostic, Task, ValidationError


class ModelTests(unittest.TestCase):
    def test_source_and_exact_values(self):
        task = Task(7, "001", "Area", "Task", "Dept", Decimal("0.5"), " PR-01 ")
        self.assertEqual((task.row, task.task_id, task.next_task_id), (7, "001", " PR-01 "))
        error = ValidationError(Diagnostic("Unknown successor", task.row, "F", task.task_id))
        self.assertIn("Process!F7", str(error))
        self.assertIn("'001'", str(error))
