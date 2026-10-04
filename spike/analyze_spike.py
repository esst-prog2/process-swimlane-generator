"""Summarize recorded spike evidence without modifying the evidence file."""

import csv
from pathlib import Path
from statistics import median
import sys


FIELDS = [
    "process_id", "source_type", "task_count", "department_count",
    "passed", "first_failure_reason",
]


def main() -> int:
    evidence_path = Path(__file__).with_name("processes.csv")
    task_counts = []
    passed_count = 0
    seen_ids = set()
    try:
        with evidence_path.open(encoding="utf-8-sig", newline="") as evidence:
            reader = csv.DictReader(evidence)
            if reader.fieldnames != FIELDS:
                raise ValueError("CSV headers must be: " + ",".join(FIELDS))
            for row in reader:
                location = f"CSV line {reader.line_num}"
                if None in row or any(value is None for value in row.values()):
                    raise ValueError(f"{location}: expected six fields")
                row = {key: value.strip() for key, value in row.items()}
                process_id = row["process_id"]
                if not process_id or process_id in seen_ids:
                    raise ValueError(f"{location}: process_id must be nonblank and unique")
                if not row["source_type"]:
                    raise ValueError(f"{location}: source_type must be nonblank")
                counts = {}
                for field in ("task_count", "department_count"):
                    try:
                        counts[field] = int(row[field])
                    except ValueError:
                        raise ValueError(f"{location}: {field} must be a positive integer") from None
                    if counts[field] < 1:
                        raise ValueError(f"{location}: {field} must be a positive integer")
                passed = row["passed"].lower()
                if passed not in ("true", "false"):
                    raise ValueError(f"{location}: passed must be true or false")
                if passed == "false" and not row["first_failure_reason"]:
                    raise ValueError(f"{location}: a failed process needs first_failure_reason")
                if passed == "true" and row["first_failure_reason"]:
                    raise ValueError(f"{location}: a passing process must leave first_failure_reason blank")
                seen_ids.add(process_id)
                task_counts.append(counts["task_count"])
                passed_count += passed == "true"
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    total = len(task_counts)
    print(f"Total processes: {total}")
    print(f"Number passed: {passed_count}")
    if total:
        print(f"Pass rate: {100 * passed_count / total:.2f}%")
        print(f"Median task count: {median(task_counts):g}")
    else:
        print("Pass rate: N/A (no observations)")
        print("Median task count: N/A (no observations)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
