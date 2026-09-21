---
name: onet-occupation-routing
description: "Which Wholesale Trade occupation and task picks survive the platform's occupation and skills relevance checks (M1/M2/M3, eight failure modes to 2026-09-17), the per-prompt routing rules, dropdown facts (no Mathematics under 41-4012 / 11-3071 / 43-4041, 43-5071 is shipping-only, 53-1047 disabled) and where the full table lives (docs/submission/platform/platform-wholesale-trade-occupations.md)"
metadata:
  type: project
---

Pick only from the platform's Wholesale Trade list, captured with the per-prompt routing table
in `docs/submission/platform/platform-wholesale-trade-occupations.md` (moved out of memory
2026-08-22). Task picks go verbatim from the dropdown into `metadata.json`
([[task-metadata]]). Reviewers do not review O*NET metadata; the evals team owns it, so M1/M2/M3
answer to that team. Narratives of the seven failure modes: docs/reference/reviewer-feedback-corpus.md
Part 5 (tasks 08, 13, 22, 23, 32, 48, 51).

## The two checks

- **Occupation prompt relevance** judges the occupation against what the prompt actually has the
  solver do, not the practitioner profile or the sector. The distributor profile straddles buy-side
  and sell-side; O*NET splits it.
- **Skills / Tasks prompt relevance** judges EACH task pick against the prompt's own words. One
  poor pick fails the whole section, and the platform re-validates the whole form on every
  resubmission, so a pick that "cleared" three rounds can fail when the reading tightens; an
  in-app finding on a form field is never debt. M2 reads every pick in metadata.json against
  prompt.md and errors when the duty behind the pick has no signal there; picks carried over from
  a sibling task are the classic failure.

## Routing by prompt type

- Supplier cost events, replenishment, rebates, dead stock, allocation: **13-1022.00 Wholesale
  and Retail Buyers** (the most crowded occupation sector-wide, see [[task-uniqueness-check]]).
- Customer bids, quotes, sell-price proposals: **41-4012.00 Sales Representatives, Wholesale and
  Manufacturing** (M1; a bid the company RECEIVES, such as a salvage buyer's bid, is not a
  customer bid). No Mathematics in its Skills dropdown.
- A sell-price AUDIT, billing correction or margin review: **11-2022.00 Sales Managers** (price
  schedules and discount rates, operational records for profitability, customer sales
  complaints only when customers actually complain). 13-1022 and 41-4012 both fail relevance on
  it ("analytical and file-maintenance work"); 13-2011 Accountants and 43-3031 clerks fail the
  platform's own Occupation-Sector table, which is narrower than onetonline.org's industry
  filter.
- Warehouse loss, salvage, storage and logistics at manager level, equipment and fleet plans:
  **11-3071.00 Transportation, Storage, and Distribution Managers** (M3 counts frame vocabulary
  against merchandise vocabulary under 13-1022 and flags a deliverable file name borrowed from
  another domain; when the check names DUTIES rather than emphasis, no wording pass saves it and
  the occupation moves). No Mathematics; its ERROR-level non-picks for an analyst prompt are
  safety programs, staffing, budgets, import/export compliance, carrier or insurer rate
  negotiation, drones, energy reduction.
- Vendor bankruptcy exposure, claims against suppliers, supply agreements and policy conformance:
  **11-3061.00 Purchasing Managers** (Mathematics IS essential there; Judgment and Decision
  Making is only transferable). "Prepare bid awards requiring board approval" needs a board in
  the prompt; "Develop and implement purchasing ... policies" needs a policy being written,
  revised or rolled out, not applied.
- Customer credit workups: **43-4041.00 Credit Authorizers, Checkers, and Clerks** (no
  Mathematics; Reading Comprehension, Critical Thinking, Writing; picks: evaluate credit
  records against standards, obtain information from banks and bureaus, compile and analyze
  credit information, prepare reports of findings).
- Slotting, storage, stockroom work: **53-7065.00 Stockers and Order Fillers** (Skills dropdown
  offers only Active Listening and Reading Comprehension, both go in; the fourth pick for a crew
  work list is "Provide assistance or direction to other stockroom ... workers"). **43-5071.00
  Shipping, Receiving, and Inventory Clerks is shipping-only** on the platform dropdown (eleven
  duties, nothing on stock location).
- Commission audits under 11-2022: picks about reviewing sales and accounting records, analyzing
  invoices and margins, preparing or validating commission reports; two picks are enough (48
  passed on two). The complaints pick needs a customer complaining, the direct-sales pick needs
  selling, the staffing/performance pick was "clearly unrelated" to a commission audit.
- **Never 53-1047.00** First-Line Supervisors of Transportation and Material Moving Workers:
  disabled on the O*NET industry page, empty task and skill dropdowns on the platform (task 45
  moved to 11-3071 at the form).

## Rules that hold across occupations

- Pick the occupation from the prompt's central deliverable and lead the prompt with that work
  (the merchandise question first, the other domain's documents as the rules material is valued
  on), because the sector is assigned and framing is the only lever when the occupation is right.
- A pick is held to its WHOLE sentence, qualifiers included, and to its OBJECT: a pick that fits
  the occupation still fails when the prompt lacks the object ("customer complaints" on a
  representative's own dispute, "board approval" with no board).
- Write the metadata sentence that ties each of 3-5 picks to the prompt clause carrying it; the
  same block must never be pasted across tasks.
- Before building on an occupation the portfolio has not used, check the O*NET industry page for
  a disabled entry, confirm the dropdowns are populated, and verify each pick against the
  dropdown, never against a quoted list (a Fable build quoted 53-7065's list as 43-5071's).
- When a rejection text does not match the occupation just entered, check the form entry before
  moving again (a mid-chain 11-2022 "FAIL" was an entry error). Check which UID the form was on
  before acting on relayed text (a 48 finding was relayed as 38's).
- M2 is per-prompt, not per-occupation: "Collaborate with vendors to obtain or develop desired
  products" is right on a sourcing prompt and wrong on an allocation plan.
- 2026-09-17 (detention-claim-audit, draft 53, eighth mode): under 43-5071 a detention CLAIM AUDIT
  fails the Skills prompt relevance check on "Contact carrier representatives to make arrangements or
  to issue instructions for shipping and delivery"; auditing what a carrier billed is not arranging
  its delivery, and a prompt that sets the dock appointments is no signal either. The three audit
  picks (compute demurrage type charges; record shipment charges and discrepancies for accounting;
  confer or correspond to rectify problems) were retained. Coded as four 43-5071 M2 rows. Checker's
  steer for an audit prompt: auditing records, calculating charges, reconciling discrepancies,
  preparing accounting or operational reports.
