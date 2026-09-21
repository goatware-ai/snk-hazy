# O*NET codes for the platform's 64 occupations

> Verified 2026-09-21 against the live onetonline.org occupation list (1,016 O*NET-SOC
> codes), with the less common codes spot-checked on their own summary pages. Job Family is
> O*NET's own, assigned by SOC major group. Titles in the first column are as the Hazy form
> spells them; the third column gives the official O*NET title where the form abbreviates.

## Why the domain list is what it is

The 64 occupations fall into exactly **13** O*NET job families, and the form's **14**
domains are those 13 plus `Healthcare Practitioners / Support`, which is not an O*NET
family at all. So the domain radio is, in practice, the occupation's own job family.

| Job Family (= the form's Domain) | Occupations |
|---|---|
| Life, Physical, and Social Science | 15 |
| Healthcare Support | 12 |
| Management | 11 |
| Healthcare Practitioners and Technical | 7 |
| Architecture and Engineering | 6 |
| Legal | 5 |
| Community and Social Service | 4 |
| Production | 3 |
| Educational Instruction and Library | 2 |
| Food Preparation and Serving Related | 1 |
| Building and Grounds Cleaning and Maintenance | 1 |
| Transportation and Material Moving | 1 |
| Installation, Maintenance, and Repair | 1 |

**Pick the domain that matches the occupation's job family**, and treat
`Healthcare Practitioners / Support` as a duplicate to avoid unless nothing else fits.

## Four traps

1. **The four First-Line Supervisor rows do not belong to Management.** They sit in Food
   Preparation and Serving, Building and Grounds, Transportation and Material Moving, and
   Installation/Maintenance/Repair respectively. Inspectors and Machinists are Production,
   not Management.
2. **"First Line Supervisors of Material Moving Operators" is badly abbreviated.** The
   official title is *First-Line Supervisors of Material-Moving Machine and Vehicle
   Operators*, code `53-1043.00`. All four supervisor titles are officially hyphenated
   "First-Line".
3. **Eight entries are O*NET detail codes**, ending `.01` to `.04` rather than `.00`. They
   are valid O*NET-SOC but will fail validation against a plain BLS SOC list: 11-9041.01,
   19-1029.01, 19-1029.04, 11-9199.02, 17-2112.03, 19-1029.02, 11-3051.01, 11-3031.01.
4. **Emergency Medical Technicians and Paramedics are separate occupations**, split in the
   2018 SOC revision. Do not collapse them into one code.

## The table

| # | Occupation (as the form lists it) | Code | Official O*NET title, if different | Job Family |
|---|---|---|---|---|
| 1 | Arbitrators, Mediators, and Conciliators | 23-1022.00 | | Legal |
| 2 | Architectural and Engineering Managers | 11-9041.00 | | Management |
| 3 | Atmospheric and Space Scientists | 19-2021.00 | | Life, Physical, and Social Science |
| 4 | Biochemists and Biophysicists | 19-1021.00 | | Life, Physical, and Social Science |
| 5 | Biofuels/Biodiesel Technology and Product Development Managers | 11-9041.01 | | Management |
| 6 | Bioinformatics Scientists | 19-1029.01 | | Life, Physical, and Social Science |
| 7 | Biological Technicians | 19-4021.00 | | Life, Physical, and Social Science |
| 8 | Biologists | 19-1029.04 | | Life, Physical, and Social Science |
| 9 | Chemists | 19-2031.00 | | Life, Physical, and Social Science |
| 10 | Civil Engineering Technologists and Technicians | 17-3022.00 | | Architecture and Engineering |
| 11 | Compliance Managers | 11-9199.02 | | Management |
| 12 | Computer Hardware Engineers | 17-2061.00 | | Architecture and Engineering |
| 13 | Dental Hygienists | 29-1292.00 | | Healthcare Practitioners and Technical |
| 14 | Economists | 19-3011.00 | | Life, Physical, and Social Science |
| 15 | Electrical Engineers | 17-2071.00 | | Architecture and Engineering |
| 16 | Emergency Medical Technicians | 29-2042.00 | | Healthcare Practitioners and Technical |
| 17 | Environmental Engineers | 17-2081.00 | | Architecture and Engineering |
| 18 | Environmental Scientists and Specialists | 19-2041.00 | Environmental Scientists and Specialists, Including Health | Life, Physical, and Social Science |
| 19 | First Line Supervisors of Food Prep and Serving Workers | 35-1012.00 | First-Line Supervisors of Food Preparation and Serving Workers | Food Preparation and Serving Related |
| 20 | First Line Supervisors of Housekeeping and Janitorial Workers | 37-1011.00 | First-Line Supervisors of Housekeeping and Janitorial Workers | Building and Grounds Cleaning and Maintenance |
| 21 | First Line Supervisors of Material Moving Operators | 53-1043.00 | First-Line Supervisors of Material-Moving Machine and Vehicle Operators | Transportation and Material Moving |
| 22 | First Line Supervisors of Mechanics, Installers, and Repairers | 49-1011.00 | First-Line Supervisors of Mechanics, Installers, and Repairers | Installation, Maintenance, and Repair |
| 23 | Food Scientists and Technologists | 19-1012.00 | | Life, Physical, and Social Science |
| 24 | General Internal Medicine Physicians | 29-1216.00 | | Healthcare Practitioners and Technical |
| 25 | Geoscientists | 19-2042.00 | Geoscientists, Except Hydrologists and Geographers | Life, Physical, and Social Science |
| 26 | Home Health Aides | 31-1121.00 | | Healthcare Support |
| 27 | Human Resources Managers | 11-3121.00 | | Management |
| 28 | Inspectors, Testers, Sorters, Samplers, and Weighers | 51-9061.00 | | Production |
| 29 | Instructional Coordinators | 25-9031.00 | | Educational Instruction and Library |
| 30 | Judges, Magistrate Judges, and Magistrates | 23-1023.00 | | Legal |
| 31 | Judicial Law Clerks | 23-1012.00 | | Legal |
| 32 | Librarians and Media Collections Specialists | 25-4022.00 | | Educational Instruction and Library |
| 33 | Machinists | 51-4041.00 | | Production |
| 34 | Manufacturing Engineers | 17-2112.03 | | Architecture and Engineering |
| 35 | Marketing Managers | 11-2021.00 | | Management |
| 36 | Medical Assistants | 31-9092.00 | | Healthcare Support |
| 37 | Medical Transcriptionists | 31-9094.00 | | Healthcare Support |
| 38 | Mental Health Counselors | 21-1014.00 | | Community and Social Service |
| 39 | Mental Health and Substance Abuse Social Workers | 21-1023.00 | | Community and Social Service |
| 40 | Molecular and Cellular Biologists | 19-1029.02 | | Life, Physical, and Social Science |
| 41 | Natural Sciences Managers | 11-9121.00 | | Management |
| 42 | Nursing Assistants | 31-1131.00 | | Healthcare Support |
| 43 | Obstetricians and Gynecologists | 29-1218.00 | | Healthcare Practitioners and Technical |
| 44 | Occupational Therapy Assistants | 31-2011.00 | | Healthcare Support |
| 45 | Packaging and Filling Machine Operators and Tenders | 51-9111.00 | | Production |
| 46 | Paralegals and Legal Assistants | 23-2011.00 | | Legal |
| 47 | Paramedics | 29-2043.00 | | Healthcare Practitioners and Technical |
| 48 | Pediatricians, General | 29-1221.00 | | Healthcare Practitioners and Technical |
| 49 | Personal Care Aides | 31-1122.00 | | Healthcare Support |
| 50 | Pharmacy Aides | 31-9095.00 | | Healthcare Support |
| 51 | Phlebotomists | 31-9097.00 | | Healthcare Support |
| 52 | Psychiatric Aides | 31-1133.00 | | Healthcare Support |
| 53 | Purchasing Managers | 11-3061.00 | | Management |
| 54 | Quality Control Systems Managers | 11-3051.01 | | Management |
| 55 | Respiratory Therapists | 29-1126.00 | | Healthcare Practitioners and Technical |
| 56 | Social and Human Service Assistants | 21-1093.00 | | Community and Social Service |
| 57 | Soil and Plant Scientists | 19-1013.00 | | Life, Physical, and Social Science |
| 58 | Substance Abuse and Behavioral Disorder Counselors | 21-1011.00 | | Community and Social Service |
| 59 | Surveyors | 17-1022.00 | | Architecture and Engineering |
| 60 | Title Examiners, Abstractors, and Searchers | 23-2093.00 | | Legal |
| 61 | Transportation, Storage, and Distribution Managers | 11-3071.00 | | Management |
| 62 | Treasurers and Controllers | 11-3031.01 | | Management |
| 63 | Veterinary Assistants and Laboratory Animal Caretakers | 31-9096.00 | | Healthcare Support |
| 64 | Zoologists and Wildlife Biologists | 19-1023.00 | | Life, Physical, and Social Science |

## Overlap with the old Geranium desk

Only two of Geranium's six Wholesale Trade codes survive here: **Purchasing Managers**
(11-3061.00) and **Transportation, Storage, and Distribution Managers** (11-3071.00). The
other four — Sales Managers 11-2022.00, Wholesale and Retail Buyers 13-1022.00, Sales
Representatives 41-4012.00, and Shipping/Receiving Clerks 43-5071.00 — are **not on the
Hazy list**. Any Geranium task idea built on them cannot be resubmitted here.
