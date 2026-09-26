"""Deterministic SVG with a horizontal slot for every task."""

import unicodedata
from xml.etree import ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
BOX_WIDTH, GAP, LEFT, TOP = 352, 72, 184, 100
LINE_HEIGHT = 20


def wrap(text, width=40):
    """Preserve every character, bounding even long words and wide glyphs."""
    lines, line, units = [], "", 0
    for char in text:
        size = 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1
        if char == "\n":
            lines.append(line)
            line, units = "", 0
            continue
        if units + size > width:
            lines.append(line)
            line, units = "", 0
        line += char
        units += size
    lines.append(line)
    return lines


def labels(task):
    result = wrap("ID: " + task.task_id)
    result += wrap(task.description)
    result += wrap("Section: " + task.section)
    if task.annual_frequency is not None:
        result += wrap("Annual frequency: " + str(task.annual_frequency))
    return result


def element(parent, tag, **attrs):
    return ET.SubElement(parent, f"{{{SVG}}}{tag}", {key.replace("_", "-"): str(value) for key, value in attrs.items()})


def text_lines(parent, lines, x, y, fill="#172b4d", size=13):
    text = element(parent, "text", x=x, y=y, fill=fill, font_size=size, font_family="Consolas, monospace")
    text.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    for index, line in enumerate(lines):
        element(text, "tspan", x=x, y=y + index * LINE_HEIGHT).text = line


def render_svg(tasks):
    departments = list(dict.fromkeys(task.department for task in tasks))
    task_lines = [labels(task) for task in tasks]
    heights = [max(100, len(lines) * LINE_HEIGHT + 32) for lines in task_lines]
    lane_heights = {
        department: max(
            max(height for task, height in zip(tasks, heights) if task.department == department) + 48,
            len(wrap(department, 16)) * LINE_HEIGHT + 48,
        ) for department in departments
    }
    lane_y, y = {}, TOP
    for department in departments:
        lane_y[department] = y
        y += lane_heights[department]
    width = LEFT + len(tasks) * (BOX_WIDTH + GAP)
    root = ET.Element(f"{{{SVG}}}svg", {"width": str(width), "height": str(y + 32), "viewBox": f"0 0 {width} {y + 32}", "role": "img"})
    element(root, "title").text = "Process swimlane diagram"
    element(root, "desc").text = f"{len(tasks)} tasks across {len(departments)} departments; read from left to right."
    element(root, "rect", width=width, height=y + 32, fill="#ffffff")
    text_lines(root, ["PROCESS SWIMLANE"], 24, 35, size=20)
    text_lines(root, [f"{len(tasks)} tasks / {len(departments)} departments / sequence left to right"], 24, 66, fill="#52647d")
    defs = element(root, "defs")
    marker = element(defs, "marker", id="arrow", markerWidth=10, markerHeight=10, refX=9, refY=5, orient="auto", markerUnits="userSpaceOnUse")
    element(marker, "path", d="M 0 0 L 10 5 L 0 10 Z", fill="#227d87")
    for index, department in enumerate(departments):
        group = element(root, "g", data_kind="lane", data_department=department)
        start, height = lane_y[department], lane_heights[department]
        element(group, "rect", x=16, y=start, width=width-32, height=height, fill="#f0f5fa" if index % 2 == 0 else "#f8fafc", stroke="#dbe3ec")
        text_lines(group, wrap(department, 16), 30, start + 35, fill="#304761")
    positions = []
    for index, (task, height) in enumerate(zip(tasks, heights)):
        x = LEFT + index * (BOX_WIDTH + GAP)
        y = lane_y[task.department] + (lane_heights[task.department] - height) / 2
        positions.append((x, y, height))
    for index in range(len(tasks)-1):
        x, y, height = positions[index]
        nx, ny, nh = positions[index+1]
        start, end, middle = y + height/2, ny + nh/2, x + BOX_WIDTH + GAP/2
        path = element(root, "path", d=f"M {x+BOX_WIDTH} {start} H {middle} V {end} H {nx}", fill="none", stroke="#227d87", stroke_width=2, marker_end="url(#arrow)", data_kind="connection", data_source=tasks[index].task_id, data_target=tasks[index+1].task_id)
    for task, lines, (x, y, height) in zip(tasks, task_lines, positions):
        group = element(root, "g", data_kind="task", data_id=task.task_id, data_department=task.department)
        element(group, "rect", x=x, y=y, width=BOX_WIDTH, height=height, rx=8, fill="#ffffff", stroke="#7892ab")
        element(group, "rect", x=x, y=y+8, width=4, height=height-16, fill="#227d87")
        text_lines(group, lines, x+16, y+27)
    result = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    ET.fromstring(result)
    return result
