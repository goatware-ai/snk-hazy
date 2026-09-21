// Tests for the pure CSV helpers. There is no node on the build machine, so run
// these with the JavaScriptCore shell that ships with macOS:
//
//   /System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc test.js
//
// or, with node available:  node test.js
if (typeof load === "function") load("csv.js");
else Object.assign(globalThis, require("./csv.js"));

const say = typeof print === "function" ? print : console.log;
let failures = 0;
let ran = 0;

function eq(actual, expected, what) {
  ran++;
  const a = JSON.stringify(actual);
  const e = JSON.stringify(expected);
  if (a !== e) { failures++; say(`FAIL ${what}\n  expected ${e}\n  actual   ${a}`); }
}

function throws(fn, re, what) {
  ran++;
  try { fn(); } catch (e) {
    if (!re.test(e.message)) { failures++; say(`FAIL ${what}\n  message ${e.message} does not match ${re}`); }
    return;
  }
  failures++;
  say(`FAIL ${what}: expected a throw`);
}

// ---- parseCsv ----
eq(parseCsv("a,b\n1,2\n"), [["a", "b"], ["1", "2"]], "plain rows");
eq(parseCsv('a,"b,c"\n'), [["a", "b,c"]], "quoted comma");
eq(parseCsv('a,"line1\nline2"\n'), [["a", "line1\nline2"]], "quoted newline");
eq(parseCsv('a,"say ""hi"""\n'), [["a", 'say "hi"']], "doubled quotes");
eq(parseCsv("a,b\r\n1,2\r\n"), [["a", "b"], ["1", "2"]], "CRLF");
eq(parseCsv("﻿a,b\n"), [["a", "b"]], "BOM stripped");
eq(parseCsv("a,b\n\n\n1,2"), [["a", "b"], ["1", "2"]], "blank rows dropped");
eq(parseCsv("a,b"), [["a", "b"]], "no trailing newline");

// ---- rowsToItems ----
const three = parseCsv("NUMBER,CRITERION,WEIGHT\n1,Does a thing.,4\n2,Does another.,-3\n");
eq(rowsToItems(three).hasReq, false, "3-column rubric has no REQ");
eq(rowsToItems(three).items, [
  { "numeric-weight": 4, "textarea-criterion": "Does a thing.", req: "" },
  { "numeric-weight": -3, "textarea-criterion": "Does another.", req: "" },
], "3-column rows");

const four = parseCsv("NUMBER,CRITERION,WEIGHT,REQ\n1,Does a thing.,4,FILE\n2,Does another.,1,EXC\n");
eq(rowsToItems(four).hasReq, true, "4-column rubric has REQ");
eq(rowsToItems(four).items.map((i) => i.req), ["FILE", "EXC"], "REQ carried through");

eq(rowsToItems(parseCsv("weight,criterion\n4,Does a thing.\n")).items[0]["numeric-weight"], 4,
  "header column order does not matter");

// Headerless: the numeric column is the weight, whichever side it is on.
eq(rowsToItems(parseCsv("4,Does a thing.\n")).items[0]["textarea-criterion"], "Does a thing.",
  "headerless, weight first");
eq(rowsToItems(parseCsv("Does a thing.,4\n")).items[0]["numeric-weight"], 4,
  "headerless, weight second");

// The bug this guards: a headerless first row whose criterion mentions "weight"
// used to be swallowed as a header row.
eq(rowsToItems(parseCsv('4,"The net weight is stated in kilograms."\n1,Second.\n')).items.length, 2,
  'headerless row mentioning "weight" is kept');

throws(() => rowsToItems(parseCsv("NUMBER,CRITERION,WEIGHT\n1,Does a thing.,2.5\n")),
  /line 2:.*not a whole number/i, "fractional weight rejected");
throws(() => rowsToItems(parseCsv("NUMBER,CRITERION,WEIGHT\n1,Does a thing.,4abc\n")),
  /not a whole number/i, "trailing garbage in weight rejected");
throws(() => rowsToItems(parseCsv("NUMBER,CRITERION,WEIGHT\n1,Fine.,4\n2, ,1\n")),
  /line 3: empty criterion/i, "empty criterion rejected, line number counts the header");
throws(() => rowsToItems([]), /empty/i, "empty CSV rejected");

// ---- weightTotals ----
eq(weightTotals(rowsToItems(three).items), { count: 2, pos: 4, neg: -3, net: 1 }, "totals");

// ---- toRubricCsv ----
const out3 = toRubricCsv([{ criterion: "Does a thing.", weight: "4", req: "FILE" }], false);
eq(out3, "﻿NUMBER,CRITERION,WEIGHT\n1,Does a thing.,4\n", "3-column output ignores req");
const out4 = toRubricCsv([{ criterion: "A, with comma", weight: "1", req: "EXC" }], true);
eq(out4, '﻿NUMBER,CRITERION,WEIGHT,REQ\n1,"A, with comma",1,EXC\n', "4-column output, minimal quoting");

// Round trip: parse a repo-shaped rubric and write it back unchanged.
const src = "﻿NUMBER,CRITERION,WEIGHT,REQ\n1,Plain row.,1,FILE\n2,\"Quoted, row.\",4,EXC\n";
const back = rowsToItems(parseCsv(src));
eq(toRubricCsv(back.items.map((i) => ({ criterion: i["textarea-criterion"], weight: i["numeric-weight"], req: i.req })), back.hasReq),
  src, "round trip is byte identical");

// ---- taskNameFromFilename ----
eq(taskNameFromFilename("rubric-sample-task-7373c89f.csv"),
  { taskName: "sample-task", uid8: "7373c89f" }, "submission file name");
eq(taskNameFromFilename("rubric-sample-task.csv"),
  { taskName: "sample-task", uid8: "" }, "draft file name, no UID");
eq(taskNameFromFilename("something-else.csv"), { taskName: "", uid8: "" }, "unrecognised name");

say(failures ? `\n${failures} of ${ran} checks FAILED` : `all ${ran} checks passed`);
if (typeof quit === "function") quit(failures ? 1 : 0);
