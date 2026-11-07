"""Offline viewer composed from the export's geometry, without a second layout."""

from copy import deepcopy
from xml.etree import ElementTree as ET

from .render import LEFT, SVG, element, text_lines


def render_viewer(svg):
    diagram = ET.fromstring(svg)
    width, height = int(diagram.get("width")), int(diagram.get("height"))
    labels = ET.Element(f"{{{SVG}}}svg", {
        "width": str(LEFT), "height": str(height),
        "viewBox": f"0 0 {LEFT} {height}", "class": "labels", "role": "img",
        "aria-label": "Department labels",
    })
    element(labels, "rect", width=LEFT, height=height, fill="#ffffff")
    text_lines(labels, ["DEPARTMENTS"], 30, 66, fill="#304761")
    for lane in diagram.findall(".//*[@data-kind='lane']"):
        label = deepcopy(lane)
        label.find(f"{{{SVG}}}rect").set("width", str(LEFT - 16))
        labels.append(label)
        # The scrollable half contains lane backgrounds, not duplicate labels.
        for text in lane.findall(f"{{{SVG}}}text"):
            lane.remove(text)
    for heading in diagram.findall(f"{{{SVG}}}text"):
        diagram.remove(heading)
    diagram.set("width", str(width - LEFT))
    diagram.set("viewBox", f"{LEFT} 0 {width - LEFT} {height}")
    diagram.set("class", "diagram")
    # ElementTree escapes all workbook text and attributes for inline SVG too.
    content = ET.tostring(labels, encoding="unicode") + ET.tostring(diagram, encoding="unicode")
    return ("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Process swimlane viewer</title>
<style>
* { box-sizing: border-box; }
body { margin: 0; color: #172b4d; background: white; font-family: system-ui, sans-serif;
       height: 100vh; display: flex; flex-direction: column; }
header { padding: 12px 20px; flex: none; }
h1 { font-size: 20px; margin: 0 0 4px; }
p { margin: 0; }
.viewport { overflow: auto; flex: 1; min-height: 0; }
.viewport:focus-visible { outline: 2px solid #227d87; outline-offset: -2px; }
.canvas { display: flex; width: max-content; align-items: flex-start; }
svg { display: block; flex: none; }
.labels { position: sticky; left: 0; z-index: 1; background: white; }
</style>
</head>
<body>
<header><h1>Process swimlane viewer</h1>
<p>Scroll right to follow the process. Department labels stay on the left.
Scroll down to see more lanes. Focus the diagram to use arrow keys.</p></header>
<main class="viewport" tabindex="0" aria-label="Scrollable process diagram">
<div class="canvas">""" + content + "</div></main></body></html>\n").encode("utf-8")
