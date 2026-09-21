---
description: Review another contributor's Hazy task end to end (Wholesale Trade)
argument-hint: <review-id>
model: opus
---

## Arguments

- `$1`: the review id. Missing: stop and ask for one; this command reviews exactly one task.

## Model

Pinned to **Opus** in the frontmatter above and independent of the session's `/model`. There is
one review path and no fable/opus skill variants, because nothing in the worksheet or the platform
form records which model reviewed.

## Stage

```bash
.venv/bin/python tools/fetch_review.py $1     # review_<short>.json + both zips into reviews/$1/
```

If it cannot produce both zips, stop and tell me rather than reviewing half a packet.

## Run the procedure

Read `prompts/review.md` in full and follow it: it is the whole procedure and the note standard.
Run it as **one pass, in one turn**: stage, verdicts, harness, read, decide, note, worksheet,
`reviews-list.md`. Do not stop to ask me to do my own read first and do not hand any part of the
judgment back to me. The only thing left for me at the end is to read `reviews/$1/worksheet.md`
and submit.

Finish by printing the decision, the selected categories, the note, and the worksheet path.

## Never run

`stb reviews accept`, `stb reviews revise`, `stb reviews skip`: submitting is mine, after I have
read the worksheet. `stb reviews list` and `stb reviews view` are mine as well; you do not need
them.
