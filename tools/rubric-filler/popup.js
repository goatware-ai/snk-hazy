// UI + orchestration. The pure CSV helpers live in csv.js (loaded first, and
// covered by test.js); everything that runs inside the page lives in pageOps().

const $ = (id) => document.getElementById(id);

let items = [];
let taskName = "";
let uid8 = "";
let hasReq = false;
let rowStatus = []; // parallel to items: {status, note, problems}
let mode = "fill"; // which run produced rowStatus: "fill" | "compare"
let mismatchArmed = false; // a task mismatch was reported; the next click fills anyway

const FILE_HINT = "columns: CRITERION, WEIGHT (REQ optional) — name it rubric-{task-name}-{uid8}.csv";

// A click on an <a download> rather than chrome.downloads, so the extension
// needs no "downloads" permission: a reload that picks up new popup code does
// not reliably pick up a newly declared permission, which left chrome.downloads
// undefined at the call site. The download starts while the popup is still open,
// so the popup's teardown never races it.
function downloadCsv(text, filename) {
  const url = URL.createObjectURL(new Blob([text], { type: "text/csv" }));
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 60000);
}

// ---------- preview ----------

function escapeHtml(s) {
  return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

// A fill needs words only for problems: the row's own highlight already says
// whether it was newly written. A compare is the other way round — the whole
// point is what differs, so every non-matching row carries its reason.
function statusLabel(rs) {
  if (!rs) return "";
  if (rs.status === "problem") return `⚠ ${escapeHtml((rs.problems || []).join("; "))}`;
  if (rs.note) return escapeHtml(rs.note);
  return "";
}

function rowClass(rs) {
  if (!rs) return "";
  if (rs.status === "problem" || rs.status === "missing") return "row-problem";
  if (rs.status === "differs") return "row-diff";
  if (rs.status === "changed") return "row-changed";
  return "";
}

function renderPreview() {
  const rows = items
    .map((it, i) => {
      const text = it["textarea-criterion"];
      const rs = rowStatus[i];
      return `<tr class="${rowClass(rs)}"><td class="seqcol">${i + 1}</td><td class="weightcol">${
        it["numeric-weight"]
      }</td><td>${escapeHtml(text.slice(0, 140))}${
        text.length > 140 ? "…" : ""
      }</td><td class="statuscol">${statusLabel(rs)}</td></tr>`;
    })
    .join("");
  $("preview").innerHTML = `<table>${rows}</table>`;
  $("preview").style.display = "block";
  document.body.classList.add("tall"); // give the row list the full popup height
}

function showPreview(name) {
  const t = weightTotals(items);
  // The rubric rules turn on these totals, so they belong in front of the
  // operator before anything is written: a truncated CSV shows up here first.
  $("fileinfo").textContent = `${name} — ${t.count} criteria · +${t.pos} / ${t.neg} · net ${t.net}${
    hasReq ? " · REQ" : ""
  }`;
  $("taskname").textContent = taskName
    ? `Task: ${taskName}${uid8 ? ` (${uid8})` : " (draft, no UID)"}`
    : "Task: (unknown — file isn't named rubric-{task-name}-{uid8}.csv)";
  renderPreview();
  $("fill").disabled = !items.length;
  $("compare").disabled = !items.length;
}

function showStatus(msg, ok) {
  const el = $("status");
  if (!msg) {
    el.style.display = "none";
    el.className = "";
    return;
  }
  el.textContent = msg;
  el.className = ok ? "ok" : "err";
}

// ---------- loading ----------

function loadFile(file) {
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const parsed = rowsToItems(parseCsv(decodeCsvBytes(reader.result)));
      items = parsed.items;
      hasReq = parsed.hasReq;
      const named = taskNameFromFilename(file.name);
      taskName = named.taskName;
      uid8 = named.uid8;
      rowStatus = []; // a freshly loaded CSV has no results yet
      mode = "fill";
      mismatchArmed = false;
      $("fill").textContent = "Fill form";
      showPreview(file.name);
      showStatus("");
      chrome.storage.local.set({
        items, taskName, uid8, hasReq, fileName: file.name, rowStatus, mode,
        fillSummary: null, fillProgress: null,
      });
    } catch (e) {
      items = [];
      taskName = "";
      uid8 = "";
      hasReq = false;
      rowStatus = [];
      $("fill").disabled = true;
      $("compare").disabled = true;
      showStatus(`CSV error: ${e.message}`, false);
    }
  };
  // readAsText would assume UTF-8; decodeCsvBytes sniffs the BOM instead.
  reader.readAsArrayBuffer(file);
}

$("file").addEventListener("change", (e) => {
  if (e.target.files[0]) loadFile(e.target.files[0]);
});
const drop = $("drop");
drop.addEventListener("dragover", (e) => { e.preventDefault(); drop.classList.add("hover"); });
drop.addEventListener("dragleave", () => drop.classList.remove("hover"));
drop.addEventListener("drop", (e) => {
  e.preventDefault();
  drop.classList.remove("hover");
  if (e.dataTransfer.files[0]) loadFile(e.dataTransfer.files[0]);
});

// Restore the last upload, and whatever the last run left behind — a fill runs
// in the page, so closing the popup mid-run no longer loses the outcome.
chrome.storage.local
  .get(["items", "taskName", "uid8", "hasReq", "fileName", "rowStatus", "mode", "fillSummary", "fillProgress"])
  .then((s) => {
    if (!s.items?.length) return;
    items = s.items;
    taskName = s.taskName || "";
    uid8 = s.uid8 || "";
    hasReq = !!s.hasReq;
    rowStatus = s.rowStatus || [];
    mode = s.mode || "fill";
    showPreview(s.fileName || "last upload");
    const running = s.fillProgress && Date.now() - s.fillProgress.at < 120000;
    if (running) {
      showStatus(
        `A fill is still running in the page: ${s.fillProgress.done}/${s.fillProgress.total} criteria. Reopen this popup in a moment for the result.`,
        true
      );
    } else if (s.fillSummary) {
      showStatus(`${s.fillSummary.text}\n(from the last run)`, s.fillSummary.ok);
    } else if (mode === "compare" && rowStatus.length) {
      // Say which run painted the rows, so the colours still mean something
      // after the popup has been closed and reopened.
      showStatus("Showing the last comparison with the form.", true);
    }
  });

// ---------- talking to the page ----------

async function runOnPage(op, payload) {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab) throw new Error("no active tab");
  let frames;
  try {
    frames = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: pageOps,
      args: [op, payload ?? null],
    });
  } catch (e) {
    throw new Error(`${e.message} (the rubric form has to be the active tab; Chrome blocks chrome:// pages)`);
  }
  // Destructuring blind used to produce "Cannot read properties of undefined"
  // for the most common mistake of all: running it on the wrong tab.
  const result = frames?.[0]?.result;
  if (!result) throw new Error("the page returned nothing — is the rubric form the active tab?");
  if (result.error) throw new Error(result.error);
  return result;
}

// The form and the CSV are otherwise indistinguishable, so check the task UID
// before writing 30-odd criteria over someone else's rubric. Returns the probe
// when it disagrees, null when it matches or when there is nothing to compare.
async function taskMismatch() {
  if (!uid8) return null; // a draft CSV carries no UID: nothing to check against
  const probe = await runOnPage("probe");
  if (!probe.uids.length) return null; // no UID visible on the page
  if (probe.uids.some((u) => u.replace(/-/g, "").startsWith(uid8))) return null;
  return probe;
}

// ---------- fill ----------

$("fill").addEventListener("click", async () => {
  if (!items.length) return;
  const btn = $("fill");
  btn.disabled = true;
  btn.textContent = "Filling…";
  showStatus("Working — the page keeps going even if this popup closes…", true);

  try {
    if (!mismatchArmed) {
      const bad = await taskMismatch();
      if (bad) {
        mismatchArmed = true;
        showStatus(
          `Task check failed — nothing was written.\nThe form shows ${bad.uids.join(", ")}\nThe CSV is ${taskName} (${uid8}).\nClick "Fill anyway" if this really is the right form.`,
          false
        );
        return;
      }
    }

    const result = await runOnPage("fill", items);
    rowStatus = result.rows || [];
    mode = "fill";
    mismatchArmed = false;
    renderPreview();
    const changed = rowStatus.filter((r) => r.status === "changed").length;
    const problems = rowStatus.filter((r) => r.status === "problem").length;
    const cleared = result.cleared
      ? `\n${result.cleared} leftover section${result.cleared === 1 ? "" : "s"} blanked (15-section minimum)`
      : "";
    const warn = result.warnings.length ? `\nWarnings:\n${result.warnings.join("\n")}` : "";
    const text = `Filled ${result.filled}/${items.length} criteria ✔  (${changed} newly filled/changed, ${problems} problem${
      problems === 1 ? "" : "s"
    })${cleared}${warn}`;
    showStatus(text, problems === 0);
    chrome.storage.local.set({ rowStatus, mode, fillSummary: { text, ok: problems === 0 } });
  } catch (e) {
    showStatus(`Fill failed: ${e.message}`, false);
  } finally {
    btn.textContent = mismatchArmed ? "Fill anyway" : "Fill form";
    btn.disabled = !items.length;
  }
});

// ---------- compare ----------

$("compare").addEventListener("click", async () => {
  if (!items.length) return;
  const btn = $("compare");
  btn.disabled = true;
  btn.textContent = "Reading form…";
  showStatus("Reading the form — keep this popup open…", true);

  try {
    const result = await runOnPage("read");
    const formRows = result.rows;
    const norm = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
    let match = 0;
    let differs = 0;
    let missing = 0;

    rowStatus = items.map((it, i) => {
      const got = formRows[i];
      if (!got) {
        missing++;
        return { status: "missing", note: "no section on the form", problems: [] };
      }
      const wantText = norm(it["textarea-criterion"]);
      const wantWeight = String(it["numeric-weight"]);
      const gotWeight = String(got.weight ?? "").trim();
      const bits = [];
      if (norm(got.criterion) !== wantText) bits.push(got.criterion ? "text differs" : "text blank");
      if (gotWeight !== wantWeight) bits.push(`weight ${gotWeight || "blank"} ≠ ${wantWeight}`);
      if (!bits.length) { match++; return { status: "match", note: "", problems: [] }; }
      differs++;
      return { status: "differs", note: bits.join(", "), problems: [] };
    });

    mode = "compare";
    renderPreview();
    const extra = formRows.slice(items.length).filter((r) => r.criterion || r.weight).length;
    const extraNote = extra ? `\n${extra} section${extra === 1 ? "" : "s"} on the form beyond the CSV still hold values` : "";
    const warn = result.warnings.length ? `\nWarnings:\n${result.warnings.join("\n")}` : "";
    showStatus(
      `Compared against the form: ${match} match, ${differs} differ, ${missing} missing${extraNote}${warn}`,
      differs === 0 && missing === 0 && !extra
    );
    chrome.storage.local.set({ rowStatus, mode, fillSummary: null });
  } catch (e) {
    showStatus(`Compare failed: ${e.message}`, false);
  } finally {
    btn.disabled = !items.length;
    btn.textContent = "⇄ Compare with form";
  }
});

// ---------- export ----------

$("fetch").addEventListener("click", async () => {
  const btn = $("fetch");
  btn.disabled = true;
  btn.textContent = "Reading form…";
  showStatus("Reading the form — keep this popup open…", true);

  try {
    const result = await runOnPage("read");
    const rows = result.rows.map((r) => ({ criterion: r.criterion, weight: r.weight, req: "" }));
    // The platform holds a floor of 15 sections, so a shorter rubric leaves
    // blank trailing ones. Drop those (only from the end) rather than export them.
    let blankSkipped = 0;
    while (rows.length && !rows[rows.length - 1].criterion && !rows[rows.length - 1].weight) {
      rows.pop();
      blankSkipped++;
    }
    if (!rows.length) {
      showStatus("The form has no filled criteria to export.", false);
      return;
    }

    // REQ is repo-side metadata with no field on the form, so it can only come
    // back from the loaded CSV, matched by position — which is honest only when
    // the two agree on how many criteria there are.
    const withReq = hasReq && rows.length === items.length;
    if (withReq) rows.forEach((r, i) => { r.req = items[i].req; });
    const reqNote = hasReq && !withReq
      ? `\nREQ column omitted: the form has ${rows.length} criteria, the CSV has ${items.length}, so REQ tags cannot be matched by position.`
      : "";

    // Keep the export distinct from the tracked rubric so it can never
    // overwrite it: the operator diffs the two by hand.
    const name = taskName ? `rubric-${taskName}-from-form.csv` : "rubric-from-form.csv";
    downloadCsv(toRubricCsv(rows, withReq), name);
    const skipped = blankSkipped
      ? `\n(${blankSkipped} trailing blank section${blankSkipped === 1 ? "" : "s"} skipped)`
      : "";
    const warn = result.warnings.length ? `\nWarnings:\n${result.warnings.join("\n")}` : "";
    showStatus(`Exported ${rows.length} criteria to ${name} ✔${skipped}${reqNote}${warn}`, !result.warnings.length);
  } catch (e) {
    showStatus(`Export failed: ${e.message}`, false);
  } finally {
    btn.disabled = false;
    btn.textContent = "⬇ Export form to CSV";
  }
});

// ---------- reset ----------

$("reset").addEventListener("click", () => {
  // Only clears the popup's CSV state — the page is never touched
  items = [];
  taskName = "";
  uid8 = "";
  hasReq = false;
  rowStatus = [];
  mode = "fill";
  mismatchArmed = false;
  $("file").value = "";
  $("preview").style.display = "none";
  $("preview").innerHTML = "";
  document.body.classList.remove("tall");
  $("fileinfo").textContent = FILE_HINT;
  $("taskname").textContent = "";
  $("fill").textContent = "Fill form";
  $("fill").disabled = true;
  $("compare").disabled = true;
  chrome.storage.local.remove([
    "items", "taskName", "uid8", "hasReq", "fileName", "rowStatus", "mode", "fillSummary", "fillProgress",
  ]);
  showStatus("CSV cleared — upload a new file", true);
});

// ---------------------------------------------------------------------------
// Injected into the page. Must be entirely self-contained: it is serialised and
// re-parsed there, so it can close over nothing from this file. One function for
// all three operations, because they share every selector and every wait.
// ---------------------------------------------------------------------------
async function pageOps(op, payload) {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const norm = (s) => (s || "").replace(/\s+/g, " ").trim().toLowerCase();
  // chrome.storage is reachable from an injected script, which is how a fill
  // reports progress that outlives the popup.
  const store = typeof chrome !== "undefined" && chrome.storage ? chrome.storage.local : null;

  // Sections carry a stable data-testid; index is 0-based
  const sectionAt = (i) =>
    document.querySelector(`[data-testid="repeatable-criteria-instance-${i}"]`);
  const sectionCount = () =>
    document.querySelectorAll('[data-testid^="repeatable-criteria-instance-"]').length;

  async function waitFor(fn, timeout = 4000) {
    const t0 = Date.now();
    while (Date.now() - t0 < timeout) {
      const v = fn();
      if (v) return v;
      await sleep(120);
    }
    return null;
  }

  // React ignores plain .value writes; go through the native setter
  function setValue(el, value) {
    const proto =
      el.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    Object.getOwnPropertyDescriptor(proto, "value").set.call(el, String(value));
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
  }

  // ---- field lookup ----
  // Both of these prefer the data-testid and fall back only when the section
  // holds exactly one candidate. A fallback that picks the first of several
  // would quietly write the weight into whatever new field the platform adds,
  // and the read-back check would pass because it reads what it just wrote.
  function criterionTextarea(section) {
    if (!section) return null;
    const byId = section.querySelector('[data-testid="field-textarea-criterion"] textarea');
    if (byId) return byId;
    const all = section.querySelectorAll("textarea");
    return all.length === 1 ? all[0] : null;
  }

  function weightInput(section) {
    if (!section) return null;
    const byId = section.querySelector('[data-testid="field-numeric-weight"] input');
    if (byId) return byId;
    const nums = section.querySelectorAll('input[type="number"]');
    return nums.length === 1 ? nums[0] : null;
  }

  // ---- dialogs ----
  // The delete confirmation is a Radix alert dialog portalled out of the section
  // subtree: role="alertdialog", data-testid="dialog-content", data-state open or
  // closed. It is position:fixed, and Chrome reports offsetParent === null for a
  // fixed element, so visibility here is measured, never inferred from that.
  const DIALOG_SEL =
    '[data-testid="dialog-content"], [role="alertdialog"], [role="dialog"], dialog[open]';

  function shown(el) {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }

  function visible(el) {
    return !!el && !el.disabled && shown(el);
  }

  // data-state flips to "closed" while the close animation plays and the node is
  // still in the DOM, so a dialog counts as open only while it is not "closed".
  function openDialog() {
    return (
      [...document.querySelectorAll(DIALOG_SEL)].find(
        (d) => d.getAttribute("data-state") !== "closed" && shown(d)
      ) || null
    );
  }

  // "Delete section? / Are you sure you want to delete this entry?" — the row
  // only goes away once this Yes is clicked. The dialog's other two buttons are
  // "Cancel" and an icon-only Close (aria-label="Close", no text), so matching on
  // the button's own text cannot hit the wrong one.
  function confirmYesButton() {
    const d = openDialog();
    if (!d) return null;
    return (
      [...d.querySelectorAll("button")].find(
        (el) => visible(el) && /^(yes|confirm|delete|ok)$/.test(norm(el.textContent))
      ) || null
    );
  }

  // If a confirmation is left standing (a delete that never took, a mis-click),
  // everything after it would be clicking a page the modal has covered — Radix
  // also drops pointer events on the rest of the document while it is open.
  async function dismissAnyDialog() {
    const d = openDialog();
    if (!d) return;
    const close =
      [...d.querySelectorAll("button")].find(
        (b) => visible(b) && /^(cancel|no)$/.test(norm(b.textContent))
      ) || d.querySelector('[data-testid="dialog-close-button"]');
    if (close) close.click();
    else document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
    await waitFor(() => !openDialog(), 1000);
  }

  // ---- section plumbing ----
  // The per-section delete control has gone by several labels ("Delete section",
  // "Delete criterion") and can be icon-only, so match its accessible name too.
  function deleteButtonIn(section) {
    if (!section) return null;
    return (
      [...section.querySelectorAll("button")].find((b) =>
        /delete (section|criteri)/.test(
          norm(`${b.textContent} ${b.getAttribute("aria-label") || ""} ${b.getAttribute("title") || ""}`)
        )
      ) || null
    );
  }

  function addButton() {
    return (
      [...document.querySelectorAll("button")].find((b) =>
        /add criterion/.test(norm(b.textContent))
      ) || null
    );
  }

  // A collapsed accordion keeps its fields out of the DOM, so nothing can be
  // read or written without expanding first.
  async function expand(i) {
    const section = sectionAt(i);
    if (!section) return null;
    const toggle = section.querySelector("button[aria-expanded]");
    if (toggle && toggle.getAttribute("aria-expanded") !== "true") toggle.click();
    return await waitFor(() => criterionTextarea(sectionAt(i)));
  }

  function collapse(i) {
    const done = sectionAt(i)?.querySelector("button[aria-expanded]");
    if (done && done.getAttribute("aria-expanded") === "true") done.click();
  }

  // Write every field of `item` into section i, verifying each write. Returns
  // { problems, textChanged, weightChanged } (problems is [] when everything
  // checks out), or null if the section is missing or will not expand.
  async function applyItem(i, item) {
    const ta = await expand(i);
    if (!ta) return null;
    const problems = [];
    let textChanged = false;
    let weightChanged = false;

    const wantText = String(item["textarea-criterion"] ?? "");
    if (ta.value !== wantText) {
      setValue(ta, wantText);
      const ok = await waitFor(() => {
        const el = criterionTextarea(sectionAt(i));
        return el && el.value === wantText;
      }, 1000);
      if (!ok) problems.push("criterion text did not stick");
      else textChanged = true;
    }

    const weight = weightInput(sectionAt(i));
    const wantWeight = String(item["numeric-weight"] ?? "");
    if (!weight) {
      problems.push("weight input not found");
    } else if (weight.value !== wantWeight) {
      setValue(weight, wantWeight);
      if (!(await waitFor(() => weight.value === wantWeight, 1000)))
        problems.push("weight did not stick");
      else weightChanged = true;
    }

    collapse(i);
    return { problems, textChanged, weightChanged };
  }

  function saveProgress(done, total) {
    try { store?.set({ fillProgress: { done, total, at: Date.now() } }); } catch (e) { /* best effort */ }
  }

  // ---- operations ----

  // Which task is this page showing? Used to refuse a fill from another task's
  // CSV, since one rubric form looks exactly like the next.
  function probe() {
    const uuid = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi;
    const near = `${location.href} ${document.title}`;
    let found = near.match(uuid) || [];
    if (!found.length) found = (document.body?.innerText || "").match(uuid) || [];
    return { sections: sectionCount(), uids: [...new Set(found.map((u) => u.toLowerCase()))] };
  }

  async function fill(list) {
    const warnings = [];
    let filled = 0;
    let cleared = 0;
    // Did criterion #i actually change during this run (phase 1 or phase 2)?
    const everChanged = new Array(list.length).fill(false);
    const phase1Problems = new Array(list.length).fill(null);

    // Phase 0: delete surplus trailing sections so re-runs reconcile the count.
    // The platform keeps a minimum of 15 sections (no delete button below that).
    const floor = Math.max(list.length, 15);
    while (sectionCount() > floor) {
      const count = sectionCount();
      let del = deleteButtonIn(sectionAt(count - 1));
      if (!del) {
        // Delete button may only render once the section is expanded
        await expand(count - 1);
        del = await waitFor(() => deleteButtonIn(sectionAt(count - 1)), 2000);
      }
      if (!del) {
        warnings.push(`could not find the section's delete button; ${count} sections remain`);
        break;
      }
      del.click();
      // Either the row goes straight away (older builds) or a confirmation modal
      // appears and has to be answered; wait for whichever comes first.
      const answer = await waitFor(
        () => (sectionCount() < count ? "deleted" : confirmYesButton()),
        2000
      );
      if (answer && answer !== "deleted") {
        answer.click();
        // The modal has to actually close, or the next delete click lands on a
        // covered page and silently does nothing.
        await waitFor(() => !confirmYesButton(), 2000);
      }
      if (!(await waitFor(() => sectionCount() < count))) {
        warnings.push(
          answer
            ? "section count did not decrease after confirming the delete"
            : 'no "Yes" confirmation appeared and the section was not deleted'
        );
        break;
      }
    }
    await dismissAnyDialog(); // never leave a modal covering the form we go on to fill

    // Phase 0b: sections past the CSV rows that could not be deleted (the
    // 15-section minimum) — blank their stale text and weight, and verify it,
    // because a leftover criterion still scores.
    for (let i = list.length; i < sectionCount(); i++) {
      const ta = await expand(i);
      if (!ta) {
        warnings.push(`#${i + 1}: leftover section could not be expanded to clear it`);
        continue;
      }
      if (ta.value !== "") setValue(ta, "");
      const weight = weightInput(sectionAt(i));
      if (weight && weight.value !== "") setValue(weight, "");
      const emptied = await waitFor(() => {
        const t = criterionTextarea(sectionAt(i));
        const w = weightInput(sectionAt(i));
        return t && t.value === "" && (!w || w.value === "");
      }, 1000);
      if (!emptied) warnings.push(`#${i + 1}: leftover section would not clear`);
      else cleared++;
      collapse(i);
    }

    // Phase 1: fill every section. Problems are not final here — a later
    // re-render can revert an earlier field, which is what phase 2 is for.
    for (let i = 0; i < list.length; i++) {
      const n = i + 1;
      let section = sectionAt(i);
      if (!section) {
        const btn = addButton();
        if (!btn) return { error: `criterion ${n}: no "Add criterion" button found` };
        btn.click();
        section = await waitFor(() => sectionAt(i));
        if (!section) return { error: `criterion ${n}: section did not appear after Add criterion` };
      }
      section.scrollIntoView({ block: "center" });

      const res = await applyItem(i, list[i]);
      if (res === null) return { error: `criterion ${n}: could not expand section (no textarea appeared)` };
      everChanged[i] = res.textChanged || res.weightChanged;
      phase1Problems[i] = res.problems;
      filled++;
      if (n % 3 === 0 || n === list.length) saveProgress(n, list.length);
      await sleep(60);
    }

    // Phase 2: verify and heal, but only where phase 1 actually wrote something
    // or hit a problem. A section phase 1 found already correct and left alone
    // has nothing for a re-render to revert, and re-opening all of them doubled
    // the run time of what is usually a no-op re-run.
    await sleep(400);
    const rows = [];
    for (let i = 0; i < list.length; i++) {
      if (!everChanged[i] && !phase1Problems[i].length) {
        rows.push({ status: "unchanged", note: "", problems: [] });
        continue;
      }
      const res = await applyItem(i, list[i]);
      if (res === null) {
        warnings.push(`#${i + 1}: section missing during verify pass`);
        rows.push({ status: "problem", note: "", problems: ["section missing during verify pass"] });
        continue;
      }
      everChanged[i] = everChanged[i] || res.textChanged || res.weightChanged;
      for (const p of res.problems) warnings.push(`#${i + 1}: ${p}`);
      rows.push({
        status: res.problems.length ? "problem" : everChanged[i] ? "changed" : "unchanged",
        note: "",
        problems: res.problems,
      });
    }

    // Hand the outcome to storage as well as to the popup: the popup may already
    // be gone, and the run it started is the one that knows what happened.
    try { store?.set({ rowStatus: rows, fillProgress: null }); } catch (e) { /* best effort */ }
    return { filled, cleared, warnings, rows };
  }

  // Reads every section in form order, leaving each one exactly as it was found.
  async function read() {
    const total = sectionCount();
    if (!total) return { error: "no criterion sections found on this page" };

    const warnings = [];
    const rows = [];
    for (let i = 0; i < total; i++) {
      const section = sectionAt(i);
      if (!section) {
        warnings.push(`#${i + 1}: section disappeared while reading`);
        rows.push({ criterion: "", weight: "" });
        continue;
      }
      const toggle = section.querySelector("button[aria-expanded]");
      const wasCollapsed = toggle && toggle.getAttribute("aria-expanded") !== "true";
      const ta = await expand(i);
      if (!ta) {
        warnings.push(`#${i + 1}: could not expand section (no textarea appeared)`);
        rows.push({ criterion: "", weight: "" });
        continue;
      }
      const weight = weightInput(sectionAt(i));
      if (!weight) warnings.push(`#${i + 1}: weight input not found`);
      rows.push({
        // The form wraps long criteria, but the stored value keeps whatever the
        // fill wrote; normalise whitespace so a diff is about wording, not layout.
        criterion: (ta.value || "").replace(/\s+/g, " ").trim(),
        weight: (weight?.value || "").trim(),
      });
      if (wasCollapsed) collapse(i);
      await sleep(30);
    }
    return { rows, warnings, total };
  }

  if (op === "probe") return probe();
  if (op === "fill") return await fill(payload);
  if (op === "read") return await read();
  return { error: `unknown operation "${op}"` };
}
