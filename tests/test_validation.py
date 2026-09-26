import unittest
from process_swimlane.model import Task, ValidationError
from process_swimlane.validation import validate_process


def task(identifier, successor=None, row=2):
    return Task(row, identifier, "Area", "Task", "Dept", None, successor)


class ValidationTests(unittest.TestCase):
    def test_shuffled(self):
        tasks = [task(str(i), str(i+1) if i < 11 else None, i+2) for i in range(12)]
        self.assertEqual(validate_process(tasks[::-1]), tasks)

    def test_duplicate(self):
        with self.assertRaisesRegex(ValidationError, "row 2"):
            validate_process([task("001"), task("001", row=4)])

    def test_exact_references(self):
        for successor in ("1", "001 ", "pr-01", "001,PR-01"):
            with self.subTest(successor=successor), self.assertRaisesRegex(ValidationError, "F2.*Unknown successor"):
                validate_process([task("start", successor), task("001"), task("PR-01")])

    def test_non_linear(self):
        cases = [
            [task("A", "C"), task("B", "C"), task("C")],
            [task("A"), task("B")],
            [task("A", "A")],
            [task("A", "B"), task("B", "A")],
            [task("A"), task("B", "C"), task("C", "B")],
        ]
        for tasks in cases:
            with self.subTest(tasks=tasks), self.assertRaisesRegex(ValidationError, "linear workflow"):
                validate_process(tasks)

    def test_zero_and_one(self):
        with self.assertRaisesRegex(ValidationError, "At least one"):
            validate_process([])
        single = task("001")
        self.assertEqual(validate_process([single]), [single])
