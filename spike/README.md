# Homework 4 spike

**Question:** What share of real process maps are single linear chains, and how long are they?

Examine 5-10 real processes from non-confidential workplace processes and/or published procedures. `processes.csv` starts with headers only; add one row per examined process after collecting evidence.

| Field | Evidence to record |
| --- | --- |
| `process_id` | A unique, non-confidential identifier for the process. |
| `source_type` | Whether the source is a non-confidential workplace process or a published procedure. |
| `task_count` | Positive integer count of tasks in the full process, including processes that fail. |
| `department_count` | Positive integer count of departments involved. |
| `passed` | `true` if the current MVP can represent the process as a single linear chain; otherwise `false`. |
| `first_failure_reason` | First reason the process cannot be represented; required for failures and blank for passes. |

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe spike/analyze_spike.py
```

The script uses Python's standard library and reads `processes.csv` beside the script, regardless of the working directory. It prints the total process count, number passed, pass percentage, and median task count across **all** examined processes. Invalid or incomplete rows produce an error instead of a partial summary. With no observations, both counts are zero and the percentage and median are `N/A`; these are empty-dataset indicators, not spike results.

The decision rule from issue #3 is: if fewer than roughly half of processes pass, **or** the median length is above roughly 25 tasks, treat the MVP as a demo and prioritize branching support rather than polish in the next project change.

Real/transcribed `.xlsx` workbooks are intentionally not committed. Keep temporary local spike workbooks in the repository-root `spike_workbooks/` directory, which is excluded by `.gitignore`. Record only non-confidential evidence in the committed CSV. No process observations or measurements are included in this setup.
