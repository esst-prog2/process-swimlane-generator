"""Generate a synthetic section-band sample without overwriting earlier inputs."""
from pathlib import Path

from openpyxl import Workbook

from process_swimlane.cli import main
from process_swimlane.workbook import HEADERS


if __name__ == "__main__":
    directory = Path(".qa")
    directory.mkdir(exist_ok=True)
    number = 1
    while True:
        suffix = "" if number == 1 else f"_{number}"
        path = directory / f"section_bands_36{suffix}.xlsx"
        if not path.exists():
            break
        number += 1
    sections = (["Intake"] * 3
                + ["Detailed review & supplier coordination <quality assurance phase>"] * 26
                + ["Approval"] * 3 + ["Intake"] * 2 + ["Closeout"] * 2)
    departments = ["Requesting", "Procurement & supplier quality coordination", "Finance", "Receiving"]
    book = Workbook()
    sheet = book.active
    sheet.title = "Process"
    sheet.append(HEADERS)
    rows = []
    for i, section in enumerate(sections):
        description = f"Synthetic task {i+1:03}"
        if i == 5:
            description += " detailed check" * 65
        if i == 6:
            description += " financial check" * 20
        rows.append([f"{i+1:03}", section, description, departments[i % 4], 0,
                     f"{i+2:03}" if i < len(sections)-1 else None])
    # Deliberately reverse worksheet order to exercise successor-based grouping.
    for row in reversed(rows):
        sheet.append(row)
    for row in sheet.iter_rows(min_row=2):
        row[0].number_format = row[5].number_format = "@"
    with path.open("xb") as stream:
        book.save(stream)
    book.close()
    print(f"Synthetic workbook: {path}")
    raise SystemExit(main([str(path), "--viewer"]))
