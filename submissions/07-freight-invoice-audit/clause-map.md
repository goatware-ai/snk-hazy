# Clause map

| # | Prompt clause | Golden location | Rubric rows |
|---|---|---|---|
| 1 | "Build the audit as one workbook named northline_audit_sept2026.xlsx" | "Northline freight bill audit, the September 2026 file, Halvorsen Building Products" | 1 |
| 2 | "The first tab is the summary Ingrid reads" | "Prepared for Ingrid Solheim, controller" (Summary, first worksheet) | 1 |
| 3 | "what Northline billed for the month" | "Total billed by Northline" | 3 |
| 4 | "what the contract says we owe" | "Total due under the contract" | 4 |
| 5 | "the difference" | "Net difference, billed less due" | 3,4 |
| 6 | "how many bills carry an exception and of what kinds" | "Freight bills with an exception", "Exceptions by contract term" | 22 |
| 7 | "and what we are claiming" | "Overcharges claimed" | 2 |
| 8 | "every freight bill rated under the contract line by line beside what Northline billed" | "CONTRACT_TOTAL", "BILLED_TOTAL" | 26,7,8,9,11 |
| 9 | "the exceptions called out with the contract term each one rests on" | "EXCEPTION", "7.1 duplicate bill" | 22,7,9,16 |
| 10 | "a claim schedule in the form the agreement asks for" | "Overcharge claim schedule under section 7.2" | 23,2 |
| 11 | "Anything where Northline billed us less than the contract goes on its own list, reported and not netted" | "reported under section 7.3 and not netted against the claim" | 20,21 |
| 12 | "Put a note to Ingrid on the last tab with what she should know before she files" | "Note to Ingrid Solheim on the September Northline audit" (last worksheet) | 24,25 |
| 13 | "including anything in the file that the documents do not settle" | "Three things the file does not settle" | 24 |
| 14 | "I need the workbook by Friday, October 16" | "report prepared October 16, 2026" | 1 |
| 15 | "a listing of what sits in their billing file behind the September bills" | "Billing File" (tab), "Corrections" (tab), "SETTLED_BY", "Billed items accepted on a document or a written confirmation" | 5,6,10,12,25 |
| 16 | "the shipping desk's email traffic with Northline for the month" | "Confirmations" (tab), "CONFIRMED_ACCESSORIALS" | 13,14,15,16,17 |

Rebuilt: 2026-09-30 (reviewer's six hardening items; every prompt ask re-read against the rebuilt golden and the rubric)
