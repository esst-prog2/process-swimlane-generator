from decimal import Decimal
from dataclasses import replace
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest
from xml.etree import ElementTree as ET

from openpyxl import Workbook

from process_swimlane.model import Task
from process_swimlane.render import render_svg, wrap
from process_swimlane.validation import validate_process
from process_swimlane.workbook import read_workbook


def demo_tasks(count=12):
    departments = ["Requesting", "Purchasing", "Finance", "Receiving"]
    frequencies = (Decimal("120"), Decimal("0.5"), Decimal("0"), None)
    return [Task(i+2, f"{i+1:03}", "Purchase request", f"Synthetic task {i+1}", departments[i % 4], frequencies[i % 4], f"{i+2:03}" if i < count-1 else None) for i in range(count)]


class RenderTests(unittest.TestCase):
    def test_homework5_manual_successors_match_arrow_endpoints(self):
        # Independent manual oracle recorded in PLANNING_LOG.md on 2026-10-08.
        # Do not obtain expected edges from renderer output or ordered tasks.
        expected_departments = {
            "A": "Requester", "B": "Reviewer", "C": "Manager", "D": "Requester",
        }
        expected_edges = [("A", "B"), ("B", "C"), ("C", "D")]
        with TemporaryDirectory() as directory:
            path = Path(directory) / "homework5.xlsx"
            book = Workbook()
            sheet = book.active
            sheet.title = "Process"
            sheet.append([
                "task_id", "section", "task", "department",
                "annual_frequency", "next_task_id",
            ])
            sheet.append(["A", "Homework 5", "Task A", "Requester", None, "B"])
            sheet.append(["B", "Homework 5", "Task B", "Reviewer", None, "C"])
            sheet.append(["C", "Homework 5", "Task C", "Manager", None, "D"])
            sheet.append(["D", "Homework 5", "Task D", "Requester", None, None])
            book.save(path)
            book.close()
            root = ET.fromstring(render_svg(validate_process(read_workbook(path))))

        namespace = {"svg": "http://www.w3.org/2000/svg"}
        nodes = root.findall(".//*[@data-kind='task']")
        self.assertEqual(len(nodes), 4)
        self.assertCountEqual([node.get("data-id") for node in nodes], expected_departments)
        ports = {}
        for node in nodes:
            task_id = node.get("data-id")
            self.assertEqual(node.get("data-department"), expected_departments[task_id])
            self.assertIn(f"ID: {task_id}", "".join(node.itertext()))
            box = node.find("svg:rect", namespace)
            self.assertIsNotNone(box)
            x, y, width, height = (float(box.get(key)) for key in ("x", "y", "width", "height"))
            self.assertGreater(width, 0)
            self.assertGreater(height, 0)
            ports[task_id] = {"in": (x, y + height / 2), "out": (x + width, y + height / 2)}

        def task_at(point, side):
            matches = [
                task_id for task_id, sides in ports.items()
                if all(abs(actual - expected) < 1e-6 for actual, expected in zip(point, sides[side]))
            ]
            self.assertEqual(len(matches), 1, f"Endpoint {point} must meet exactly one task's {side} port")
            return matches[0]

        # The documented routing uses gaps between horizontal slots (archived
        # add-process-swimlane-mvp/design.md). Current SVG encodes this as M/H/V/H.
        # Read the actual geometry; never trust data-source/data-target as proof.
        number = r"([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)"
        route = re.compile(rf"M\s+{number}\s+{number}\s+H\s+{number}\s+V\s+{number}\s+H\s+{number}\s*")
        arrows = root.findall(".//*[@data-kind='connection']")
        self.assertEqual(len(arrows), 3)
        actual_edges = []
        for arrow in arrows:
            self.assertEqual(arrow.tag, "{http://www.w3.org/2000/svg}path")
            self.assertEqual(arrow.get("marker-end"), "url(#arrow)")
            match = route.fullmatch(arrow.get("d", ""))
            self.assertIsNotNone(match, f"Unsupported connector routing: {arrow.get('d')}")
            start_x, start_y, bend_x, end_y, end_x = map(float, match.groups())
            source = task_at((start_x, start_y), "out")
            target = task_at((end_x, end_y), "in")
            actual_edges.append((source, target))
        self.assertCountEqual(actual_edges, expected_edges)

    def test_layout_and_connections(self):
        tasks = demo_tasks()
        svg = render_svg(tasks)
        self.assertEqual(svg, render_svg(validate_process(tasks[::-1])))
        root = ET.fromstring(svg)
        lanes = root.findall(".//*[@data-kind='lane']")
        nodes = root.findall(".//*[@data-kind='task']")
        arrows = root.findall(".//*[@data-kind='connection']")
        self.assertEqual((len(lanes), len(nodes), len(arrows)), (4, 12, 11))
        self.assertEqual([lane.get("data-department") for lane in lanes], ["Requesting", "Purchasing", "Finance", "Receiving"])
        for i, arrow in enumerate(arrows):
            self.assertEqual((arrow.get("data-source"), arrow.get("data-target")), (tasks[i].task_id, tasks[i+1].task_id))
        self.assertGreater(int(root.get("width")), 4000)

    def test_one_and_labels(self):
        description = "Éléments <&> " + "Long " * 80
        task = Task(2, "001", "Section", description, "Dept", Decimal(0), None)
        root = ET.fromstring(render_svg([task]))
        self.assertEqual(len(root.findall(".//*[@data-kind='connection']")), 0)
        node = root.find(".//*[@data-kind='task']")
        text = "".join(node.itertext())
        for value in ("ID: 001", description, "Section: Section", "Annual frequency: 0"):
            self.assertIn(value, text)
        self.assertGreater(float(node[0].get("height")), 100)
        absent = Task(2, "001", "Area", "Task", "Dept", None, None)
        self.assertNotIn("Annual frequency", render_svg([absent]).decode())

    def test_frequency_values_in_each_task_box(self):
        for count in (12, 40):
            with self.subTest(count=count):
                tasks = demo_tasks(count)
                root = ET.fromstring(render_svg(tasks))
                nodes = root.findall(".//*[@data-kind='task']")
                for task, node in zip(tasks, nodes):
                    content = "".join(node.itertext())
                    if task.annual_frequency is None:
                        self.assertNotIn("Annual frequency:", content)
                    else:
                        self.assertIn(f"Annual frequency: {task.annual_frequency}", content)
                self.assertEqual(sum("Annual frequency:" in "".join(node.itertext()) for node in nodes), count * 3 // 4)

    def test_frequency_wrapping_fits_task_and_lane(self):
        tasks = demo_tasks()
        for frequency in (Decimal("120"), Decimal("0.5"), Decimal("0"), None,
                          Decimal("12345678901234567890123456789012345678901234567890")):
            with self.subTest(frequency=frequency):
                tasks[0] = replace(tasks[0], description="Long description " * 40, annual_frequency=frequency)
                root = ET.fromstring(render_svg(tasks))
                lanes = {node.get("data-department"): node[0] for node in root.findall(".//*[@data-kind='lane']")}
                last_right = 0
                for node in root.findall(".//*[@data-kind='task']"):
                    box = node[0]
                    x, y, width, height = (float(box.get(key)) for key in ("x", "y", "width", "height"))
                    self.assertGreater(x, last_right)
                    last_right = x + width
                    lane = lanes[node.get("data-department")]
                    self.assertGreaterEqual(y, float(lane.get("y")))
                    self.assertLessEqual(y + height, float(lane.get("y")) + float(lane.get("height")))
                    spans = node.findall(".//{http://www.w3.org/2000/svg}tspan")
                    for span in spans:
                        self.assertGreaterEqual(float(span.get("y")) - 13, y)
                        self.assertLess(float(span.get("y")) + 4, y + height)
                        self.assertLessEqual(len(span.text or ""), 40)
                        self.assertGreaterEqual(float(span.get("x")), x + 16)
                        self.assertLessEqual(float(span.get("x")) + 40 * 8, x + width - 16)
                content = "".join(root.find(".//*[@data-kind='task']").itertext())
                if frequency is not None:
                    self.assertIn(f"Annual frequency: {frequency}", content)

    def test_wrap_preserves_long_words_and_spaces(self):
        value = "a" * 100 + "   "+"漢" * 40
        self.assertEqual("".join(wrap(value)), value)
