---
name: fetch-status-tables-not-bars
description: "user wants /fetch-status results shown as markdown tables, not the script's ASCII bar charts"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bb88f2dc-2539-40b9-a79c-6c7db83eb568
  modified: 2026-09-11T15:14:46.202Z
---

For every `/fetch-status` report, present the submission and payment counts as markdown tables instead of pasting the script's own bar-chart output. **Why:** user asked directly ("show the tables always") after an earlier one-off table request, making it a standing preference rather than a single-turn ask. **How to apply:** still run `tools/build_model.py require sonnet` then `fetch_status.py` as normal and still surface any Movement/Updated/Rejected/Needs-attention sections from its output verbatim (those are status changes, not the chart), but convert the bar-chart count blocks (Submissions, Payment) into small tables in the reply instead of quoting the ASCII bars. See [[submission-tracking]] for the underlying script/report mechanics this sits on top of.
