# Homework 4 spike

**Question:** What share of real process maps are single linear chains, and how long are they?

The completed Homework 4 spike measured **5 anonymized workplace processes**. Of these, **4 were structurally compatible with the linear MVP**, giving an **80% pass rate** and a **median process length of 14 tasks** across all five processes. The committed evidence is in [processes.csv](processes.csv), and [analyze_spike.py](analyze_spike.py) reproduces the summary.

P03 demonstrated real yes/no branching. Its flattened workbook passed the CLI, but it could not faithfully represent the real process as a single linear chain, so P03 is recorded as a structural failure. A successful CLI run alone does not establish structural compatibility.

The original measurement scope was 5-10 real processes from non-confidential workplace processes and/or published procedures. For any additional observations, add one row per examined process only after collecting evidence, using the fields below.

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

Neither threshold was crossed by the measured sample. The results support the linear MVP's usefulness for these sampled processes; P03 confirms that branching remains an important future capability.

Actual workplace `.xlsx` workbooks remain local-only in the repository-root `spike_workbooks/` directory, which is excluded by `.gitignore`. Keep any additional real/transcribed workbooks there too. Record only non-confidential evidence in the committed CSV.
