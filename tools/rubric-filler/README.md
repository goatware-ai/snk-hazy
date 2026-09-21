# Rubric Filler

Chrome extension that fills the platform's rubric criterion form from a CSV file, compares
the form against that CSV, and exports the form's criteria back out as a CSV for diffing.

## Install

1. Open `chrome://extensions`
2. Enable **Developer mode** (top right)
3. Click **Load unpacked** and select this folder (`tools/rubric-filler`)

After a manifest change (a new permission, the icons), remove the unpacked extension and
add it again rather than reloading it, since a plain reload does not reliably pick those up.

## CSV format

With a header row (column order doesn't matter; extra columns are ignored):

```csv
NUMBER,CRITERION,WEIGHT
1,"On the Purchase Orders tab, the order quantity for item 100280 is 23 cases.",4,EXC
2,"The workbook contains four tabs: Purchase Orders, Vendor Summary, Budget Check, and Exceptions.",2,FILE
3,"The Purchase Orders tab includes a line for an item with zero units.",-3,EXC
```

- `weight` and `criterion` are required; a header row must name **both** of them, or it is
  read as data instead.
- Weights must be whole numbers. `2.5` is rejected rather than silently truncated to `2`.
- Quote fields that contain commas. Quoted newlines are handled. UTF-8 and UTF-16 files
  both load (the BOM decides).
- No header row also works with exactly two columns: the numeric one is taken as the
  weight, the other as the criterion text.

**Name the file `rubric-{task-name}-{uid8}.csv`**, where `{uid8}` is the first eight
characters of the Taskboard UID. The browser never exposes a picked or dropped file's
full path to the page, only its bare name, so this is the one way the popup can tell which
task a CSV belongs to, since every task's rubric is otherwise indistinguishable content
wise until you read it. The repo's `submissions/*/rubric-{task-name}-{uid8}.csv` files
follow this; a draft has no UID yet and is `drafts/*/rubric-{task-name}.csv`, which the
popup reads just as well. A file named anything else still loads and fills the form fine;
the popup just has no task name to show and cannot run the task check below.

## Use

1. Open the rubric form page and make sure the criterion list is visible.
2. Click the extension icon and drop (or pick) the CSV file. The preview shows the parsed
   rows, each numbered with its criterion sequence number (the leftmost column, matching
   the criterion's position on the platform form). Above it, the task name and UID from the
   file name; below it, the counts that the rubric rules turn on:
   `34 criteria · +48 / -6 · net 42`. A truncated or mis-parsed CSV usually shows up
   in that line before anything reaches the form.
3. Click **Fill form**.

**The task check runs first.** The extension reads the task UID off the page and compares it
with the `{uid8}` in the file name. If they disagree, nothing is written: the status banner
names both, and the button becomes **Fill anyway** for a deliberate second click. A draft CSV
(no UID in the name), or a page showing no UID at all, skips the check.

Then it:

- deletes surplus trailing sections / clicks **Add criterion** until the section count
  matches the CSV; below the platform's 15-section minimum it instead blanks the leftover
  sections' text and weight, verifies they really are empty, and reports how many,
- answers the **Delete section? / Are you sure you want to delete this entry?** confirmation
  each delete raises by clicking its **Yes**, and waits for the modal to close before the
  next one (a build that deletes without asking still works),
- expands each collapsed section, fills the criterion textarea and weight input, and
  collapses it again,
- re-checks the sections it actually wrote to, since a later re-render can revert an earlier
  field. Sections that already matched the CSV are left alone and not re-opened.

After it finishes, every row is marked by its highlight:

- **no highlight** — the section already matched the CSV; nothing was written.
- **yellow row** — this run wrote a new criterion text and/or weight, because the section
  was blank or held a different value.
- **red row, with ⚠ *reason*** — a write didn't stick; the reason is the same text that
  also lands in the status banner's warnings list.

That lets you tell a fresh fill from a no-op re-run at a glance, and the seq column names
exactly which criteria still need attention. Re-running is safe: values are overwritten in
place, so to update an already-filled form just upload the corrected CSV and click
**Fill form** again.

The fill runs inside the page, so closing the popup no longer loses it. Reopen the popup
and it shows either the progress of a run still going (`12/34 criteria`) or the result of
the last one.

**Reset** clears the loaded CSV (rows, preview, status, remembered upload) so a new file can
be uploaded. It never touches the page.

## Compare with form

**⇄ Compare with form** reads what the form currently holds and marks each preview row
against the CSV, writing nothing:

- **no highlight** — text and weight both match.
- **orange row** — `text differs`, `weight 4 ≠ 2`, or both.
- **red row** — `no section on the form` for that criterion.

The status bar totals it up, and says whether any sections *beyond* the CSV still hold
values. Use it to confirm a submitted rubric still matches the repo's copy without
downloading anything.

## Export form to CSV

**⬇ Export form to CSV** goes the other way: it reads the criteria the form currently holds
and downloads them as a CSV.

It walks every criterion section in form order, expanding each one long enough to read its
text and weight and then putting it back the way it was found (a collapsed section keeps its
fields out of the DOM, so there is no way to read it without expanding). Blank trailing
sections, the leftovers of the platform's 15-section minimum, are dropped rather than
exported, and the status bar says how many were skipped. Nothing on the page is written.

The file is written to the browser's download folder as `rubric-{task-name}-from-form.csv`
when a CSV named `rubric-{task-name}-{uid8}.csv` is loaded (so the task name is known),
otherwise `rubric-from-form.csv`. The `-from-form` suffix keeps it from ever overwriting the
tracked rubric. The download goes through an `<a download>` click, so no `downloads`
permission is needed; Chrome strips any path from that name, so the destination is always
the download folder. Keep the popup open until the status banner appears.

The output matches the repo's `rubric-{task-name}-{uid8}.csv` format exactly, byte for byte:
BOM, `NUMBER,CRITERION,WEIGHT` header, LF line endings, minimal quoting. So an unchanged
rubric diffs clean:

```
diff submissions/23-sample-task/rubric-sample-task-7373c89f.csv \
     ~/Downloads/rubric-sample-task-from-form.csv
```

