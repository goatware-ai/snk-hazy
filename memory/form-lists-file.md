---
name: form-lists-file
description: "Every task folder carries form-lists.md at its root (outside both zips) with the platform form's typed values: Input File List entries (name - contents), the Output File List entry, the five time values, the tools, and the domain and occupation pair; the operator asked twice on 2026-09-21 where these answers were"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: afce3ffb-b5e8-491d-b00d-dc340ae72fb1
  modified: 2026-09-21T21:21:21.191Z
---

Write `form-lists.md` in every task folder root, beside metadata.json and outside both zips, holding what the operator types into the form: one Input File List entry per input (exact file name, a plain hyphen, a short note on the contents), the Output File List entry, a table of the four minute fields and the total in hours, the tools, and the domain, occupation and O*NET code.

**Why:** the folder layout in prompts/submission.md had no home for the per-file descriptions the form's Input File List asks for, so after the first draft on 2026-09-21 the operator asked "where are the input list files to be filled in the form?" and then "why these are not in task folder?", and again where the time and tool answers were. The values sit in metadata.json, but the file descriptions existed only in chat.

**How to apply:** write the file from the zip listings as the last content step of a build, run the same prose-tell sweep over it as over the prompt (plain hyphens, no em dashes, no self-description in the notes), and keep its numbers identical to metadata.json. See [[task-metadata]] and [[repo-layout-and-tooling]].
