from dataclasses import replace
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from xml.etree import ElementTree as ET

from openpyxl import Workbook

from process_swimlane.model import Task
from process_swimlane.render import render_svg, section_runs
from process_swimlane.validation import validate_process
from process_swimlane.viewer import render_viewer
from process_swimlane.workbook import read_workbook, HEADERS


def chain(sections):
    return [Task(i+2, str(i+1), section, "Task", "Dept", None,
                 str(i+2) if i+1 < len(sections) else None)
            for i, section in enumerate(sections)]


def nodes(root, kind):
    return root.findall(f".//*[@data-kind='{kind}']")


class SectionTests(unittest.TestCase):
    def test_shuffled_workbook_uses_linked_runs_and_recurring_colour(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "sections.xlsx"
            book = Workbook()
            book.active.title = "Process"
            book.active.append(HEADERS)
            for row in [("3", "B", "Task", "Dept", None, "4"),
                        ("1", "A", "Task", "Dept", None, "2"),
                        ("4", "A", "Task", "Dept", None, None),
                        ("2", "A", "Task", "Dept", None, "3")]:
                book.active.append(row)
            book.save(path)
            book.close()
            tasks = validate_process(read_workbook(path))
        self.assertEqual(section_runs(tasks), [("A", 0, 2), ("B", 2, 3), ("A", 3, 4)])
        root = ET.fromstring(render_svg(tasks))
        bands = nodes(root, "section-band")
        self.assertEqual([(b.get("data-section"), b.get("data-first"), b.get("data-last")) for b in bands],
                         [("A", "1", "2"), ("B", "3", "3"), ("A", "4", "4")])
        self.assertEqual(bands[0][0].get("fill"), bands[2][0].get("fill"))
        self.assertEqual(len(nodes(root, "section-heading")), 3)
        self.assertEqual([len(nodes(band, "section-heading")) for band in bands], [1, 1, 1])
        self.assertNotEqual(bands[0][0].get("fill"), bands[1][0].get("fill"))
        self.assertEqual([t.get("data-id") for t in nodes(root, "task")], ["1", "2", "3", "4"])
        # Independent literal positions: 184px left, 352px boxes, 72px gaps.
        self.assertEqual([float(b[0].get("x")) for b in bands], [184, 996, 1420])
        self.assertEqual([float(b[0].get("width")) for b in bands], [812, 424, 444])
        self.assertEqual([float(s.get("x1")) for s in nodes(root, "section-separator")], [996, 1420])

    def test_exact_identity_and_edge_cases(self):
        for sections, expected in [(["A"], 1), (["A"] * 20, 1),
                                   (["A", "a", " A", "A ", "A"], 5),
                                   ([str(i) for i in range(20)], 20)]:
            with self.subTest(sections=sections):
                root = ET.fromstring(render_svg(chain(sections)))
                self.assertEqual(len(nodes(root, "section-band")), expected)
                self.assertEqual(len(nodes(root, "section-heading")), expected)
                self.assertEqual(len(nodes(root, "section-separator")), expected-1)
                self.assertEqual(len(nodes(root, "connection")), len(sections)-1)
                colours = {}
                for band in nodes(root, "section-band"):
                    section, colour = band.get("data-section"), band[0].get("fill")
                    self.assertEqual(colours.setdefault(section, colour), colour)
                self.assertEqual(len(set(colours.values())), len(colours))

    def test_long_wide_band_has_one_complete_heading_and_fits(self):
        name = "Long phase <&> " * 30
        root = ET.fromstring(render_svg(chain([name] * 12 + ["Finish"])))
        bands = nodes(root, "section-band")
        headings = nodes(bands[0], "section-heading")
        self.assertEqual(len(headings), 1)
        self.assertEqual(float(headings[0][0].get("x")), 200)
        lane_top = float(nodes(root, "lane")[0][0].get("y"))
        for band in bands:
            right = float(band[0].get("x")) + float(band[0].get("width"))
            for heading in nodes(band, "section-heading"):
                self.assertEqual(float(heading[0].get("x")), float(band[0].get("x")) + 16)
                self.assertEqual("".join(heading.itertext()), band.get("data-section"))
                for span in heading[0]:
                    self.assertLess(float(span.get("y")) + 4, lane_top)
                    self.assertLessEqual(float(span.get("x")) + len(span.text or "") * 8, right)

    def test_36_task_sample_has_five_headings_and_four_separators(self):
        script = Path(__file__).with_name("section_preview.py")
        with TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(script.resolve())], cwd=directory,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = Path(directory) / "output"
            svg = ET.fromstring((output / "section_bands_36_swimlane.svg").read_bytes())
            html = (output / "section_bands_36_swimlane.html").read_text(encoding="utf-8")
        label_svg, diagram = [ET.fromstring(s) for s in re.findall(r"<svg\b.*?</svg>", html, re.S)]
        self.assertEqual(nodes(label_svg, "section-heading"), [])
        for root in (svg, diagram):
            self.assertEqual(len(nodes(root, "task")), 36)
            self.assertEqual(len(nodes(root, "connection")), 35)
            self.assertEqual(len(nodes(root, "section-heading")), 5)
            self.assertEqual(len(nodes(root, "section-separator")), 4)
            bands = nodes(root, "section-band")
            self.assertEqual([len(nodes(b, "section-heading")) for b in bands], [1] * 5)
            self.assertEqual([b.get("data-first") for b in bands], ["001", "004", "030", "033", "035"])
            self.assertEqual(bands[0][0].get("fill"), bands[3][0].get("fill"))

    def test_markup_safe_in_both_formats(self):
        name = '\" onload=\"bad()\"><script>bad()</script>& É漢'
        svg = render_svg(chain([name, "Other", name]))
        html = render_viewer(svg).decode()
        class Audit(HTMLParser):
            def handle_starttag(parser, tag, attrs):
                self.assertNotEqual(tag, "script")
                self.assertFalse(any(key.startswith("on") for key, _ in attrs))
        Audit().feed(html)
        for source in [svg.decode(), *re.findall(r"<svg\b.*?</svg>", html, re.S)[1:]]:
            root = ET.fromstring(source)
            self.assertEqual(nodes(root, "section-band")[0].get("data-section"), name)
            self.assertEqual("".join(nodes(root, "section-heading")[0].itertext()), name)
            self.assertIn("Section: " + name, "".join(nodes(root, "task")[0].itertext()))

    def test_viewer_geometry_and_neutral_label_column(self):
        tasks = chain(["A", "A", "B", "A"])
        tasks[1] = replace(tasks[1], department="Long department name " * 5, description="detail " * 100)
        svg = render_svg(tasks)
        root = ET.fromstring(svg)
        labels, diagram = [ET.fromstring(s) for s in re.findall(r"<svg\b.*?</svg>", render_viewer(svg).decode(), re.S)]
        for kind in ("section-band", "section-heading", "section-separator", "lane-boundaries", "task", "connection"):
            self.assertEqual([ET.tostring(n) for n in nodes(root, kind)], [ET.tostring(n) for n in nodes(diagram, kind)])
            self.assertEqual(nodes(labels, kind), [])
        self.assertGreater(len({n[0].get("height") for n in nodes(root, "lane")}), 1)
        for original, label, lane in zip(nodes(root, "lane"), nodes(labels, "lane"), nodes(diagram, "lane")):
            for key in ("y", "height"):
                self.assertEqual(original[0].get(key), label[0].get(key))
                self.assertEqual(original[0].get(key), lane[0].get(key))
            self.assertIn(label[0].get("fill"), ("#f0f5fa", "#f8fafc"))
        self.assertEqual(labels.get("height"), diagram.get("height"))
        for band in nodes(root, "section-band"):
            self.assertGreaterEqual(float(band[0].get("x")), 184)

    def test_section_changes_do_not_change_tasks_or_arrows(self):
        # Equal-length section names preserve label wrapping; only bands differ.
        uniform = ET.fromstring(render_svg(chain(["A", "A", "A", "A"])))
        grouped = ET.fromstring(render_svg(chain(["A", "A", "B", "A"])))
        self.assertEqual([ET.tostring(n) for n in nodes(uniform, "connection")],
                         [ET.tostring(n) for n in nodes(grouped, "connection")])
        self.assertEqual([ET.tostring(n[0]) for n in nodes(uniform, "task")],
                         [ET.tostring(n[0]) for n in nodes(grouped, "task")])
        self.assertEqual([(n.get("data-source"), n.get("data-target")) for n in nodes(grouped, "connection")],
                         [("1", "2"), ("2", "3"), ("3", "4")])
        # All new background elements precede arrows and opaque task boxes.
        children = list(grouped)
        last_background = max(children.index(n) for n in nodes(grouped, "section-band") + nodes(grouped, "lane-boundaries"))
        self.assertLess(last_background, min(children.index(n) for n in nodes(grouped, "connection")))
