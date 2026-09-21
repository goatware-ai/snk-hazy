/* Everything that touches the page runs here.
 *
 * `pageOps` is handed to chrome.scripting.executeScript, which serialises it and runs it
 * in the page's own world. That means it must be SELF-CONTAINED: no imports, no closure
 * over anything in the popup. Helpers live inside it for that reason.
 *
 * What it knows about the form's DOM, and how much of that is verified:
 *
 *   Sections    VERIFIED. All five accordions carry data-testid="section-<heading>" and
 *               are open or closed by a bare data-open / data-closed attribute, with no
 *               value. Every write opens its own section first and then scopes its field
 *               lookups to that section, which is what keeps a label like "File" from
 *               matching in the wrong place.
 *   Section 1   VERIFIED against a capture (section1-sample.html). The domain and
 *               occupation groups are [data-testid="field-radio-domain"] and
 *               "...-occupation"; each option is
 *               [data-testid="radio-option-container-<exact label>"]; and the control to
 *               click is the button[role=radio], NOT the <input type=radio> beside it,
 *               which is aria-hidden and clipped to a 1px box. One domain arrives already
 *               selected, so a pick is confirmed by reading the group back.
 *   Section 2   VERIFIED against a capture (section2-sample.html). The instruction is
 *               [data-testid="field-task-prompt"] > textarea#task-prompt. The Input File
 *               List is [data-testid="field-repeatabletextarea-input_file_list"] and it
 *               ARRIVES EMPTY: no rows, no editable control, just an Add button. Rows are
 *               counted inside the field container and created as needed, because
 *               anything that locates the list by finding one of its rows finds none.
 *   Section 3   VERIFIED against a capture (section3-sample.html). The five time fields
 *               are TEXTAREAS with maxlength="5", addressed by testid because the section
 *               prints one of their labels three times. Tools is
 *               field-repeatabletextarea-please_insert_any_tool_used_for_this_task_human
 *               and ARRIVES WITH ONE ROW, unlike the file lists which arrive empty; its
 *               row is [data-testid="field-repeatable-textarea"], not the -instance- the
 *               rubric uses, so both row markers count.
 *   Section 4   VERIFIED against two captures. rubric-sample.html is the rubric with
 *               every row expanded; section4-sample.html is the same section on ARRIVAL,
 *               and the difference is what the code is built around. Three rows exist but
 *               ONLY THE FIRST IS OPEN: rows 2 and 3 carry data-hidden/data-closed with
 *               no panel in the DOM, so they have no textarea and no weight input. Rows
 *               are therefore counted by their instance containers and expanded before
 *               anything is written. The ids are also DUPLICATED across rows - every
 *               description textarea carries id="textarea-rubric_description" - so
 *               getElementById is useless and every field lookup is scoped to its row.
 *   Section 5   VERIFIED against a capture (section5-sample.html). The fourteen boxes are
 *               NOT inputs: each is a div with role="checkbox", aria-checked, and its
 *               whole text in aria-label, with no <label> wrapper. aria-checked is the
 *               only record of state, so every tick is confirmed by reading it back, and
 *               a box that will not tick is named.
 *
 * Every section now has a capture behind it. `scan` still exists and is still worth
 * running first: it reports each section's state and what it found without writing.
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

  // Writes, then reads back. A field with maxlength truncates a long value silently, so
  // the only honest way to know what landed is to look.
  function setChecked(el, value) {
    const want = String(value);
    setValue(el, want);
    const got = el.value;
    if (got === want) return null;
    const cap = el.getAttribute("maxlength");
    return cap
      ? `"${want}" did not fit (maxlength ${cap}); the field holds "${got}"`
      : `wrote "${want}" but the field holds "${got}"`;
  }

  function readValue(el) {
    return el ? norm(el.value) : null;
  }

  // ---------------------------------------------------------------- finding

  function allButtons(root) {
    return [...(root || document).querySelectorAll('button, [role="button"]')];
  }

  function findButton(re, root) {
    return allButtons(root).find((b) => re.test(norm(b.textContent)));
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

  function controls(root) {
    return [...(root || document).querySelectorAll("input, textarea")].filter(
      (el) => el.type !== "hidden"
    );
  }

  // Scoped on purpose: several sections carry a field simply labelled "File", so a
  // page-wide label search is ambiguous. Every caller passes the section it means.
  function byLabel(re, opts = {}) {
    const hits = controls(opts.root).filter(
      (el) => re.test(labelOf(el)) && (!opts.type || el.type === opts.type)
    );
    return opts.all ? hits : hits[0] || null;
  }

  // ---------------------------------------------------------------- sections

  // The form's five accordions. Each carries data-testid="section-<its heading>" and is
  // open or closed by the presence of a bare `data-open` / `data-closed` attribute, not by
  // a value. A closed section may not render its fields at all, so anything that writes
  // into one opens it first.
  const SECTIONS = {
    identity: "Select the Domain and Sector",
    metadata: "MetaData",
    completed: "Completed Task",
    rubric: "Task Rubrics",
    checklist: "Before You Submit — Task Creation Checklist",
  };

  // The checklist heading contains an em dash. Comparing it literally is brittle: a capture
  // can carry a hyphen or an en dash instead, and the difference is invisible on screen. So
  // matching falls back to comparing dash-and-space-normalised text.
  function loosen(s) {
    return low(s).replace(/[‒-―−-]+/g, "-").replace(/\s+/g, " ");
  }

  function sectionEl(key) {
    const want = SECTIONS[key];
    if (!want) return null;
    const exact = document.querySelector(`[data-testid="section-${want}"]`);
    if (exact) return exact;
    const target = loosen("section-" + want);
    return (
      [...document.querySelectorAll('[data-testid^="section-"]')].find(
        (n) => loosen(n.getAttribute("data-testid")) === target
      ) || null
    );
  }

  function sectionOpen(el) {
    if (!el) return false;
    if (el.hasAttribute("data-open")) return true;
    if (el.hasAttribute("data-closed")) return false;
    // Neither attribute present: fall back to whether it renders any field at all.
    return controls(el).length > 0;
  }

  // Click whatever actually toggles the section, then wait for data-open to appear rather
  // than assuming the click worked.
  async function openSection(el) {
    if (!el || sectionOpen(el)) return sectionOpen(el);
    const trigger =
      el.querySelector('[aria-expanded]:not([aria-haspopup])') ||
      el.querySelector("button, [role='button'], summary") ||
      el.firstElementChild ||
      el;
    for (let tries = 0; tries < 3; tries++) {
      try {
        trigger.click();
      } catch (e) {
        /* a disabled trigger is not an error */
      }
      for (let w = 0; w < 12; w++) {
        await sleep(60);
        if (sectionOpen(el)) return true;
      }
    }
    return sectionOpen(el);
  }

  // Returns the section root to scope lookups to, or null with the reason recorded.
  async function useSection(key, problems) {
    const el = sectionEl(key);
    if (!el) {
      problems.push(
        `section "${SECTIONS[key]}" not found; falling back to a page-wide search`
      );
      return null;
    }
    const ok = await openSection(el);
    if (!ok) problems.push(`section "${SECTIONS[key]}" would not open`);
    return el;
  }

  // Rubric rows are accordions of their own, inside the Task Rubrics section.
  async function expandRows(root) {
    const scope = root || document;
    for (let pass = 0; pass < 4; pass++) {
      // :not([aria-haspopup]) matters. The "Show criteria" buttons in sections 2 and 3
      // also carry aria-expanded="false", and clicking one opens a dialog over the form.
      const shut = [
        ...scope.querySelectorAll('[aria-expanded="false"]:not([aria-haspopup])'),
      ];
      if (!shut.length) break;
      for (const b of shut) {
        try {
          b.click();
        } catch (e) {
          /* ignore */
        }
      }
      await sleep(180);
    }
  }


  // ------------------------------------------------------------ repeatables

  // Known field containers, verified against captures. Anchoring on these rather than on
  // label text removes the ambiguity that several sections share a row heading of "File".
  const FIELD = {
    task_instruction: "field-task-prompt",
    input_files: "field-repeatabletextarea-input_file_list",
    output_files: "field-repeatabletextarea-output_file_list",
    tools: "field-repeatabletextarea-please_insert_any_tool_used_for_this_task_human",
    uploader_inputs: "field-s3fileuploader-file_uploader",
    uploader_solution: "field-s3fileuploader-completed_task_upload",
    checklist:
      "field-multiselect-confirm_each_item_below_applies_to_your_submission_" +
      "before_you_check_it_off_all_boxes_must_be_checked_to_submit_",
  };

  // The checklist's boxes are NOT <input type="checkbox">. Each is a div carrying
  // role="checkbox", aria-checked, and the item's whole text in aria-label, with no
  // <label> wrapper - so the role element is the click target and aria-checked is the only
  // record of state. There are fourteen.
  const BOX_SEL = '[role="checkbox"], input[type="checkbox"]';
  const BOX_COUNT = 14;

  function boxes(root) {
    const field = fieldBox(FIELD.checklist, root);
    return [...(field || root || document).querySelectorAll(BOX_SEL)];
  }

  function boxLabel(b) {
    return norm(b.getAttribute("aria-label") || b.textContent || "");
  }

  function boxTicked(b) {
    return b.checked === true || b.getAttribute("aria-checked") === "true";
  }

  // The five time fields, in the order the form shows them. All five are TEXTAREAS rather
  // than number inputs, and each carries maxlength="5": a total of "10.25" fits exactly and
  // anything longer is truncated by the browser without saying so, which is why the value
  // is measured before it is written.
  const TIME_FIELD = {
    read: "field-textarea-time_to_read_prompt",
    files: "field-textarea-time_to_open_skimsearch_and_use_the_reference_files_human",
    work: "field-textarea-time_to_perform_the_required_work_analysis_writing_calculations_coding_spreadsheet_edits_formatting_human",
    qa: "field-textarea-time_for_verificationqa_and_final_review_human",
    total_hours: "field-textarea-total_time_in_hours",
  };

  // Exact testid first, then a prefix match, so a field whose suffix is renamed still
  // resolves. `within` is the section, which keeps two similarly named fields apart.
  function fieldBox(testid, within) {
    const scope = within || document;
    return (
      scope.querySelector(`[data-testid="${testid}"]`) ||
      document.querySelector(`[data-testid="${testid}"]`) ||
      scope.querySelector(`[data-testid^="${testid.replace(/-[^-]*$/, "")}"]`) ||
      null
    );
  }

  function instancesIn(box) {
    return [...box.querySelectorAll('[data-testid*="-instance-"]')];
  }

  // Rows inside a repeatable. The form renders each as a -instance- container once it
  // exists; before the first Add there are none at all, which is the normal starting
  // state and must not read as a failure.
  // A repeatable's rows are addressed by their CONTROLS, not by a row marker.
  //
  // Two different repeatable components ship on this form and they mark rows differently:
  // the rubric numbers rows as [data-testid*="-instance-N"], the tools list uses
  // [data-testid="field-repeatable-textarea"], and the file lists were only ever captured
  // while EMPTY, so their row markup was an assumption carried over from tools. Writing
  // into "the field inside row i" fails the moment that assumption is wrong, and it fails
  // silently: the rows get added, and every one of them stays blank.
  //
  // So the file and tool lists work off the editable controls the field contains, in
  // document order. A row is whatever holds the nth control. No marker needed.
  function slotsIn(box) {
    return [...box.querySelectorAll("textarea, input")].filter((el) => {
      const t = (el.type || "").toLowerCase();
      if (["file", "hidden", "checkbox", "radio", "button", "submit"].includes(t)) return false;
      if (el.readOnly || el.disabled) return false;
      // a control inside an open "Show criteria" dialog is not part of the list
      if (el.closest('[role="dialog"], [role="alertdialog"]')) return false;
      return true;
    });
  }

  // Describes what a repeatable actually looks like, for the popup's scan. When a list
  // will not fill, this is the line to send back: it names the row markers present, so a
  // wrong assumption about them is visible instead of inferred.
  function describeRepeatable(key, sectionRoot) {
    const box = fieldBox(FIELD[key], sectionRoot);
    if (!box) return { key, found: false };
    const marks = {};
    for (const n of box.querySelectorAll("[data-testid]")) {
      const t = n.getAttribute("data-testid");
      if (t && t !== FIELD[key]) marks[t] = (marks[t] || 0) + 1;
    }
    return {
      key,
      found: true,
      slots: slotsIn(box).length,
      controls: [...box.querySelectorAll("textarea, input")].map(
        (e) => e.tagName.toLowerCase() + (e.type ? ":" + e.type : "")
      ),
      markers: Object.entries(marks).map(([t, n]) => `${t}${n > 1 ? " x" + n : ""}`),
      buttons: [...box.querySelectorAll("button")]
        .map((b) => norm(b.textContent))
        .filter(Boolean),
    };
  }

  // Fill a one-value-per-row repeatable: the input and output file lists, and tools.
  //
  // The list arrives EMPTY for the file lists and with one row for tools, so slots are
  // counted first and the Add button is pressed only for the shortfall.
  async function fillListField(name, key, addRe, values, sectionRoot) {
    const res = {
      name, wanted: values.length, written: 0, rows: 0, added: 0, problems: [],
    };
    if (!values.length) {
      res.problems.push("nothing to write");
      return res;
    }

    let box = fieldBox(FIELD[key], sectionRoot);
    if (!box) {
      const btn = findButton(addRe, sectionRoot);
      if (!btn) {
        res.problems.push(
          `neither [data-testid="${FIELD[key]}"] nor a button matching ${addRe} was found`
        );
        return res;
      }
      box = btn.closest('[data-testid^="field-"]') || btn.parentElement;
      res.problems.push("field container not found; used the add button's field instead");
    }

    const addBtn = findButton(addRe, box) || findButton(addRe, sectionRoot);
    let slots = slotsIn(box);
    const startedWith = slots.length;

    let guard = 0;
    while (slots.length < values.length && addBtn && guard++ < 200) {
      addBtn.click();
      await sleep(160);
      const before = slots.length;
      slots = slotsIn(box);
      if (slots.length === before) {
        // The click produced no new control. Stop rather than spraying clicks.
        res.problems.push(
          `"${norm(addBtn.textContent)}" added no field on click ${guard}; stopped at ` +
            `${slots.length} of ${values.length}`
        );
        break;
      }
    }
    res.rows = slots.length;
    res.added = Math.max(0, slots.length - startedWith);

    if (!slots.length) {
      res.problems.push(
        addBtn
          ? "no editable field in this list even after clicking Add"
          : `no editable field and no button matching ${addRe}`
      );
      return res;
    }
    if (slots.length < values.length) {
      res.problems.push(`only ${slots.length} field(s) for ${values.length} value(s)`);
    }

    // The two file lists want "name - what it contains". A payload whose entries are bare
    // file names still fills without error, and the result looks fine until a reviewer
    // reads it, so say so here rather than letting it through quietly. The usual cause is
    // a payload regenerated on disk while the popup still holds the copy loaded before it.
    if (key === "input_files" || key === "output_files") {
      const bare = values.filter((v) => !/\s[-\u2013\u2014]\s/.test(String(v)));
      if (bare.length) {
        res.problems.push(
          `${bare.length} of ${values.length} entries are a bare file name with no ` +
            `description (first: "${String(bare[0]).slice(0, 48)}"). The form asks for ` +
            `"name - what it contains". If you regenerated form-payload.json, press Load ` +
            `JSON again - the popup keeps the copy you loaded last.`
        );
      }
    }

    values.forEach((v, i) => {
      const el = slots[i];
      if (!el) return;
      const bad = setChecked(el, v);
      if (bad) res.problems.push(`entry ${i + 1}: ${bad}`);
      else res.written++;
    });

    if (slots.length > values.length) {
      res.problems.push(
        `${slots.length - values.length} empty row(s) beyond the ${values.length} supplied; ` +
          "delete them on the form"
      );
    }
    return res;
  }

  // ---------------------------------------------------------------- rubric

  // Verified selectors. The description and weight ids repeat across rows, so both are
  // read from inside the row's own instance container.
  const RUBRIC_GROUP = "repeatable-repeatable-bfbf1";
  const RUBRIC_DESC = '[data-testid="field-textarea-rubric_description"]';
  const RUBRIC_WEIGHT = '[data-testid^="field-numeric-add_a_criteria_weight"]';
  const RUBRIC_ADD = /add a new rubric/i;

  // Rows are counted by their instance containers, which exist whether or not the row is
  // expanded. This is the whole game: on arrival only the FIRST row is open, and rows 2
  // and 3 carry data-hidden/data-closed with no panel in the DOM at all - no description
  // textarea, no weight input. Counting "instances that contain a description field"
  // returns 1 instead of 3, and topping the list up to the criterion count then adds a
  // fresh row for every criterion on top of the three already sitting there.
  function rubricRows(root) {
    const scope = root || document;
    const group = scope.querySelector(`[data-testid="${RUBRIC_GROUP}"]`);
    const within = group || scope;
    const all = [...within.querySelectorAll('[data-testid*="-instance-"]')];
    if (all.length) return all;
    // No instance containers at all: fall back to anything shaped like a rubric row.
    return [...scope.querySelectorAll('[data-testid*="-instance-"]')].filter(
      (n) =>
        n.querySelector(RUBRIC_DESC) ||
        (n.querySelector("textarea") && n.querySelector('input[min="-5"][max="5"]'))
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

  async function fillRubric(criteria, root) {
    const res = { name: "rubric", wanted: criteria.length, written: 0, rows: 0, problems: [] };
    if (!criteria.length) {
      res.problems.push("nothing to write");
      return res;
    }
    const addBtn = findButton(RUBRIC_ADD, root);
    let rows = rubricRows(root);
    const startedWith = rows.length;
    if (!rows.length && !addBtn) {
      res.problems.push("no rubric rows and no \"Add a New Rubric\" button on this page");
      return res;
    }

    // Add only what is missing. rubricRows counts collapsed rows too, so this starts from
    // the real total rather than from the one row that happens to be open.
    let guard = 0;
    while (rows.length < criteria.length && addBtn && guard++ < 400) {
      addBtn.click();
      await sleep(140);
      rows = rubricRows(root);
    }
    res.added = Math.max(0, rows.length - startedWith);

    // Expand every row, then re-read: a collapsed row has no fields to write into.
    await expandRows(root);
    rows = rubricRows(root);
    res.rows = rows.length;

    const stillShut = rows.filter((r) => !rubricFields(r).desc).length;
    if (stillShut) {
      res.problems.push(
        `${stillShut} row(s) would not expand, so their fields could not be reached`
      );
    }
    if (rows.length < criteria.length) {
      res.problems.push(
        `only ${rows.length} rows for ${criteria.length} criteria` +
          (addBtn ? "" : ' (no "Add a New Rubric" button found)')
      );
    }
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

  // VERIFIED against a capture of section 1. Both pickers are exact rather than
  // label-guessed:
  //   the two groups     [data-testid="field-radio-domain"] / "...-occupation"
  //   each option        [data-testid="radio-option-container-<the exact visible label>"]
  //   the clickable bit  button[role="radio"] inside that option
  //
  // The <input type="radio"> sitting next to the button is aria-hidden and clipped to a
  // 1px box, so it is the button that must be clicked, not the input.
  //
  // Each option's button also carries value="<slug>", where the slug is the label
  // lowercased with every run of non-alphanumerics turned into one underscore. That gives
  // a second, punctuation-proof way to match: "Healthcare Practitioners / Support" becomes
  // healthcare_practitioners_support, and "Installation, Maintenance, and Repair" becomes
  // installation_maintenance_and_repair.
  function slugify(s) {
    return low(s).replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
  }

  function radioGroup(which, root) {
    const sel = `[data-testid="field-radio-${which}"]`;
    return (root || document).querySelector(sel) || document.querySelector(sel);
  }

  function optionLabel(node) {
    const tid = node.getAttribute("data-testid") || "";
    return tid.replace(/^radio-option-container-/, "");
  }

  function isChecked(btn) {
    return (
      btn.hasAttribute("data-checked") || btn.getAttribute("aria-checked") === "true"
    );
  }

  // Pick one option out of a named radio group. Returns what it did, or why it could not.
  async function pickRadio(which, wanted, root) {
    if (!wanted) return { ok: false, why: "no value supplied" };
    const group = radioGroup(which, root);
    if (!group) return { ok: false, why: `no ${which} radio group on the page` };

    const options = [...group.querySelectorAll('[data-testid^="radio-option-container-"]')];
    if (!options.length) return { ok: false, why: `the ${which} group has no options` };

    const target = low(wanted);
    const targetSlug = slugify(wanted);
    const score = (o) => {
      const label = optionLabel(o);
      if (low(label) === target) return 3;                 // exact label
      if (slugify(label) === targetSlug) return 2;          // same slug: punctuation-proof
      if (low(label).startsWith(target)) return 1;
      return 0;
    };
    const ranked = options
      .map((o) => ({ o, s: score(o) }))
      .filter((x) => x.s > 0)
      .sort((a, b) => b.s - a.s);

    if (!ranked.length) {
      return {
        ok: false,
        why: `"${wanted}" is not one of the ${options.length} ${which} options`,
        options: options.slice(0, 6).map(optionLabel),
      };
    }
    const best = ranked[0];
    if (ranked.length > 1 && ranked[1].s === best.s) {
      return { ok: false, why: `"${wanted}" matched ${ranked.filter(r => r.s === best.s).length} options` };
    }

    const btn =
      best.o.querySelector('button[role="radio"]') ||
      best.o.querySelector('[role="radio"]') ||
      best.o.querySelector('input[type="radio"]');
    if (!btn) return { ok: false, why: `the "${optionLabel(best.o)}" option has no control` };

    const label = optionLabel(best.o);
    if (isChecked(btn)) return { ok: true, label, already: true };

    btn.click();
    for (let w = 0; w < 12; w++) {
      await sleep(50);
      if (isChecked(btn)) return { ok: true, label };
    }
    // The button did not take; try the wrapping label, then the hidden input.
    const alt = best.o.tagName === "LABEL" ? best.o : best.o.closest("label");
    if (alt) alt.click();
    const hidden = best.o.querySelector('input[type="radio"]');
    if (hidden && !isChecked(btn)) hidden.click();
    await sleep(80);
    return isChecked(btn)
      ? { ok: true, label }
      : { ok: false, why: `clicked "${label}" but it did not become selected` };
  }

  // What the group currently has selected, for reporting and verification.
  function selectedIn(which, root) {
    const group = radioGroup(which, root);
    if (!group) return null;
    const on = [...group.querySelectorAll('[role="radio"]')].find(isChecked);
    if (!on) return null;
    const holder = on.closest('[data-testid^="radio-option-container-"]');
    return holder ? optionLabel(holder) : norm(on.value || "");
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
      checkboxesTicked: checkboxes.filter(boxTicked).length,
      checklistTotal: boxes().length,
      checklistTicked: boxes().filter(boxTicked).length,
      checklistUnticked: boxes()
        .filter((b) => !boxTicked(b))
        .map((b) => boxLabel(b).slice(0, 78)),
      fileInputs: fileInputs.length,
      rubricRows: rubricRows().length,
      selectedDomain: selectedIn("domain"),
      selectedOccupation: selectedIn("occupation"),
      domainOptions: (radioGroup("domain") || document).querySelectorAll
        ? [...(radioGroup("domain") || document).querySelectorAll(
            '[data-testid^="radio-option-container-"]'
          )].length
        : 0,
      occupationOptions: radioGroup("occupation")
        ? [...radioGroup("occupation").querySelectorAll(
            '[data-testid^="radio-option-container-"]'
          )].length
        : 0,
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

  // --------------------------------------------------------------- dispatch

  if (op === "scan") {
    const states = {};
    for (const key of Object.keys(SECTIONS)) {
      const el = sectionEl(key);
      states[SECTIONS[key]] = !el
        ? "not found"
        : (await openSection(el)) ? "open" : "would not open";
    }
    await expandRows(sectionEl("rubric"));
    out.scan = scan();
    out.scan.sectionStates = states;
    out.scan.repeatables = [
      describeRepeatable("input_files", sectionEl("metadata")),
      describeRepeatable("output_files", sectionEl("completed")),
      describeRepeatable("tools", sectionEl("completed")),
    ];
    return out;
  }

  const p = payload || {};
  const want = (k) => op === "fill" || op === "fill:" + k;

  // Section 1 -------------------------------------------------------------
  if (want("identity") && (p.domain || p.occupation)) {
    const r = { name: "domain & occupation", problems: [] };
    const root = await useSection("identity", r.problems);
    // Occupation first: it is the choice grounded in real expertise, and the domain is
    // then the job family that follows from it.
    if (p.occupation) {
      const o = await pickRadio("occupation", p.occupation, root);
      r.occupation = o.ok ? o.label : null;
      if (o.already) r.problems.push("occupation was already selected");
      if (!o.ok) {
        r.problems.push("occupation: " + o.why);
        if (o.options) r.problems.push("  first options seen: " + o.options.join("; "));
      }
    }
    if (p.domain) {
      const d = await pickRadio("domain", p.domain, root);
      r.domain = d.ok ? d.label : null;
      if (!d.ok) r.problems.push("domain: " + d.why);
    }
    // Read the group back rather than trusting the click. The domain arrives with an
    // option already selected, so "it is checked" is not evidence that WE checked it.
    r.selected = {
      domain: selectedIn("domain", root),
      occupation: selectedIn("occupation", root),
    };
    if (p.domain && r.selected.domain && low(r.selected.domain) !== low(p.domain)) {
      r.problems.push(
        `domain reads back as "${r.selected.domain}", not "${p.domain}"`
      );
    }
    if (
      p.occupation &&
      r.selected.occupation &&
      low(r.selected.occupation) !== low(p.occupation)
    ) {
      r.problems.push(
        `occupation reads back as "${r.selected.occupation}", not "${p.occupation}"`
      );
    }
    out.sections.identity = r;
  }

  // Section 2 -------------------------------------------------------------
  if (want("instruction") && p.task_instruction) {
    const r = { name: "task instruction", problems: [] };
    const root = await useSection("metadata", r.problems);
    const box = fieldBox(FIELD.task_instruction, root);
    const el =
      (box && (box.querySelector("#task-prompt") || box.querySelector("textarea"))) ||
      byLabel(/task instruction/i, { root }) ||
      [...(root || document).querySelectorAll("textarea")].find((t) =>
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
    const problems = [];
    const root = await useSection("metadata", problems);
    const res = await fillListField(
      "input file list",
      "input_files",
      /add another input file/i,
      p.input_files,
      root
    );
    res.problems = problems.concat(res.problems);
    out.sections.input_files = res;
  }

  // Section 3 -------------------------------------------------------------
  if (want("outputs") && (p.output_files || []).length) {
    const problems = [];
    const root = await useSection("completed", problems);
    const res = await fillListField(
      "output file list",
      "output_files",
      /add another output file/i,
      p.output_files,
      root
    );
    res.problems = problems.concat(res.problems);
    out.sections.output_files = res;
  }

  if (want("times") && p.times) {
    const r = { name: "times", written: 0, problems: [] };
    const root = await useSection("completed", r.problems);
    for (const key of Object.keys(TIME_FIELD)) {
      const v = p.times[key];
      if (v === undefined || v === null || v === "") continue;
      const box = fieldBox(TIME_FIELD[key], root);
      const el = box && (box.querySelector("textarea") || box.querySelector("input"));
      if (!el) {
        r.problems.push(`no field for ${key} ([data-testid="${TIME_FIELD[key]}"])`);
        continue;
      }
      const bad = setChecked(el, v);
      if (bad) r.problems.push(`${key}: ${bad}`);
      else r.written++;
    }
    // The form's own rule, checked here so a bad total is caught before submitting.
    const mins = ["read", "files", "work", "qa"].map((k) => Number(p.times[k]));
    const total = Number(p.times.total_hours);
    if (mins.every((m) => Number.isFinite(m) && m > 0) && Number.isFinite(total)) {
      const floor = mins.reduce((a, b) => a + b, 0) / 60;
      if (total + 1e-9 < floor) {
        r.problems.push(
          `total ${total}h is below the four parts (${mins.reduce((a, b) => a + b, 0)} min ` +
            `= ${floor.toFixed(2)}h); the form requires at least their sum`
        );
      }
      if (total < 3) {
        r.problems.push(`total ${total}h is under the 3-hour difficulty floor`);
      }
    }
    out.sections.times = r;
  }

  if (want("tools") && (p.tools || []).length) {
    const problems = [];
    const root = await useSection("completed", problems);
    const res = await fillListField("tools", "tools", /add another tool/i, p.tools, root);
    res.problems = problems.concat(res.problems);
    out.sections.tools = res;
  }

  // Section 4 -------------------------------------------------------------
  if (want("rubric") && (p.rubric || []).length) {
    const problems = [];
    const root = await useSection("rubric", problems);
    const res = await fillRubric(p.rubric, root);
    res.problems = problems.concat(res.problems);
    out.sections.rubric = res;
  }

  // Section 5 -------------------------------------------------------------
  // Opt-in only. Each box is an attestation about the package, so ticking them is never
  // part of "fill everything"; the operator asks for it separately and deliberately.
  if (op === "fill:checklist") {
    const problems = [];
    const root = await useSection("checklist", problems);
    const all = boxes(root);

    if (all.length !== BOX_COUNT) {
      problems.push(
        `found ${all.length} boxes, expected ${BOX_COUNT}; the checklist has changed, so ` +
          "read it yourself before submitting"
      );
    }

    let ticked = 0;
    const stuck = [];
    for (const b of all) {
      if (boxTicked(b)) continue;
      if (b.getAttribute("aria-disabled") === "true" || b.disabled) {
        stuck.push(boxLabel(b));
        continue;
      }
      b.click();
      await sleep(50);
      // aria-checked is the only state here, so confirm it actually flipped.
      if (boxTicked(b)) ticked++;
      else stuck.push(boxLabel(b));
    }

    for (const label of stuck) {
      problems.push(`did not tick: ${label.slice(0, 90)}`);
    }

    out.sections.checklist = {
      name: "checklist",
      boxes: all.length,
      ticked,
      remaining: all.filter((b) => !boxTicked(b)).length,
      problems,
    };
  }

  // Uploads ---------------------------------------------------------------
  const files = [...document.querySelectorAll('input[type="file"]')];
  if (files.length) {
    const named = files
      .map((f) => {
        const box = f.closest('[data-testid^="field-"]');
        const l = box && box.querySelector("label");
        return l ? norm(l.textContent) : null;
      })
      .filter(Boolean);
    out.skipped.push(
      `${files.length} upload field(s) left alone` +
        (named.length ? ` (${named.join(", ")})` : "") +
        " - a page cannot set a file input from a path, so both zips are yours to attach"
    );
  }

  if (!Object.keys(out.sections).length) {
    out.ok = false;
    out.notes.push("nothing matched: is the right form section open on this tab?");
  }
  return out;
}
