"""Run the documented installed CLI and assert end-to-end acceptance."""
from pathlib import Path
import subprocess
import sys
from xml.etree import ElementTree as ET

repo = Path(__file__).resolve().parents[1]
executable = Path(sys.executable).parent / "process-map.exe"
source = repo / "examples" / "purchase_request.xlsx"
original = source.read_bytes()
output = repo / "output"


def run(path):
    result = subprocess.run([str(executable), str(path)], cwd=repo, capture_output=True, text=True)
    print(result.stdout or result.stderr, end="")
    return result


before = set(output.glob("purchase_request_swimlane*.svg"))
for _ in range(2):
    result = run(source)
    assert result.returncode == 0, result.stderr
new = set(output.glob("purchase_request_swimlane*.svg")) - before
assert len(new) == 2
for file in new:
    root = ET.fromstring(file.read_bytes())
    for kind, expected in (("task", 12), ("lane", 4), ("connection", 11)):
        assert len(root.findall(f".//*[@data-kind='{kind}']")) == expected
saved = {path:path.read_bytes() for path in output.iterdir()}
for invalid in sorted((repo / "examples").glob("invalid_*.xlsx")):
    assert run(invalid).returncode != 0
assert saved == {path:path.read_bytes() for path in output.iterdir()}
assert source.read_bytes() == original
print("PASS: 12 tasks, 4 lanes, 11 arrows; two new outputs; invalid inputs preserved all diagrams; input unchanged.")
print("Outputs: " + ", ".join(sorted(path.name for path in new)))
