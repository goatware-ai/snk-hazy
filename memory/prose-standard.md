---
name: prose-standard
description: "The prose reviewers send back in prompt, inputs, golden text cells AND rubric alike: zero em dashes (A6), the three-beat LLM rhythm and its seven classes plus aphoristic parallelism, fragment openers and performed urgency (A10, full history in docs/reference/llm-prose-tells.md), comma rules (A20: comma before a clause-joining conjunction, never three clauses, serial comma), comma splices, two-ways-at-once sentences, plural-noun-singular-verb, slogan headers, desk slang in criteria; 'partially' never 'partly' in review notes"
metadata:
  type: feedback
---

Reviewers read the prompt, the input documents, the golden's prose and the rubric under one
standard, and reject as well as send back on it (task 45, first human review). Correct, ordinary
punctuation reads MORE human here; the practitioner voice pushes toward clipped, breathless
prose, which is exactly the register reviewers call "an LLM trying too hard to sound like a real,
rushed, busy person". The P4/P6 prompt frame is in [[prompt-overspecification-giveaways]].

**Zero em dashes** in every task artifact (docx inputs, prompt.md, the rubric CSV, golden text
cells, review notes): commas, colons, semicolons or parentheses instead; a plain hyphen is fine
in subject lines. Density is the tell (task 07 failed at 4 per 191 words). Coded A6: docx ERROR
at >= 4 dashes and >= 12/1000 words, WARN at >= 3 and >= 8; ANY em dash in prompt.md or the
rubric CSV warns. Adding a comma to an unquoted CRITERION field breaks the CSV row; quote it.

**The three-beat rhythm, not a word list** (task 12, 2026-08-22): "messy workplace detail -->
artificial shorthand/idioms --> analytical requirement", the aphorism in the middle carrying no
information. Seven classes with verbatim history and a fix for each in
`docs/reference/llm-prose-tells.md`, read before writing any prompt, input or briefing:
tautologies ("Committed work is committed", ERROR under A10), slogans ("September is use it or
lose it"), idiom standing in for a quantity ("where we are naked"), compressed first-person
filler ("I pulled the rest"), fragments as headings, em dashes, run-ons and comma splices; added
2026-08-31: aphoristic parallelism (the semicolon-balanced maxim), scene-setting fragment
openers ("Word travels."), and urgency performed instead of stated (write "This is urgent" plus
the deadline; someone with a truly urgent issue does not speak in images). A10 scans prompt.md,
every input docx and the solution's text cells; treat a clean A10 as the floor and read aloud.
Elliptical trade jargon reads as a typo to the spelling check ("at the counter day Friday");
keep the noun, frame it grammatically.

**Comma rules, in the reviewer's words** (task 45 rejection, 2026-09-05): a comma before the
conjunction that joins two independent clauses ("When two sentences are joined with 'and' or
'so' or 'but' ... they need a comma"); never a third independent clause in one sentence, whatever
the conjunction; a serial comma in every list ("tires, forks, and damage"). Coded A20
(REV-REGISTER) for the two mechanical shapes (a bare conjunction opening a new subject and verb;
three or more clauses); the serial comma and the comma splice stay a read. Its first sweep fired
on every task, which is the habit, not noise.

**The send-back classes from open-order-cleanup (2026-08-21 and 08-24):** comma splices ("Let me
know before Labor Day if you want that trimmed, it is easy now"); the missing comma before a
coordinating conjunction; slogan sentences and rhetorical paragraph openers in the memo AND the
golden's briefing ("Where the desk stands", "What comes off": open a paragraph on its subject);
over-explaining the deliverable to itself ("which is on the Exceptions sheet with the
arithmetic"); a sentence that points two ways at once ("takes effect on anything unshipped, which
is how the pages have always read"); plural-noun-singular-verb ("our minimum on stock orders is
$500" went back; "our minimum on a stock order is $500" is the fix); run-ons chained with and/so
(flyer-program-review round 4). **The rubric is prose too**: desk register in criteria (trimmed,
comes off the book, worked off, stands at, the desk converts) is slang and becomes plain
professional English (reduced in quantity, removed from the open commitment, calculated from,
remains at, the plan converts); anchors and figures survive the rewrite.

**How to apply:** plain, correctly punctuated sentences everywhere; before zipping sweep every
docx paragraph, the prompt and every workbook text cell for `, (it|we|they|there|that|this|the
X is)` and check each hit is a subordinate clause; audit for independent clauses chained with
and/so. In review notes write "partially", never "partly" (operator, 2026-09-03; neither is a
tell, the desk picks one form), see [[review-task-workflow]].

**Verbless fragments fail the platform's Prompt spelling and grammar check (boettcher Refinery pre-submission, 2026-09-11):** "One workbook back, named X.xlsx" and "The program order sized item by item" were called malformed; write the deliverable ask as a full sentence ("Build one workbook, named X.xlsx. It carries ...").
- 2026-09-11 (hathi refinement round 4, A21): the platform's authorship reader fails a docx whose sections
  all run one status-report skeleton ("remained / continue according to procedure; No X was reported"),
  MEDIUM on an input at llm-only 0.50; A10 never sees it because each sentence is clean on its own. A21
  errors at half or more of a document's sentences on the skeleton; vary the shape section by section.
- 2026-09-15 (rfq-response refinement 253bad46, in-app Rubric objectivity check): "defensible" in a criterion ("no item or defensible alternate in the range") is an unanchored judgment term even beside a count. Anchor the quality to the record that decides it ("neither a matching item nor an alternate listed in the cross reference"), after checking the record really says so. The gate's judgment-term list does not carry "defensible"; words like defensible, credible, reasonable-looking and viable belong on the watch list for criteria.
