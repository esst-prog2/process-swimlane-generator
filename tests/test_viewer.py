from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from xml.etree import ElementTree as ET

from openpyxl import Workbook

from process_swimlane.cli import main
from process_swimlane.model import Task
from process_swimlane.output import publish_pair
from process_swimlane.render import render_svg
from process_swimlane.viewer import render_viewer
from process_swimlane.workbook import HEADERS


class ViewerTests(unittest.TestCase):
    def test_shared_geometry_and_complete_content(self):
        tasks = [
            Task(2, "first", "Area", "Task", "Short", None, "last"),
            Task(3, "last", "Area", "Long " * 100, "A long department name " * 8, None, None),
        ]
        svg = render_svg(tasks)
        original = ET.fromstring(svg)
        html = render_viewer(svg).decode()
        labels, diagram = [ET.fromstring(s) for s in re.findall(r"<svg\b.*?</svg>", html, re.S)]
        expected = original.findall(".//*[@data-kind='lane']")
        self.assertNotEqual(expected[0][0].get("height"), expected[1][0].get("height"))
        for root in (labels, diagram):
            self.assertEqual(root.get("height"), original.get("height"))
            for lane, source in zip(root.findall(".//*[@data-kind='lane']"), expected):
                for key in ("y", "height"):
                    self.assertEqual(lane[0].get(key), source[0].get(key))
        for lane, source in zip(labels.findall(".//*[@data-kind='lane']"), expected):
            self.assertEqual(ET.tostring(lane[1]), ET.tostring(source[1]))
        for kind in ("task", "connection"):
            self.assertEqual([ET.tostring(n) for n in diagram.findall(f".//*[@data-kind='{kind}']")],
                             [ET.tostring(n) for n in original.findall(f".//*[@data-kind='{kind}']")])
        left, top, width, height = map(int, diagram.get("viewBox").split())
        boxes = [n[0] for n in diagram.findall(".//*[@data-kind='task']")]
        self.assertEqual(float(boxes[0].get("x")), left)
        self.assertLess(float(boxes[-1].get("x")) + float(boxes[-1].get("width")), left + width)
        self.assertNotRegex(html, r"<(?:script|link|iframe|img)\b")

    def test_escape_all_workbook_fields(self):
        value = '\" onload=\"alert(1)\"><script>alert(1)</script>& é'
        task = Task(2, value, value, value, value, None, None)
        svg = render_svg([task])
        html = render_viewer(svg).decode()
        self.assertNotIn("<script>", html)
        class Audit(HTMLParser):
            def handle_starttag(parser, tag, attrs):
                self.assertNotEqual(tag, "script")
                self.assertFalse(any(key.startswith("on") for key, _ in attrs))
        Audit().feed(html)
        for source in [svg.decode(), *re.findall(r"<svg\b.*?</svg>", html, re.S)]:
            root = ET.fromstring(source)
            self.assertIn(value, "".join(root.itertext()))
            self.assertFalse(any(n.tag.endswith("script") or "onload" in n.attrib for n in root.iter()))


class PairTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def files(self):
        return {p.name: p.read_bytes() for p in self.directory.iterdir()}

    def test_either_extension_and_numbering_gap(self):
        old = {"x_swimlane.html": b"html", "x_swimlane_2.svg": b"svg", "x_swimlane_4.html": b"later"}
        for name, data in old.items():
            (self.directory / name).write_bytes(data)
        result = publish_pair(b"new svg", b"new html", "x", self.directory)
        self.assertEqual([p.name for p in result], ["x_swimlane_3.svg", "x_swimlane_3.html"])
        self.assertEqual(self.files(), old | {p.name: data for p, data in zip(result, (b"new svg", b"new html"))})

    def test_collision_on_either_rename_preserves_competitor(self):
        rename = os.rename
        for extension in ("svg", "html"):
            with self.subTest(extension=extension), TemporaryDirectory() as directory:
                directory = Path(directory)
                def collide(source, destination):
                    if destination.name == f"x_swimlane.{extension}":
                        destination.write_bytes(b"competitor")
                    rename(source, destination)
                with patch("process_swimlane.output.os.rename", side_effect=collide):
                    result = publish_pair(b"svg", b"html", "x", directory)
                self.assertEqual([p.name for p in result], ["x_swimlane_2.svg", "x_swimlane_2.html"])
                self.assertEqual({p.name: p.read_bytes() for p in directory.iterdir()}, {
                    f"x_swimlane.{extension}": b"competitor", "x_swimlane_2.svg": b"svg", "x_swimlane_2.html": b"html"})

    def test_staging_and_publication_failures_roll_back(self):
        sentinel = self.directory / "previous.svg"
        sentinel.write_bytes(b"previous")
        for operation in ("fsync", "rename"):
            real = getattr(os, operation)
            for failed_call in (1, 2):
                with self.subTest(operation=operation, failed_call=failed_call):
                    calls = 0
                    def fail(*args):
                        nonlocal calls
                        calls += 1
                        if calls == failed_call:
                            raise PermissionError("simulated disk failure")
                        return real(*args)
                    with patch(f"process_swimlane.output.os.{operation}", side_effect=fail):
                        with self.assertRaisesRegex(OSError, "simulated disk failure"):
                            publish_pair(b"svg", b"html", "x", self.directory)
                    self.assertEqual(self.files(), {"previous.svg": b"previous"})

    def test_cleanup_denial_identifies_incomplete_file(self):
        rename, unlink = os.rename, Path.unlink
        def fail_html(source, destination):
            if destination.suffix == ".html":
                raise PermissionError("publication denied")
            rename(source, destination)
        def deny_svg(path, *args, **kwargs):
            if path.name == "x_swimlane.svg":
                raise PermissionError("cleanup denied")
            return unlink(path, *args, **kwargs)
        with patch("process_swimlane.output.os.rename", side_effect=fail_html), patch.object(Path, "unlink", deny_svg):
            with self.assertRaisesRegex(OSError, r"Incomplete output cleanup.*x_swimlane.svg.*cleanup denied"):
                publish_pair(b"svg", b"html", "x", self.directory)
        self.assertEqual(self.files(), {"x_swimlane.svg": b"svg"})


class ViewerCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.input = self.root / "sample.xlsx"
        book = Workbook()
        book.active.title = "Process"
        book.active.append(HEADERS)
        book.active.append(["001", "Area", "Task", "Dept", 0, None])
        book.save(self.input)
        book.close()

    def run_cli(self, *options):
        return subprocess.run([sys.executable, "-m", "process_swimlane.cli", str(self.input), *options], cwd=self.root, capture_output=True, text=True)

    def test_opt_in_and_default_compatibility(self):
        before = self.input.read_bytes()
        result = self.run_cli("--viewer")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("sample_swimlane.svg", result.stdout)
        self.assertIn("sample_swimlane.html", result.stdout)
        self.assertIn("Open this HTML file for frozen department labels", result.stdout)
        output = self.root / "output"
        first = {p.name: p.read_bytes() for p in output.iterdir()}
        self.assertEqual(len(first), 2)
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((output / "sample_swimlane_2.svg").read_bytes(), first["sample_swimlane.svg"])
        self.assertFalse((output / "sample_swimlane_2.html").exists())
        result = self.run_cli("--viewer")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("sample_swimlane_3.html", result.stdout)
        for name, data in first.items():
            self.assertEqual((output / name).read_bytes(), data)
        self.assertEqual(self.input.read_bytes(), before)

    def test_viewer_render_and_publish_failure_diagnostics(self):
        for target, stage in (("render_viewer", "render diagram"), ("publish_pair", "write diagram")):
            with self.subTest(target=target), patch(f"process_swimlane.cli.{target}", side_effect=OSError("simulated failure")), redirect_stderr(StringIO()) as errors, redirect_stdout(StringIO()) as output:
                self.assertEqual(main([str(self.input), "--viewer"]), 1)
                self.assertIn(stage, errors.getvalue())
                self.assertNotIn("Created", output.getvalue())

    def test_invalid_viewer_input_creates_nothing(self):
        self.input.write_bytes(b"invalid workbook")
        result = self.run_cli("--viewer")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Created", result.stdout)
        self.assertFalse((self.root / "output").exists())
