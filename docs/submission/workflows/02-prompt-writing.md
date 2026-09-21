# Workflow 02 — Prompt Writing: your voice, a real situation

The platform states the prompt rules once: voice, required properties, the "You are a ..."
opener and overspecification in `../platform/project-guidelines-v5.1.md#your-prompt`, and
the tell list in
`../platform/project-guidelines-v5.1.md#how-to-tell-if-your-prompt-sounds-llm-generated`.
This page holds only what the house adds on top. Coded rules carry their check id; the
one-line statement of every id is `../../rules.md`.

## House rules the platform does not state

- **One primary deliverable, named** (P1). The Prompt Quality Check rejects two co-equal
  required output files; fold companion outputs into the single artifact. See
  `06-metadata.md#house-notes-on-platform-submission-formmd`.
- **Every input file named in the opening paragraph, woven into the narrative** (P2, P3).
  A separate "here are the pulls" inventory paragraph is flagged even when every file is
  named.
- **Gloss at most one or two files** (P5). Saying what most named files are for fails the
  platform's Prompt human voice check even in a human voice; name them all in one run and
  gloss only the one or two whose distinction is unclear.
- **Fit the 3,000-character field** with headroom.
- **Ask for the answer the requester does not want.** Name the adverse result the requester
  is prepared to hear and make the files capable of producing it: it gives the requester a
  real motive, forces the golden to carry a finding against interest, and gives the rubric a
  criterion a model playing along will miss.

## The opening frame (P4, P6)

The first paragraph or two, roughly the first 900 characters, must carry three things,
written as the requester talking, never as an instruction to the solver:

- **P4a the place.** The state, or the country plainly. A town name does not carry it.
- **P4b the role.** What the requester does. "my desk" does not count.
- **P4c the expertise.** What the reader is expected to already know, in purchasing or
  procurement terms.
- **P4d not a persona.** Never "You are a financial analyst. Utilizing your expertise ...".

And none of it as a self-introduction to a coworker (P6):

- The place rides on something the work touches ("the pipe yard here in Chattanooga,
  Tennessee"), never "<Company>, a <trade> wholesaler in <Town>, <State>" told to a
  colleague who works there.
- The role is ownership of the problem ("the trucks are mine to settle"), never a job
  description.
- The experience is the reason for the handoff, addressed to the reader ("you have a few
  years of distribution operations behind you"), never "whoever picks this up should
  have ...", which gates a stranger.
- Every event the opening names says in the same sentence why it matters to the work.

✅ "Four of our trucks come off the Cumberland lease on December 31, and Darrell wants the
whole fleet settled before then. I run the warehouse and the pipe yard here in Chattanooga,
Tennessee, so the trucks are mine to settle, and I am handing this to you because you have a
few years of distribution operations behind you and will not need the lease schedules walked
through."

P4 reads the three parts out of the opening window and fires separately on the persona
shape; P6 fires on the self-introduction sentence and the "whoever picks this up" gate. The
rest is a read. history:
`../../reference/workflow-history.md#open-order-cleanup-rejected-on-prompt-quality-2026-09-02`,
`../../reference/workflow-history.md#lift-truck-fleet-plan-rejected-at-first-human-review-2026-09-05`.

## Sentence mechanics (A20)

- A comma before and/but/so/or joining two independent clauses.
- Never a third independent clause in one sentence.
- The serial comma in every list.

A20 codes the first two shapes; the serial comma, the comma splice and compound sentences
inside a subordinate clause are a read. It applies to the prompt, every input document,
every golden text cell and the rubric. history:
`../../reference/workflow-history.md#lift-truck-fleet-plan-rejected-at-first-human-review-2026-09-05`.

## Overspecification giveaways beyond step-by-step

The guidelines say what, not how. Reviewers also send back these subtler forms:

- Saying what a file is for (P5); name it and what it contains, and let how it enters the
  analysis be the solver's discovery.
- Outlining the sections of a deliverable component; the component and its audience are
  enough.
- Warning about data pitfalls; if spotting bad rows or an atypical period is graded, the
  warning hands it over.
- Stating derived parameters; a horizon, cutoff or scope the solver computes from scenario
  facts must not appear as a given.
- Enumerating the decision framework an input file teaches (the disposition options, the
  cap that binds).
- An inventory paragraph of file names (P3).

At the same time the prompt must be complete: every requirement the rubric grades is stated
or is a thing any competent practitioner would know to do (R4, R13). Hidden requirements are
a rubric defect, not difficulty. history:
`../../reference/workflow-history.md#weldon-transition-buy-reviewer-feedback-august-2026`,
`../../reference/workflow-history.md#yearend-deadstock-plan-reviewer-feedback-august-2026`.

## House notes on platform-submission-form.md

The form's O*NET checks, as observed on submissions. The narratives behind each rule are in
`../../reference/workflow-history.md#onet-occupation-and-task-pick-checks-twincreek-frankfort-kolterman-drafts-23-to-40-task-45-august-to-september-2026`.

- **The Occupation prompt relevance check reads the prompt's actual work and distinguishes
  buy-side from sell-side** (M1). 13-1022 covers purchasing merchandise for resale; a prompt
  centered on pricing or submitting a bid or quote to a customer fails under it. Sell-side
  prompts go to 41-4012.00 Sales Representatives, Wholesale and Manufacturing, Except
  Technical and Scientific Products, whose task list carries "Estimate or quote prices,
  credit or contract terms, warranties, and delivery dates.", "Negotiate details of
  contracts and payments." and "Monitor market conditions, product innovations, and
  competitors' products, prices, and sales." Pick "Prepare drawings, estimates, and bids
  that meet specific customer needs." only when the prompt prepares a bid.
- **The same check fails on framing, not just on fit** (M3). Under 13-1022, lead the ask
  with the merchandise question, list the stock, item, movement, backlog and supplier-price
  files first, let another domain's documents enter as the basis each class of material is
  valued on, put the buy-side work ahead of that domain's closing figure, and name the
  deliverable for the merchandise work (the check reads the file name in the prompt).
- **When the rejection names duties rather than emphasis, the occupation is wrong and no
  wording pass will save it.** The Wholesale Trade industry filter
  (onetonline.org/find/industry?i=42) lists 63 occupations; the platform's sector table has
  51 of them (`../platform/platform-wholesale-trade-occupations.md`). 11-3071.00
  Transportation, Storage, and Distribution Managers owns warehouse loss work ("Develop and
  document standard and emergency operating procedures for receiving, handling, storing,
  shipping, or salvaging products or materials", "Monitor inventory levels of products or
  materials in warehouses", "Resolve problems concerning transportation, logistics systems,
  imports or exports, or customer issues", "Collaborate with other departments to integrate
  logistics with business systems or processes, such as customer sales, order management,
  accounting, or shipping", "Examine invoices and shipping manifests for conformity to
  tariff and customs regulations", "Negotiate with carriers, warehouse operators, or
  insurance company representatives"). Do not pick its supervisory, safety-program, budget,
  import/export, carrier-rate-negotiation, drone or energy tasks for an analyst prompt (M2
  errors on all seven).
- **The ONET Occupation-Sector Match uses the platform's own occupation-to-sector table.**
  It carries no accounting, bookkeeping or billing occupation: 13-2011 and 43-3031 fail as
  "Professional, Scientific, and Technical Services" only, whatever the relevance reading
  says. Pick only from the table.
- **Task picks are checked separately from the occupation.** The Skills prompt relevance
  check reads every selected task against the prompt and fails the whole section when one
  pick leans on a headline duty the prompt never asks for (M2). There is no default block:
  pick the 3 to 5 tasks off what the prompt has the solver do, and be able to name the
  prompt clause behind each pick. The 13-1022 map from work to task number:

| The prompt has the solver... | Task |
| --- | --- |
| work supplier terms, freight terms, zone rates, a rebate program | #2 |
| decide what to stock, what to convert, what to drop on specification or quality | #3 |
| set or defend sell prices, margins, mark-ups or mark-downs | #4 |
| gather what customers or jobs require through sales or purchasing people | #5 |
| work a return, a credit claim, an invoice discrepancy or a chargeback | #6 |
| read usage, movement or sales history to size what is needed | #7 |
| work the vendor directly for product, terms clarifications or supply dates | #8 |
| judge stock condition, date codes, quality, value or yield | #9 |
| consult managers about a purchasing budget or an assortment decision | #11 |
| place the buy itself, for resale | #1 |

- **Skills dropdowns without Mathematics:** 41-4012 (use Complex Problem Solving), 11-3071
  and 43-4041 (Reading Comprehension, Critical Thinking, Judgment and Decision Making,
  Complex Problem Solving, Writing). 11-2022's essential list is Active Listening,
  Speaking, Critical Thinking, Monitoring, Reading Comprehension, Active Learning, Writing,
  Learning Strategies and Mathematics. 43-4151 Order Clerks' is Active Listening, Speaking,
  Reading Comprehension, Critical Thinking, Monitoring, Writing, Active Learning and
  Mathematics.

## House notes on platform-wholesale-trade-occupations.md

**Not on the table, and rejected by the sector match:**

- 53-1047.00 First-Line Supervisors of Transportation and Material Moving Workers: listed on
  the O*NET industry page but disabled there, with empty platform task and skill dropdowns.
  Never pick it.
- 13-2011.00 Accountants and Auditors (platform: Professional, Scientific, and Technical
  Services only).
- 43-3031.00 Bookkeeping, Accounting, and Auditing Clerks (same).
- 43-3021.00 Billing and Posting Clerks (not on the list; never tried).

The table carries no accounting, bookkeeping or billing occupation; an audit-shaped prompt
goes on one of the analytical occupations below.

**Which occupation for which prompt** (verified on the Occupation prompt relevance check
unless marked pending; the task names are the evidence, detailed in
`../../reference/workflow-history.md`):

| Prompt's center | Occupation | Status |
| --- | --- | --- |
| Buying merchandise for resale, supplier increase, program buy, stocking decisions | 13-1022.00 Wholesale and Retail Buyers | passed (tasks 01-07, 09-12, 14-21) |
| Pricing or bidding to a customer, quoting, agreement renewal | 41-4012.00 Sales Representatives, Wholesale (no Mathematics skill) | passed (twincreek) |
| Warehouse loss, salvage, inventory at the building, receiving and distribution operations | 11-3071.00 Transportation, Storage, and Distribution Managers (no Mathematics skill) | passed (frankfort); failed on a customer backcharge dispute: delivery records as evidence do not make it distribution work |
| Physical count reconciliation, cutoff and receiving errors, stock adjustment, transfer versus buy replenishment | 11-3071.00 (monitor inventory levels in warehouses; SOPs for receiving, handling and storing; resolve logistics problems; collaborate with accounting and order management) | pending (task 18, after 13-1022 failed naming count and reorder-point duties it does not carry) |
| Customer dispute or complaint over sales and service: backcharges, credits, terms of sale, receivable | 11-2022.00 Sales Managers (resolve customer complaints regarding sales and service; review sales and service accounting and record-keeping, receiving and shipping) | pending (after 11-3071 failed) |
| Sell-price audit, invoice corrections and credits, margin review, pricing controls | 11-2022.00 Sales Managers (determine price schedules and discount rates; review operational records for profitability; resolve customer sales complaints; no Mathematics needed) | passed (after 13-1022 and 41-4012 failed relevance) |
| Alternative for the same, clerical framing | 43-4151.00 Order Clerks (verify order information for correctness; compute total charges; prepare invoices; calculate statistics and prepare reports for management; Mathematics in Skills) | untried, O*NET-verified wording on file |
| Purchasing policy, contract conformance, vendor program administration | 11-3061.00 Purchasing Managers | untried |
| Vendor bankruptcy exposure, claims against a supplier, credits/deposits recovery, supplier agreement decision | 11-3061.00 Purchasing Managers (resolve vendor or contractor grievances and claims against suppliers; represent companies in negotiating contracts and formulating policies with suppliers; review purchase order claims and contracts for conformance to company policy; Mathematics in its essential Skills, Judgment and Decision Making not) | pending (pavelka, after 13-1022 failed as financial analysis rather than buying) |
| Customer credit application workup: references, statement ratios, job exposure, security conditions | 43-4041.00 Credit Authorizers, Checkers, and Clerks (no Mathematics; Reading Comprehension, Critical Thinking, Writing passed) | passed (wanasek-credit-workup, occupation and tasks/skills checks) |

Two rejection texts worth recognising: "not on purchasing merchandise or performing
wholesale/retail buyer duties" and "primarily analytical and file-maintenance work rather
than the direct wholesale selling activities". Both name duties, so the fix is the
occupation, not the prompt.

## Final screen before moving on

- [ ] Reads like you talking to a colleague; passed the read-aloud test (A10, P7)
- [ ] Context (who / for whom / why now) present and specific
- [ ] **P4:** the opening names the state (or the US), what the requester does, and the
      purchasing experience the reader brings, in the requester's voice
- [ ] **P6:** none of that is a self-introduction to a coworker; every event the opening
      names says in the same sentence why it matters
- [ ] **A20:** a comma before and/but/so/or joining two clauses, never three clauses in one
      sentence, a serial comma in every list
- [ ] One output file named exactly (P1); every input file named in the opening paragraph
      (P2, P3), at most one or two glossed (P5)
- [ ] Not answerable without the input files
- [ ] What, not how: none of the six giveaway forms above
- [ ] No spelling or grammar errors

Next: `03-input-files.md`
