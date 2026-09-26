from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from openpyxl import Workbook
from process_swimlane.cli import main
from process_swimlane.output import publish_svg
from process_swimlane.workbook import HEADERS


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.input = self.root / "sample.xlsx"
        book = Workbook()
        sheet = book.active
        sheet.title = "Process"
        sheet.append(HEADERS)
        sheet.append(["001", "Area", "Task", "Dept", 0, None])
        book.save(self.input)

    def run_cli(self, path):
        return subprocess.run([sys.executable, "-m", "process_swimlane.cli", str(path)], cwd=self.root, capture_output=True, text=True)

    def test_success_and_numbering(self):
        before = self.input.read_bytes()
        for name in ("sample_swimlane.svg", "sample_swimlane_2.svg", "sample_swimlane_3.svg"):
            result = self.run_cli(self.input)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(name, result.stdout)
            self.assertTrue((self.root / "output" / name).exists())
        self.assertEqual(self.input.read_bytes(), before)

    def test_invalid_preserves_output(self):
        self.run_cli(self.input)
        before = {p.name:p.read_bytes() for p in (self.root / "output").iterdir()}
        book = Workbook()
        book.active.title = "Process"
        book.active.append(HEADERS)
        book.active["D1"] = "wrong"
        book.save(self.input)
        result = self.run_cli(self.input)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("D1", result.stderr)
        self.assertIn("department", result.stderr)
        self.assertEqual(before, {p.name:p.read_bytes() for p in (self.root / "output").iterdir()})

    def test_unreadable_and_corrupt(self):
        for name in ("missing.xlsx", "broken.xlsx"):
            path = self.root / name
            if name == "broken.xlsx":
                path.write_text("not a workbook")
            result = self.run_cli(path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("could not read workbook", result.stderr)
            self.assertFalse((self.root / "output").exists())

    def test_render_failure_does_not_publish(self):
        with patch("process_swimlane.cli.render_svg", side_effect=ValueError("render failed")), patch("process_swimlane.cli.publish_svg") as publish, redirect_stderr(StringIO()) as errors:
            self.assertEqual(main([str(self.input)]), 1)
        publish.assert_not_called()
        self.assertIn("render diagram", errors.getvalue())

    def test_write_failure_exit(self):
        with patch("process_swimlane.cli.publish_svg", side_effect=PermissionError("locked")), redirect_stderr(StringIO()) as errors:
            self.assertEqual(main([str(self.input)]), 1)
        self.assertIn("write diagram", errors.getvalue())


class OutputTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name) / "output"

    def test_numbering_and_gap(self):
        self.directory.mkdir()
        (self.directory / "x_swimlane.svg").write_bytes(b"old")
        (self.directory / "x_swimlane_3.svg").write_bytes(b"older")
        result = publish_svg(b"new", "x", self.directory)
        self.assertEqual(result.name, "x_swimlane_2.svg")
        self.assertEqual((self.directory / "x_swimlane.svg").read_bytes(), b"old")
        self.assertEqual((self.directory / "x_swimlane_3.svg").read_bytes(), b"older")

    def test_collision_retry(self):
        rename = os.rename
        def collide(source, destination):
            if destination.name == "x_swimlane.svg":
                destination.write_bytes(b"competitor")
            rename(source, destination)
        with patch("process_swimlane.output.os.rename", side_effect=collide):
            result = publish_svg(b"new", "x", self.directory)
        self.assertEqual(result.name, "x_swimlane_2.svg")
        self.assertEqual((self.directory / "x_swimlane.svg").read_bytes(), b"competitor")

    def test_write_and_move_failures_clean_staging(self):
        for operation in ("fsync", "rename"):
            with self.subTest(operation=operation):
                self.directory.mkdir(exist_ok=True)
                old = self.directory / "x_swimlane.svg"
                old.write_bytes(b"old")
                with patch(f"process_swimlane.output.os.{operation}", side_effect=OSError("disk failure")):
                    with self.assertRaises(OSError):
                        publish_svg(b"new", "x", self.directory)
                self.assertEqual(list(self.directory.iterdir()), [old])
                self.assertEqual(old.read_bytes(), b"old")
