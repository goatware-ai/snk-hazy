/* Popup wiring: hold the payload, run an op in the page, render what came back.
 * All DOM work happens in page.js; nothing here touches the form.
 */
(() => {
  const $ = (id) => document.getElementById(id);
  const ta = $("payload");
  const out = $("out");

  const show = (html, cls) => {
    out.className = cls || "";
    out.innerHTML = html;
  };
  const esc = (s) =>
    String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

  // ------------------------------------------------------------- payload io

  // What is in the payload right now, in one line. The popup restores the last payload
  // from browser storage, so without this a stale one looks identical to a fresh one -
  // which is exactly how a regenerated file gets ignored in favour of the copy loaded
  // before it.
  function summarise(raw, where) {
    let p;
    try {
      p = JSON.parse(raw);
    } catch (e) {
      return `<span class="bad">${where}: not valid JSON</span>`;
    }
    const occ = p.occupation || (p.onet_occupation || {}).title;
    const ins = p.input_files || [];
    const described = ins.filter((e) => / - | \u2014 /.test(e)).length;
    const bits = [
      `${ins.length} input${ins.length === 1 ? "" : "s"}`,
      `${(p.output_files || []).length} output`,
      `${(p.rubric || []).length} criteria`,
      `${(p.tools || []).length} tool${(p.tools || []).length === 1 ? "" : "s"}`,
    ];
    let line = `<span class="ok">${where}</span> ${esc(occ || "no occupation")} | ${bits.join(" | ")}`;
    if (ins.length && described < ins.length) {
      line +=
        `\n<span class="bad">${ins.length - described} input(s) are a bare file name with no ` +
        `description.</span> The form wants "name - what it contains". If you regenerated ` +
        `metadata.json, press Load JSON again: the box above still holds the copy you ` +
        `loaded last, not the file on disk.`;
    }
    return line;
  }

  chrome.storage.local.get("payload").then((r) => {
    if (r.payload) {
      ta.value = r.payload;
      show(summarise(r.payload, "Restored from last time:"));
    }
  });
  let saveTimer;
  ta.addEventListener("input", () => {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(
      () => chrome.storage.local.set({ payload: ta.value }),
      250
    );
  });

  $("clear").addEventListener("click", () => {
    ta.value = "";
    chrome.storage.local.remove("payload");
    show("Cleared.");
  });

  function parsePayload() {
    const raw = ta.value.trim();
    if (!raw) throw new Error("Nothing loaded. Load the task's metadata.json.");
    let p;
    try {
      p = JSON.parse(raw);
    } catch (e) {
      throw new Error("That is not valid JSON: " + e.message);
    }
    if (p && typeof p === "object" && !Array.isArray(p)) return p;
    throw new Error("The payload must be a JSON object.");
  }

  $("jsonFile").addEventListener("change", async (e) => {
    const f = e.target.files[0];
    if (!f) return;
    ta.value = await f.text();
    chrome.storage.local.set({ payload: ta.value });
    show(summarise(ta.value, `Loaded ${f.name}:`));
    e.target.value = "";
  });

  // A rubric CSV is the repo's own artifact: NUMBER,CRITERION,WEIGHT with a UTF-8 BOM and
  // quoted criteria that contain commas. Parsed here so the rubric can be filled without
  // building a payload first.
  function parseCsv(text) {
    const rows = [];
    let row = [], cell = "", q = false;
    const src = text.replace(/^﻿/, "").replace(/\r\n?/g, "\n");
    for (let i = 0; i < src.length; i++) {
      const c = src[i];
      if (q) {
        if (c === '"') {
          if (src[i + 1] === '"') { cell += '"'; i++; }
          else q = false;
        } else cell += c;
      } else if (c === '"') q = true;
      else if (c === ",") { row.push(cell); cell = ""; }
      else if (c === "\n") { row.push(cell); rows.push(row); row = []; cell = ""; }
      else cell += c;
    }
    if (cell.length || row.length) { row.push(cell); rows.push(row); }
    return rows.filter((r) => r.some((c) => c.trim() !== ""));
  }

  $("csvFile").addEventListener("change", async (e) => {
    const f = e.target.files[0];
    if (!f) return;
    e.target.value = "";
    try {
      const rows = parseCsv(await f.text());
      if (!rows.length) throw new Error("the file is empty");
      const head = rows[0].map((h) => h.trim().toUpperCase());
      const ci = head.indexOf("CRITERION");
      const wi = head.indexOf("WEIGHT");
      if (ci < 0 || wi < 0) {
        throw new Error("expected a NUMBER,CRITERION,WEIGHT header row");
      }
      const rubric = rows
        .slice(1)
        .map((r) => ({ description: (r[ci] || "").trim(), weight: (r[wi] || "").trim() }))
        .filter((c) => c.description);
      let p = {};
      try { p = JSON.parse(ta.value || "{}"); } catch (_) { p = {}; }
      p.rubric = rubric;
      ta.value = JSON.stringify(p, null, 2);
      chrome.storage.local.set({ payload: ta.value });
      const bad = rubric.filter((c) => c.weight === "" || isNaN(Number(c.weight)));
      show(
        `<span class="ok">Loaded ${rubric.length} criteria from ${esc(f.name)}.</span>` +
          (bad.length ? `\n<span class="warn">${bad.length} row(s) have no numeric weight.</span>` : "")
      );
    } catch (err) {
      show(`<span class="bad">CSV: ${esc(err.message)}</span>`);
    }
  });

  // ---------------------------------------------------------------- running

  async function run(op) {
    let payload = null;
    if (op !== "scan") {
      try {
        payload = parsePayload();
      } catch (e) {
        show(`<span class="bad">${esc(e.message)}</span>`);
        return;
      }
    }
    show("Working...");
    let tab;
    try {
      [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!tab || !tab.id) throw new Error("no active tab");
      if (/^(chrome|edge|about|chrome-extension):/i.test(tab.url || "")) {
        throw new Error("this is a browser page; open the submission form first");
      }
      const frames = await chrome.scripting.executeScript({
        target: { tabId: tab.id, allFrames: true },
        func: pageOps,
        args: [op, payload],
      });
      // The form may sit in an iframe. Prefer the frame that actually did something.
      const results = frames.map((f) => f.result).filter(Boolean);
      if (!results.length) throw new Error("the page returned nothing");
      const best =
        results.find((r) => r.scan && r.scan.labelledFields && r.scan.labelledFields.length) ||
        results.find((r) => Object.keys(r.sections || {}).length) ||
        results[0];
      render(op, best, results.length);
    } catch (e) {
      show(`<span class="bad">${esc(e.message)}</span>`);
    }
  }

  // --------------------------------------------------------------- printing

  function render(op, r, frameCount) {
    if (op === "scan") return renderScan(r, frameCount);
    const lines = [];
    let problems = 0;
    for (const key of Object.keys(r.sections)) {
      const s = r.sections[key];
      const bits = [];
      if (s.written === true) bits.push(`written${s.chars ? ` (${s.chars} chars)` : ""}`);
      else if (typeof s.written === "number") bits.push(`${s.written}/${s.wanted} written`);
      if (s.rows !== undefined) bits.push(`${s.rows} row(s) on form`);
      if (s.added) bits.push(`${s.added} added`);
      if (s.removed) bits.push(`${s.removed} removed`);
      if (s.selected) {
        bits.push(`domain: ${s.selected.domain || "none"}`);
        bits.push(`occupation: ${s.selected.occupation || "none"}`);
      } else {
        if (s.domain) bits.push(`domain: ${s.domain}`);
        if (s.occupation) bits.push(`occupation: ${s.occupation}`);
      }
      if (s.ticked !== undefined) {
        bits.push(`${s.ticked} newly ticked of ${s.boxes}`);
        if (s.remaining) bits.push(`${s.remaining} still off`);
      }
      const bad = (s.problems || []).length;
      problems += bad;
      lines.push(
        `<span class="${bad ? "warn" : "ok"}">${bad ? "!" : "✓"}</span> ${esc(s.name)}: ${esc(bits.join(", ") || "done")}`
      );
      for (const p of s.problems || []) lines.push(`    <span class="warn">${esc(p)}</span>`);
    }
    for (const s of r.skipped) lines.push(`<span class="warn">skipped</span> ${esc(s)}`);
    for (const n of r.notes) lines.push(`<span class="bad">${esc(n)}</span>`);
    if (!lines.length) lines.push('<span class="bad">nothing was written</span>');
    lines.push(
      `\n<span class="warn">Read the form before you submit.</span> Every section but the ` +
        `rubric is matched on label text, so check what landed where.`
    );
    show(lines.join("\n"), problems ? "" : "");
  }

  function renderScan(r, frameCount) {
    const s = r.scan || {};
    const L = [];
    L.push(`<span class="ok">Scanned</span> ${esc(s.title || "")}`);
    if (s.sectionStates) {
      L.push("\nSections:");
      for (const [name, state] of Object.entries(s.sectionStates)) {
        const cls = state === "open" ? "ok" : "bad";
        L.push(`  <span class="${cls}">${esc(state)}</span>  ${esc(name)}`);
      }
    }
    L.push(
      `radios ${s.radios}  checkboxes ${s.checkboxes} (${s.checkboxesTicked} ticked)  ` +
        `rubric rows ${s.rubricRows}  file inputs ${s.fileInputs}`
    );
    for (const r of s.repeatables || []) {
      if (!r.found) {
        L.push(`\n<span class="bad">${esc(r.key)}: field not found</span>`);
        continue;
      }
      L.push(`\n${esc(r.key)}: ${r.slots} editable slot(s)`);
      if (r.markers && r.markers.length) L.push(`  rows: ${esc(r.markers.join(", "))}`);
      if (r.buttons && r.buttons.length) L.push(`  buttons: ${esc(r.buttons.join(" | "))}`);
    }
    if (s.checklistTotal) {
      L.push(`\nChecklist: ${s.checklistTicked} of ${s.checklistTotal} ticked`);
      for (const item of (s.checklistUnticked || []).slice(0, 14)) {
        L.push(`  <span class="warn">off</span>  ${esc(item)}`);
      }
    }
    if (s.domainOptions || s.occupationOptions) {
      L.push(
        `\nSection 1: ${s.domainOptions} domain / ${s.occupationOptions} occupation options`
      );
      L.push(`  domain now:     ${esc(s.selectedDomain || "nothing selected")}`);
      L.push(`  occupation now: ${esc(s.selectedOccupation || "nothing selected")}`);
    }
    if (frameCount > 1) L.push(`(${frameCount} frames scanned)`);
    if ((s.addButtons || []).length) {
      L.push("\nAdd buttons:");
      for (const b of s.addButtons) L.push("  " + esc(b));
    }
    L.push("\nLabelled fields:");
    if (!(s.labelledFields || []).length) {
      L.push('  <span class="bad">none - is the form section collapsed or not open?</span>');
    } else {
      for (const f of s.labelledFields) L.push(`  [${esc(f.tag)}] ${esc(f.label)}`);
    }
    if (s.fileInputs) {
      L.push(
        `\n<span class="warn">${s.fileInputs} upload field(s) will be left alone.</span>`
      );
    }
    show(L.join("\n"));
  }

  $("scan").addEventListener("click", () => run("scan"));
  $("fill").addEventListener("click", () => run("fill"));
  $("verify").addEventListener("click", () => run("scan"));
  for (const b of document.querySelectorAll("button[data-op]")) {
    b.addEventListener("click", () => {
      if (b.dataset.op === "fill:checklist") {
        const ok = confirm(
          "The 14 checklist boxes are statements about your package: that the instruction " +
            "is self-contained, that every listed file was uploaded, that no criterion " +
            "asserts a fact the inputs do not support.\n\n" +
            "Ticking them here does not make any of that true. Read them on the form.\n\n" +
            "Tick all 14 anyway?"
        );
        if (!ok) return;
      }
      run(b.dataset.op);
    });
  }
})();
