# Domains and occupations

> Captured 2026-09-21 from section 1 of the live submission form. Both lists are
> single-select radio lists, not free text. The guidelines are explicit that **a domain or
> sector not visible in the form is not available**, so this is a closed list: a task must
> fit one of the entries below or it cannot be submitted.

The form header points at <https://www.onetonline.org/find/industry> for picking the
closest occupation. <https://www.onetonline.org/find/all> is the fuller list for
the occupation and its code. Titles below are reproduced as the form spells them, which is
sometimes shorter than the official O*NET title.

## Domain (14)

Selected first, "based on your area of expertise".

1. Architecture and Engineering
2. Building and Grounds Cleaning and Maintenance
3. Community and Social Service
4. Educational Instruction and Library
5. Food Preparation and Serving
6. Healthcare Practitioners / Support
7. Healthcare Practitioners and Technical
8. Healthcare Support
9. Installation, Maintenance, and Repair
10. Legal
11. Life, Physical, and Social Science
12. Management
13. Production
14. Transportation and Material Moving

Two pairs overlap and the form does not say how they differ: *Healthcare Practitioners /
Support* against both *Healthcare Practitioners and Technical* and *Healthcare Support*.
Pick the most specific one that fits and record the choice in the task's metadata.

Note what is **absent**: no Business and Financial Operations, no Computer and
Mathematical, no Sales, no Office and Administrative Support, no Construction and
Extraction, no Arts/Design/Media, no Personal Care and Service, no Protective Service,
no Farming/Fishing/Forestry. Several occupations in the list below sit in those families at
O*NET, so the domain and the occupation's own O*NET job family do not always agree. The
form's domain choice is what governs.

## Occupation (64)

Selected second, "based on your area of expertise". Alphabetical in the form.

| # | Occupation as the form lists it |
|---|---|
| 1 | Arbitrators, Mediators, and Conciliators |
| 2 | Architectural and Engineering Managers |
| 3 | Atmospheric and Space Scientists |
| 4 | Biochemists and Biophysicists |
| 5 | Biofuels/Biodiesel Technology and Product Development Managers |
| 6 | Bioinformatics Scientists |
| 7 | Biological Technicians |
| 8 | Biologists |
| 9 | Chemists |
| 10 | Civil Engineering Technologists and Technicians |
| 11 | Compliance Managers |
| 12 | Computer Hardware Engineers |
| 13 | Dental Hygienists |
| 14 | Economists |
| 15 | Electrical Engineers |
| 16 | Emergency Medical Technicians |
| 17 | Environmental Engineers |
| 18 | Environmental Scientists and Specialists |
| 19 | First Line Supervisors of Food Prep and Serving Workers |
| 20 | First Line Supervisors of Housekeeping and Janitorial Workers |
| 21 | First Line Supervisors of Material Moving Operators |
| 22 | First Line Supervisors of Mechanics, Installers, and Repairers |
| 23 | Food Scientists and Technologists |
| 24 | General Internal Medicine Physicians |
| 25 | Geoscientists |
| 26 | Home Health Aides |
| 27 | Human Resources Managers |
| 28 | Inspectors, Testers, Sorters, Samplers, and Weighers |
| 29 | Instructional Coordinators |
| 30 | Judges, Magistrate Judges, and Magistrates |
| 31 | Judicial Law Clerks |
| 32 | Librarians and Media Collections Specialists |
| 33 | Machinists |
| 34 | Manufacturing Engineers |
| 35 | Marketing Managers |
| 36 | Medical Assistants |
| 37 | Medical Transcriptionists |
| 38 | Mental Health Counselors |
| 39 | Mental Health and Substance Abuse Social Workers |
| 40 | Molecular and Cellular Biologists |
| 41 | Natural Sciences Managers |
| 42 | Nursing Assistants |
| 43 | Obstetricians and Gynecologists |
| 44 | Occupational Therapy Assistants |
| 45 | Packaging and Filling Machine Operators and Tenders |
| 46 | Paralegals and Legal Assistants |
| 47 | Paramedics |
| 48 | Pediatricians, General |
| 49 | Personal Care Aides |
| 50 | Pharmacy Aides |
| 51 | Phlebotomists |
| 52 | Psychiatric Aides |
| 53 | Purchasing Managers |
| 54 | Quality Control Systems Managers |
| 55 | Respiratory Therapists |
| 56 | Social and Human Service Assistants |
| 57 | Soil and Plant Scientists |
| 58 | Substance Abuse and Behavioral Disorder Counselors |
| 59 | Surveyors |
| 60 | Title Examiners, Abstractors, and Searchers |
| 61 | Transportation, Storage, and Distribution Managers |
| 62 | Treasurers and Controllers |
| 63 | Veterinary Assistants and Laboratory Animal Caretakers |
| 64 | Zoologists and Wildlife Biologists |

The capture spans a page break between *Dental Hygienists* and *Economists*. The sequence
is alphabetical and continuous there, but a short title falling between the two could have
been cut. Check the live form before concluding an occupation is unavailable.

## O*NET codes

Codes are verified separately and recorded in
[onet-codes.md](onet-codes.md). Always confirm the code on the occupation's own
onetonline.org page before pasting it into the form: the form's titles are abbreviated, and
several of these occupations are O*NET detail codes ending in `.01` or `.02` rather than
`.00`.

## What this means for task design

This desk can no longer assume one sector. Three consequences:

1. **Pick the occupation before writing the prompt.** The occupation constrains what
   counts as authentic day-to-day work, and the platform checks that the prompt matches it.
2. **Most of these occupations are hands-on rather than desk-bound.** Phlebotomists,
   Machinists and Home Health Aides do not spend their day producing .xlsx deliverables.
   The task still has to land on a concrete document deliverable, so favour the supervisory,
   managerial, analytical and licensed-professional entries where a written work product is
   genuinely part of the job: the four First Line Supervisor rows, the manager rows, the
   scientist rows, and the legal rows.
3. **Safety and privacy exposure is much higher than in a trade sector.** Clinical,
   counselling and laboratory occupations put real patient-safety and PHI questions in
   scope. A task must never teach unsafe practice, and no input file may carry anything
   that reads as real patient data.
