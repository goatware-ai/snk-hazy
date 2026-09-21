---
name: task-metadata
description: "metadata.json per task folder: the exact key set (form values only, no rationale prose, AHT nowhere in the repo), taskboard_uid present and null until submission and how a UID is proven to belong to a draft, built_with for model gating, and where UIDs are looked up (2026-08-26)"
metadata:
  type: project
---

Each task folder carries **`metadata.json`** (never metadata.md, converted 2026-08-26: "just clear
data, no need to explanation"). Keys in this order:

```json
{
  "task_name": "june-price-review",
  "taskboard_uid": "7373c89f-...",       // null until submitted
  "sector": "Wholesale Trade",
  "onet_occupation": { "code": "11-2022.00", "title": "Sales Managers" },
  "onet_tasks": ["...", "...", "..."],   // 3-5, verbatim dropdown text
  "onet_skills": ["...", "...", "..."],  // 3-5, Worker Requirements -> Skills only
  "input_file_count": 10,
  "multimodal": false,
  "web_search_allowed": false,
  "manual_time_hours": 7,
  "llm_starting_point": "Other",
  "built_with": "claude-fable-5",        // see [[model-routing]]
  "build_session": "f26c2b60"
}
```

**Values only.** No justification prose, no alternates kept on file, no occupation rationale, no
per-pick clause mapping; that reasoning goes in the build summary and the task's feedback-log.md
([[feedback-log-convention]]). **AHT is tracked nowhere in the repo** (2026-08-26): not in the
metadata and struck from every doc; the platform still asks at submit time, answer it there in
minutes.

**`taskboard_uid` is always present, null until the operator fills it after submission.** A
missing key and a null one must not be confused: null marks the folder as unsubmitted, and
`autoeval_check.py` keys its `_unsubmitted` behaviour off the blank placeholder, so deleting the
line silently loosens the gate. Never invent a UUID. Several drafts may await submission at once,
so prove which UID belongs to which draft before writing it: `stb submissions fetch-task <uid>`
writes a JSON whose `task_documents[0].submission_document.prompt` is the prompt actually
submitted; match that text against the draft's prompt.md. `stb submissions download` does not
serve this ("no uploaded file"). Once written, the next `/fetch-status` promotes the draft
([[submission-tracking]]); a still-null or mis-filled UID leaves the submission under "Needs
attention" as `?`. A retired task has no UID at all.

**Consumers read JSON:** `gcheck.common.load_metadata` (M1/M2/M3 and `_rubric_uid_suffix`),
`build_model.read`/`stamp` (`built_with`), `fetch_status.find_draft_by_uid` (`taskboard_uid`).
The old markdown form let a wrapped bold header swallow a skills block; that class of bug is why
the file is JSON.

**Finding a task from a UID:** grep the UID across `*/metadata.json` or read `submission-list.md`,
which maps sequence prefix to task name to UID per status section ([[submission-tracking]],
[[repo-layout-and-tooling]]). submission-list.md is a status board, not a journal: no dates,
findings or platform to-do lists beyond the short Note column under NEEDS_REVISION. Related:
[[onet-occupation-routing]] for the occupation, task and skill values.

- 2026-09-12 (boiler-replacement-recommendation refinement): the platform's Input Files Quality Check ruled a PDF-only input set "not multi-modal under the rule" and FAILed the form with multimodal Yes, after an earlier run of the same check had called Yes a match; the check is LLM-judged and flips, so set multimodal No for PDF-only sets and follow its FAIL ruling on resubmission. prompts/refine-task.md updated the same day.
