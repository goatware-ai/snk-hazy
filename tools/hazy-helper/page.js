/* Everything that touches the page runs here.
 *
 * `pageOps` is handed to chrome.scripting.executeScript, which serialises it and runs it
 * in the page's own world. That means it must be SELF-CONTAINED: no imports, no closure
 * over anything in the popup. Helpers live inside it for that reason.
 *
 * What it knows about the form's DOM, and how much of that is verified:
 *
 *   Rubric      VERIFIED against a capture of the live rubric view (rubric-sample.html).
 *               The ids are DUPLICATED across rubric rows - all three description
 *               textareas carry id="textarea-rubric_description" - so getElementById is
 *               useless here and every lookup is scoped to a repeatable instance
 *               container instead.
 *   Everything  INFERRED from the form capture's field labels, because no DOM for those
 *   else       sections was available when this was written. They are matched on label
 *               text, which is why `scan` exists: run it first and read what matched
 *               before letting `fill` write anything.
 *
 * File uploads are never touched. A browser will not let a page set a file input's value
 * from a path, and the operator excluded it anyway; they are reported and skipped.
 */
async function pageOps(op, payload) {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const norm = (s) => (s || "").replace(/\s+/g, " ").trim();
  const low = (s) => norm(s).toLowerCase();
  const out = { op, ok: true, sections: {}, notes: [], skipped: [] };

  // ---------------------------------------------------------------- values

  // React ignores a plain `.value =` write: it tracks the last value it set and skips the
  // change. Going through the prototype's native setter and then dispatching input/change
  // is what makes the framework see the edit.
  function setValue(el, value) {
    const proto =
      el.tagName === "TEXTAREA"
        ? HTMLTextAreaElement.prototype
        : HTMLInputElement.prototype;
    Object.getOwnPropertyDescriptor(proto, "value").set.call(el, String(value));
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function readValue(el) {
    return el ? norm(el.value) : null;
  }

  // ---------------------------------------------------------------- finding

  function allButtons() {
    return [...document.querySelectorAll('button, [role="button"]')];
  }

  function findButton(re) {
    return allButtons().find((b) => re.test(norm(b.textContent)));
  }

  // The label a control is bound to, by `for`, by wrapping <label>, or by the nearest
  // field container's own label. Field containers carry data-testid="field-...".
  function labelOf(el) {
    if (el.id) {
      const esc = (window.CSS && CSS.escape) ? CSS.escape(el.id) : el.id.replace(/"/g, '\\"');
      const l = document.querySelector(`label[for="${esc}"]`);
      if (l) return norm(l.textContent);
    }
    const wrap = el.closest("label");
    if (wrap) return norm(wrap.textContent);
    const field = el.closest('[data-testid^="field-"]');
    const l2 = field && field.querySelector("label");
    if (l2) return norm(l2.textContent);
    return "";
  }

  function controls() {
    return [...document.querySelectorAll("input, textarea")].filter(
      (el) => el.type !== "hidden"
    );
  }

  function byLabel(re, opts = {}) {
    const hits = controls().filter(
      (el) => re.test(labelOf(el)) && (!opts.type || el.type === opts.type)
    );
    return opts.all ? hits : hits[0] || null;
  }

  // Expand every collapsed accordion so the fields exist in the DOM. Form sections and
  // rubric rows are both accordions; a collapsed one may not render its inputs at all.
  async function expandAll() {
    let opened = 0;
    for (let pass = 0; pass < 4; pass++) {
      const shut = [...document.querySelectorAll('[aria-expanded="false"]')];
      if (!shut.length) break;
      for (const b of shut) {
        try {
          b.click();
          opened++;
        } catch (e) {
          /* a disabled trigger is not an error */
        }
      }
      await sleep(180);
    }
    return opened;
  }

  // ------------------------------------------------------------ repeatables

  // Every repeatable field renders its rows as [data-testid*="-instance-N"]. The group
  // itself is found by walking up from its own "Add another ..." button until we reach a
  // node that contains instances - that survives the testid hash changing between fields.
  function groupFor(addRe) {
    const btn = findButton(addRe);
    if (!btn) return null;
    let n = btn;
    while (n && n !== document.body) {
      if (n.querySelector('[data-testid*="-instance-"]')) return { group: n, btn };
      n = n.parentElement;
    }
    return { group: null, btn };
  }

  function instancesIn(group) {
    return [...group.querySelectorAll('[data-testid*="-instance-"]')];
  }

  async function ensureRows(addRe, wanted) {
    const found = groupFor(addRe);
    if (!found || !found.group) return { group: null, btn: found && found.btn };
    let rows = instancesIn(found.group);
    let guard = 0;
    while (rows.length < wanted && guard++ < 200) {
      found.btn.click();
      await sleep(140);
      rows = instancesIn(found.group);
    }
    return { group: found.group, btn: found.btn, rows, guard };
  }

  // Fill a one-field-per-row repeatable (input file list, output file list, tools).
  async function fillSimpleRepeatable(name, addRe, values) {
    const res = { name, wanted: values.length, written: 0, rows: 0, problems: [] };
    if (!values.length) {
      res.problems.push("nothing to write");
      return res;
    }
    const { group, btn, rows } = await ensureRows(addRe, values.length);
    if (!btn) {
      res.problems.push(`no "add another" button matched ${addRe}`);
      return res;
    }
    if (!group) {
      res.problems.push("found the add button but no instance rows under it");
      return res;
    }
    res.rows = rows.length;
    if (rows.length < values.length) {
      res.problems.push(`only ${rows.length} rows for ${values.length} values`);
    }
    values.forEach((v, i) => {
      const row = rows[i];
      if (!row) return;
      const el =
        row.querySelector("textarea") ||
        row.querySelector('input[type="text"]') ||
        row.querySelector("input:not([type=file]):not([type=checkbox]):not([type=radio])");
      if (!el) {
        res.problems.push(`row ${i + 1}: no text field`);
        return;
      }
      setValue(el, v);
      res.written++;
    });
    return res;
  }

  // ---------------------------------------------------------------- rubric

  // Verified selectors. The description and weight ids repeat across rows, so both are
  // read from inside the row's own instance container.
  const RUBRIC_DESC = '[data-testid="field-textarea-rubric_description"]';
  const RUBRIC_WEIGHT = '[data-testid^="field-numeric-add_a_criteria_weight"]';
  const RUBRIC_ADD = /add a new rubric/i;

  function rubricRows() {
    const all = [...document.querySelectorAll('[data-testid*="-instance-"]')];
    const mine = all.filter((n) => n.querySelector(RUBRIC_DESC));
    if (mine.length) return mine;
    // Fall back to any instance holding a textarea plus a number input in -5..+5.
    return all.filter(
      (n) =>
        n.querySelector("textarea") &&
        n.querySelector('input[min="-5"][max="5"], input[type="number"]')
    );
  }

  function rubricFields(row) {
    const desc =
      row.querySelector(`${RUBRIC_DESC} textarea`) || row.querySelector("textarea");
    const weight =
      row.querySelector(`${RUBRIC_WEIGHT} input`) ||
      row.querySelector('input[min="-5"][max="5"]') ||
      row.querySelector('input[type="number"]');
    return { desc, weight };
  }

  async function fillRubric(criteria) {
    const res = { name: "rubric", wanted: criteria.length, written: 0, rows: 0, problems: [] };
    if (!criteria.length) {
      res.problems.push("nothing to write");
      return res;
    }
    const addBtn = findButton(RUBRIC_ADD);
    let rows = rubricRows();
    let guard = 0;
    while (rows.length < criteria.length && addBtn && guard++ < 300) {
      addBtn.click();
      await sleep(140);
      rows = rubricRows();
    }
    if (!rows.length) {
      res.problems.push("no rubric rows found on this page");
      return res;
    }
    await expandAll();
    rows = rubricRows();
    res.rows = rows.length;
    if (rows.length < criteria.length) {
      res.problems.push(
        `only ${rows.length} rows for ${criteria.length} criteria` +
          (addBtn ? "" : ' (no "Add a New Rubric" button found)')
      );
    }
    criteria.forEach((c, i) => {
      const row = rows[i];
      if (!row) return;
      const { desc, weight } = rubricFields(row);
      if (!desc) {
        res.problems.push(`row ${i + 1}: no description field`);
        return;
      }
      setValue(desc, c.description);
      if (weight != null && c.weight != null && c.weight !== "") {
        setValue(weight, c.weight);
      } else if (c.weight != null && c.weight !== "") {
        res.problems.push(`row ${i + 1}: no weight field`);
      }
      res.written++;
    });
    if (rows.length > criteria.length) {
      res.problems.push(
        `${rows.length - criteria.length} row(s) on the form beyond the ${criteria.length} supplied; ` +
          "they were left untouched and must be removed by hand"
      );
    }
    return res;
  }

  // ------------------------------------------------------------ radio picks

  // Domain and Occupation are single-select lists. Match an option by its exact visible
  // text, then click whatever is actually clickable for it.
  function pickOption(wanted) {
    const target = low(wanted);
    if (!target) return { ok: false, why: "no value supplied" };
    const radios = [...document.querySelectorAll('input[type="radio"], [role="radio"]')];
    const scored = radios.map((r) => {
      const lbl = labelOf(r) || norm(r.closest("label,li,div")?.textContent || "");
      return { r, lbl: low(lbl) };
    });
    let hit = scored.filter((s) => s.lbl === target);
    if (!hit.length) hit = scored.filter((s) => s.lbl.startsWith(target));
    if (!hit.length) hit = scored.filter((s) => s.lbl.includes(target));
    if (!hit.length) return { ok: false, why: `no option matching "${wanted}"` };
    if (hit.length > 1) {
      const exact = hit.filter((s) => s.lbl === target);
      if (exact.length === 1) hit = exact;
      else return { ok: false, why: `"${wanted}" matched ${hit.length} options` };
    }
    const el = hit[0].r;
    const clickable = el.closest("label") || el;
    clickable.click();
    if (el.tagName === "INPUT" && !el.checked) el.click();
    return { ok: true, label: hit[0].lbl };
  }

  // ------------------------------------------------------------------ scan

  function scan() {
    const fileInputs = [...document.querySelectorAll('input[type="file"]')];
    const checkboxes = [...document.querySelectorAll('input[type="checkbox"], [role="checkbox"]')];
    const radios = [...document.querySelectorAll('input[type="radio"], [role="radio"]')];
    const s = {
      url: location.href,
      title: document.title,
      radios: radios.length,
      checkboxes: checkboxes.length,
      checkboxesTicked: checkboxes.filter(
        (c) => c.checked || c.getAttribute("aria-checked") === "true"
      ).length,
      fileInputs: fileInputs.length,
      rubricRows: rubricRows().length,
      addButtons: allButtons()
        .map((b) => norm(b.textContent))
        .filter((t) => /^\+?\s*add /i.test(t)),
      labelledFields: [],
    };
    for (const el of controls()) {
      if (el.type === "file") continue;
      const l = labelOf(el);
      if (l) s.labelledFields.push({ label: l.slice(0, 110), tag: el.tagName.toLowerCase(), type: el.type });
    }
    const seen = new Set();
    s.labelledFields = s.labelledFields.filter((f) => {
      const k = f.label + "|" + f.tag;
      if (seen.has(k)) return false;
      seen.add(k);
      return true;
    });
    return s;
  }

  // ------------------------------------------------------------------ time

  const TIME_FIELDS = [
    ["read", /time to read and understand/i],
    ["files", /time to open|skim\s*\/?\s*search|use the reference files/i],
    ["work", /time to perform the required work/i],
    ["qa", /verification\s*\/?\s*qa|final review/i],
    ["total_hours", /total time/i],
  ];

  // --------------------------------------------------------------- dispatch

  if (op === "scan") {
    await expandAll();
    out.scan = scan();
    return out;
  }

  const p = payload || {};
  const want = (k) => op === "fill" || op === "fill:" + k;

  await expandAll();

  // Section 1 -------------------------------------------------------------
  if (want("identity") && (p.domain || p.occupation)) {
    const r = { name: "domain & occupation", problems: [] };
    if (p.occupation) {
      const o = pickOption(p.occupation);
      r.occupation = o.ok ? o.label : null;
      if (!o.ok) r.problems.push("occupation: " + o.why);
    }
    if (p.domain) {
      const d = pickOption(p.domain);
      r.domain = d.ok ? d.label : null;
      if (!d.ok) r.problems.push("domain: " + d.why);
    }
    out.sections.identity = r;
  }

  // Section 2 -------------------------------------------------------------
  if (want("instruction") && p.task_instruction) {
    const r = { name: "task instruction", problems: [] };
    const el =
      byLabel(/task instruction/i) ||
      [...document.querySelectorAll("textarea")].find((t) =>
        /you are the \[role\]|briefing a skilled colleague/i.test(t.placeholder || "")
      );
    if (el) {
      setValue(el, p.task_instruction);
      r.written = true;
      r.chars = p.task_instruction.length;
    } else {
      r.problems.push("no Task Instruction textarea found");
    }
    out.sections.instruction = r;
  }

  if (want("inputs") && (p.input_files || []).length) {
    out.sections.input_files = await fillSimpleRepeatable(
      "input file list",
      /add another input file/i,
      p.input_files
    );
  }

  // Section 3 -------------------------------------------------------------
  if (want("outputs") && (p.output_files || []).length) {
    out.sections.output_files = await fillSimpleRepeatable(
      "output file list",
      /add another output file/i,
      p.output_files
    );
  }

  if (want("times") && p.times) {
    const r = { name: "times", written: 0, problems: [] };
    for (const [key, re] of TIME_FIELDS) {
      const v = p.times[key];
      if (v === undefined || v === null || v === "") continue;
      const el = byLabel(re);
      if (!el) {
        r.problems.push(`no field matched ${key}`);
        continue;
      }
      setValue(el, v);
      r.written++;
    }
    out.sections.times = r;
  }

  if (want("tools") && (p.tools || []).length) {
    out.sections.tools = await fillSimpleRepeatable(
      "tools",
      /add another tool/i,
      p.tools
    );
  }

  // Section 4 -------------------------------------------------------------
  if (want("rubric") && (p.rubric || []).length) {
    out.sections.rubric = await fillRubric(p.rubric);
  }

  // Section 5 -------------------------------------------------------------
  // Opt-in only. Each box is an attestation about the package, so ticking them is never
  // part of "fill everything"; the operator asks for it separately and deliberately.
  if (op === "fill:checklist") {
    const boxes = [...document.querySelectorAll('input[type="checkbox"], [role="checkbox"]')];
    let ticked = 0;
    for (const b of boxes) {
      const on = b.checked || b.getAttribute("aria-checked") === "true";
      if (!on) {
        (b.closest("label") || b).click();
        ticked++;
        await sleep(40);
      }
    }
    out.sections.checklist = { name: "checklist", boxes: boxes.length, ticked };
  }

  // Uploads ---------------------------------------------------------------
  const files = document.querySelectorAll('input[type="file"]');
  if (files.length) {
    out.skipped.push(
      `${files.length} file upload field(s) left alone - a page cannot set a file input ` +
        "from a path, so both zips are yours to attach by hand"
    );
  }

  if (!Object.keys(out.sections).length) {
    out.ok = false;
    out.notes.push("nothing matched: is the right form section open on this tab?");
  }
  return out;
}
