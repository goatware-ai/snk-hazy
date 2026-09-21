// Pure CSV helpers, shared by popup.js and by test.js. Nothing here touches the
// DOM or a chrome API, so `jsc test.js` can exercise all of it.

// ---------- reading ----------

// RFC 4180: quoted fields, embedded commas and newlines, doubled quotes.
function parseCsv(text) {
  text = text.replace(/^﻿/, ""); // strip UTF-8 BOM
  const rows = [];
  let row = [];
  let field = "";
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; }
        else inQuotes = false;
      } else field += c;
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ",") {
      row.push(field); field = "";
    } else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); field = "";
      rows.push(row); row = [];
    } else field += c;
  }
  if (field !== "" || row.length) { row.push(field); rows.push(row); }
  return rows.filter((r) => r.some((cell) => cell.trim() !== ""));
}

// FileReader.readAsText assumes UTF-8, so an Excel "CSV UTF-16" save comes back
// as mojibake rather than as an error. Sniff the BOM and decode accordingly.
function decodeCsvBytes(buf) {
  const b = new Uint8Array(buf);
  if (b.length >= 2 && b[0] === 0xff && b[1] === 0xfe)
    return new TextDecoder("utf-16le").decode(b);
  if (b.length >= 2 && b[0] === 0xfe && b[1] === 0xff)
    return new TextDecoder("utf-16be").decode(b);
  return new TextDecoder("utf-8").decode(b);
}

// Rows -> { items, hasReq }. REQ is repo-side metadata the form has no field
// for, so it is carried through untouched purely so an export can put it back.
function rowsToItems(rows) {
  if (!rows.length) throw new Error("CSV is empty");

  const head = rows[0].map((c) => c.trim().toLowerCase());
  const findCol = (re) => head.findIndex((h) => re.test(h));
  const headWeight = findCol(/weight/);
  const headCriterion = findCol(/criteri/);

  // A header row has to name BOTH columns. Accepting either one on its own
  // silently ate the first data row of a headerless CSV whose criterion text
  // happened to contain the word "weight".
  const hasHeader = headWeight !== -1 && headCriterion !== -1;
  let cols;
  let dataRows;
  if (hasHeader) {
    cols = { weight: headWeight, criterion: headCriterion, req: findCol(/^req$/) };
    dataRows = rows.slice(1);
  } else {
    dataRows = rows;
    const first = rows[0];
    if (first.length < 2) throw new Error("Need at least 2 columns (weight, criterion)");
    const w0 = /^-?\d+$/.test(first[0].trim());
    cols = { weight: w0 ? 0 : 1, criterion: w0 ? 1 : 0, req: -1 };
  }

  const items = dataRows.map((r, i) => {
    const line = i + 1 + (hasHeader ? 1 : 0); // the CSV's own line number
    const rawWeight = (r[cols.weight] ?? "").trim();
    const criterion = (r[cols.criterion] ?? "").trim();
    // parseInt would take "2.5" as 2 and "4abc" as 4, both silently.
    if (!/^-?\d+$/.test(rawWeight))
      throw new Error(`Line ${line}: weight "${rawWeight}" is not a whole number`);
    if (!criterion) throw new Error(`Line ${line}: empty criterion text`);
    return {
      "numeric-weight": parseInt(rawWeight, 10),
      "textarea-criterion": criterion,
      req: cols.req === -1 ? "" : (r[cols.req] ?? "").trim(),
    };
  });

  if (!items.length) throw new Error("CSV has a header but no criteria");
  return { items, hasReq: cols.req !== -1 };
}

// The rubric rules turn on these totals (positive ceiling, negative share), so
// the popup shows them before anything reaches the form.
function weightTotals(items) {
  let pos = 0;
  let neg = 0;
  for (const it of items) {
    const w = it["numeric-weight"];
    if (w >= 0) pos += w;
    else neg += w;
  }
  return { count: items.length, pos, neg, net: pos + neg };
}

// ---------- writing ----------

function csvField(v) {
  const s = String(v ?? "");
  return /[",\r\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

// Matches the repo's rubric-{task-name}-{uid8}.csv byte for byte: BOM, header,
// LF line endings, minimal quoting. The REQ column is written only when the
// loaded CSV had one, since the older tracked rubrics are three columns wide.
function toRubricCsv(rows, withReq) {
  const lines = [withReq ? "NUMBER,CRITERION,WEIGHT,REQ" : "NUMBER,CRITERION,WEIGHT"];
  rows.forEach((r, i) => {
    const cells = [i + 1, csvField(r.criterion), csvField(r.weight)];
    if (withReq) cells.push(csvField(r.req));
    lines.push(cells.join(","));
  });
  return "﻿" + lines.join("\n") + "\n";
}

// ---------- file name ----------

// The task name lives in the file name itself: submissions/{seq}-{task-name}/
// carries its rubric as rubric-{task-name}-{uid8}.csv, a draft as the same name
// without the UID suffix. File.name is the only thing the browser exposes (never
// the full path), and the UID suffix is eight hex digits, which no task name
// ends in, so stripping it cannot eat a real trailing name segment.
function taskNameFromFilename(name) {
  const m = String(name).match(/^rubric-(.+?)(?:-([0-9a-f]{8}))?\.csv$/i);
  return { taskName: m ? m[1] : "", uid8: m && m[2] ? m[2].toLowerCase() : "" };
}

if (typeof module !== "undefined") {
  module.exports = { parseCsv, rowsToItems, weightTotals, csvField, toRubricCsv, taskNameFromFilename, decodeCsvBytes };
}
