# Clause map

| # | Prompt clause | Golden location | Rubric rows |
|---|---|---|---|
| 1 | "Build the audit as one workbook named northline_audit_sept2026.xlsx" | "Northline freight bill audit, September 2026 pickups, Halvorsen Building Products" | 1 |
| 2 | "The first tab is the summary Ingrid reads" | "Prepared for Ingrid Solheim, controller" (Summary, first worksheet) | 1,22 |
| 3 | "what Northline billed for the month" | "Total billed by Northline" | 3 |
| 4 | "what the contract says we owe" | "Total due under the contract" | 4 |
| 5 | "the difference" | "Net difference, billed less due" | 3,4 |
| 6 | "how many bills carry an exception and of what kinds" | "Freight bills with an exception", "Exceptions by contract term" | 17,18 |
| 7 | "and what we are claiming" | "Overcharges claimed" | 2 |
| 8 | "every freight bill rated under the contract line by line beside what Northline billed" | "CONTRACT_TOTAL", "BILLED_TOTAL" | 23,7,8,10,12 |
| 9 | "the exceptions called out with the contract term each one rests on" | "EXCEPTION", "7.1 duplicate bill" | 18,6,15 |
| 10 | "a claim schedule in the form the agreement asks for" | "Overcharge claim schedule under section 7.2" | 19,2 |
| 11 | "Anything where Northline billed us less than the contract goes on its own list, reported and not netted" | "reported under section 7.3 and not netted against the claim" | 5,16 |
| 12 | "Put a note to Ingrid on the last tab with what she should know before she files" | "Note to Ingrid Solheim on the September Northline audit" (last worksheet) | 20,22 |
| 13 | "including anything in the file that the documents do not settle" | "Three things the file does not settle" | 20,21 |
| 14 | "I need the workbook by Friday, October 16" | "report prepared October 16, 2026" | 1 |
| 15 | "a listing of what sits in their billing file behind the September bills" | "Billing File" (tab), "SETTLED_BY", "Billed items accepted on a document or a written confirmation" | 9,11,12,21 |
| 16 | "the shipping desk's email traffic with Northline for the month" | "Confirmations" (tab), "CONFIRMED_ACCESSORIALS" | 13,14 |

Rebuilt: 2026-09-22 (difficulty revision; every prompt ask re-read against the rebuilt golden and the rubric)
