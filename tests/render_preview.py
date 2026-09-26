"""Generate 12/40-task previews with positive, fractional, zero and blank frequencies."""
from pathlib import Path
from dataclasses import replace
from test_render import demo_tasks
from process_swimlane.render import render_svg

directory = Path('.qa')
directory.mkdir(exist_ok=True)
for count in (12, 40):
    tasks = demo_tasks(count)
    tasks[0] = replace(tasks[0], description='Review the request, confirm the responsible department, and explain the next step. ' * 4)
    (directory / f'preview_{count}.svg').write_bytes(render_svg(tasks))
