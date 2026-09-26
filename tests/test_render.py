from decimal import Decimal
from dataclasses import replace
import unittest
from xml.etree import ElementTree as ET

from process_swimlane.model import Task
from process_swimlane.render import render_svg, wrap
from process_swimlane.validation import validate_process


def demo_tasks(count=12):
    departments = ["Requesting", "Purchasing", "Finance", "Receiving"]
    frequencies = (Decimal("120"), Decimal("0.5"), Decimal("0"), None)
    return [Task(i+2, f"{i+1:03}", "Purchase request", f"Synthetic task {i+1}", departments[i % 4], frequencies[i % 4], f"{i+2:03}" if i < count-1 else None) for i in range(count)]


class RenderTests(unittest.TestCase):
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
