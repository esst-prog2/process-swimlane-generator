"""Generate a repeatable synthetic wide/tall viewer; never read private inputs."""
from pathlib import Path

from openpyxl import Workbook

from process_swimlane.cli import main
from process_swimlane.workbook import HEADERS


if __name__ == "__main__":
    directory = Path(".qa")
    directory.mkdir(exist_ok=True)
    path = directory / "sticky_departments_45.xlsx"
    if not path.exists():
        book = Workbook()
        sheet = book.active
        sheet.title = "Process"
        sheet.append(HEADERS)
        departments = ["Requesting", "International procurement & supplier quality coordination", "Finance", "Receiving"]
        for i in range(45):
            description = f"Synthetic task {i+1:03}"
            if i == 1:
                description += " detailed review" * 55
            if i == 2:
                description += " financial check" * 18
            sheet.append([f"{i+1:03}", "Viewer verification", description, departments[i % 4], 0,
                          f"{i+2:03}" if i < 44 else None])
        book.save(path)
        book.close()
    raise SystemExit(main([str(path), "--viewer"]))
