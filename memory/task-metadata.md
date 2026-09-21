---
name: task-metadata
description: "metadata.json per task folder on Hazy: the key set after the 2026-09-21 port (domain replaces sector, onet_occupation {code,title} from the platform's closed 64, the five time values as four integer minute fields plus a total in hours, a tools list with at least one non-AI tool), taskboard_uid present and null until a UID is proven to belong to a draft, built_with for model gating, and the keys carried over from Geranium that no Hazy form field asks for"
metadata:
  type: project
---

Each task folder carries **`metadata.json`** (never metadata.md, converted 2026-08-26: "just clear
data, no need to explanation"). Keys in this order:

```json
{
  "task_name": "june-price-review",
  "taskboard_uid": "7373c89f-...",       // null until submitted
  "domain": "Management",                // one of the form's 14
  "onet_occupation": { "code": "11-3071.00", "title": "Transportation, Storage, and Distribution Managers" },
  "onet_tasks": ["...", "...", "..."],   // carried over, see "Keys no Hazy form asks for"
  "onet_skills": ["...", "...", "..."],  // carried over, see "Keys no Hazy form asks for"
  "input_file_count": 4,
  "multimodal": false,
  "web_search_allowed": false,
  "time": {
    "read_prompt_min": 25,               // integer minutes
    "reference_files_min": 85,           // integer minutes
    "perform_work_min": 240,             // integer minutes
    "verification_qa_min": 70,           // integer minutes
    "total_hours": 7.0                   // decimal hours, >= the four summed and converted
  },
  "tools": ["Excel", "Adobe Acrobat"],   // at least one, at least one of them non-AI
  "llm_starting_point": "Other",
  "built_with": "claude-fable-5",        // see [[model-routing]]
  "build_session": "f26c2b60"
}
```

**Values only.** No justification prose, no alternates kept on file, no occupation rationale, no
per-pick clause mapping; that reasoning goes in the build summary and the task's feedback-log.md
([[feedback-log-convention]]).

## domain and onet_occupation (2026-09-21, replaces sector)

**`sector` is gone.** Hazy assigns no sector. The form's section 1 is two single-select radio
lists, Domain (14 entries) and Occupation (64 entries), both closed: a domain or occupation not
visible in the form is not available. Both lists are captured in
`docs/submission/platform/domains-and-occupations.md`; the O*NET codes and job families are in
`docs/submission/platform/onet-codes.md`.

- `domain` is the form's spelling of one of the 14, verbatim.
- `onet_occupation.title` is the form's spelling of one of the 64, verbatim, and `.code` is that
  occupation's O*NET-SOC code from onet-codes.md. The form abbreviates some titles; the code is
  what identifies the occupation.
- **Pick the domain that matches the occupation's own O*NET job family.** The 64 occupations fall
  into 13 families, and the form's 14 domains are those 13 plus `Healthcare Practitioners /
  Support`, which is not an O*NET family and is the duplicate to avoid unless nothing else fits.
  The four First-Line Supervisor rows are NOT Management.

Both values vary per task. No document, prompt or check may assert a single sector or occupation
for this desk.

## The five time values (2026-09-21, replaces manual_time_hours)

The single `manual_time_hours` number is gone, and so is the older "AHT is tracked nowhere in the
repo" rule: the form now asks for five figures and the metadata carries all five, because they
have to be re-entered on every revision.

- The four minute fields are **integers**, and they are the form's four in its order: read and
  understand the prompt; open, skim/search and use the reference files; perform the required work;
  verification/QA and final review.
- `total_hours` is decimal and is **at least the four summed and converted** ("90 minutes is 1.5
  hours"). It may be higher. The form's own advisory check tests exactly this.
- The estimate is for a qualified professional working **without any AI assistant**. Exclude time
  learning missing domain knowledge, waiting on other people or approvals, breaks, and web
  research unless the prompt explicitly requires it.
- The form's advisory Difficulty check wants estimated manual effort **over 3 hours**; the
  guidelines PDF targets **5-10 hours**. Treat under 3 as an error and under 5 as worth a second
  look at the task's size.

## tools (2026-09-21, new)

`tools` is a list of the non-AI tools a solver would reasonably use, the form's "e.g., Excel,
Photoshop, DaVinci, SolidWorks, LabVIEW". At least one entry, and at least one entry that is not
an AI assistant. It is a required form field, so an empty list blocks submission.

## Keys no Hazy form asks for

`onet_tasks`, `onet_skills`, `multimodal`, `web_search_allowed` and `llm_starting_point` are
carried over from Geranium's form, which had pickers for them. **Hazy's form has none of these
fields.** They are kept because the ported gate still loads them and because a future Hazy form
change may restore them; nothing on the live form reads them, so do not spend build time
researching values for them, and do not treat a thin one as a defect. Flagged 2026-09-21 for the
tooling owner to settle.

## taskboard_uid

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

**Consumers read JSON:** `gcheck.common.load_metadata`, `build_model.read`/`stamp`
(`built_with`), `fetch_status.find_draft_by_uid` (`taskboard_uid`). The old markdown form let a
wrapped bold header swallow a skills block; that class of bug is why the file is JSON.

**Finding a task from a UID:** grep the UID across `*/metadata.json` or read `submission-list.md`,
which maps sequence prefix to task name to UID per status section ([[submission-tracking]],
[[repo-layout-and-tooling]]). submission-list.md is a status board, not a journal: no dates,
findings or platform to-do lists beyond the short Note column under NEEDS_REVISION.

- 2026-09-12 (boiler-replacement-recommendation refinement): the platform's Input Files Quality Check ruled a PDF-only input set "not multi-modal under the rule" and FAILed the form with multimodal Yes, after an earlier run of the same check had called Yes a match; the check is LLM-judged and flips, so set multimodal No for PDF-only sets and follow its FAIL ruling on resubmission. Geranium-side; Hazy's form has no multimodal field.
- 2026-09-21 (the Hazy port): `sector` deleted, `domain` added, `manual_time_hours` replaced by the five time values, `tools` added. Input file count is now bounded below, not above: minimum 2, three or more strongly preferred, no upper bound.
