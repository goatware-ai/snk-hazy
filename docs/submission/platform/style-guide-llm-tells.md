# Style Guide

> **Carried over from the desk this repo was built from and not yet confirmed here.** This
> document describes the LLM tells that get a file sent back. It is kept because the guidance
> is domain-agnostic, but nothing in it has been checked against Hazy's own platform. Where it
> disagrees with `create-the-task-guidelines.md` or `platform-submission-form.md`, those win.

Style Guide for Expert Contributors

Section 1: Recognizing LLM-Generated Files

## Purpose and Scope

This tab of the Style Guide is a practical reference for recognizing LLM-generated files. It names the specific signals that reviewers flag when evaluating task submissions, explains which models produce them, and gives the fix directly.

The "LLM Examples" tab includes screenshots of LLM generated files submitted on the task and explanations of why they are unacceptable. The "Reviewer Rubric" tab provides guidance to reviewers on when to reject, when to send back for revisions, and when to accept files.

## Input Files: Real, or Indistinguishable From Real

> Input files must read exactly like real professional documents. They are the source material that drives task difficulty. An LLM may assist in producing an input file, but the result must be indistinguishable from a document you would actually use at your job. It must contain none of the tells in this guide and none of the synthetic-data pitfalls: round numbers, generic entity names, placeholder text, mismatched field labels, or hard-coded values where formulas belong. Preferred sources remain real documents from your professional practice cleaned of PII, public-domain materials, and files you have personally authored. Where an LLM assist is used, edit until the file mirrors the real-world document exactly. If any tell remains, the file does not qualify.

Edited LLM drafts grounded in real structure may be acceptable in limited cases, but the default is real over synthetic, and LLM drafts must be edited until they exactly mirror the actual real-world document you would use at your job to complete the task.

## Output Files (Golden Solutions): LLM as Starting Point Only

Output files may begin with a model-generated draft. That is permitted. What is not permitted is submitting that draft with minimal editing and treating it as a finished golden solution.

> **The Client Test**
>
> Ask yourself: would you hand this deliverable to a client or present it to your manager without embarrassment? If the answer is no, it is not ready. That is the bar. Not "good for a first draft." Not "better than what the model produced." Actually presentation-ready.

The practical test: if you can produce the same output by pasting your prompt into a model and accepting the first response, it is not meeting the standard. Meaningful editing means domain-specific voice, terminology from your occupation, formatting choices appropriate to your sector, and verified data that you checked against the input files yourself.

## 2. How to Use This Guide

The tells reference table is organized into six categories corresponding to the most common failure modes reviewers encounter. Within each category, individual tells carry four attributes:

- **How It Appears:** the specific way the tell manifests in a real file, with examples
- **Model(s):** which of ChatGPT, Gemini, and Claude most commonly produce this tell
- **Applies To:** whether the tell is relevant for input files, output files, or both
- **[Severity]:** HIGH, MEDIUM, or LOW, reflecting how quickly reviewers flag it and how likely it is to cause a return or rejection

### Severity Key

| Severity | What It Means for Your Submission |
| --- | --- |
| HIGH | Immediate rejection signal. Reviewers flag this on first pass. Submissions with HIGH-severity tells will be returned without full review. |
| MEDIUM | Strong indicator of unedited LLM output. One or two isolated instances may be tolerated; a pattern of MEDIUM tells across a file constitutes a HIGH-severity rejection pattern. |
| LOW | Worth correcting, but unlikely to cause rejection on its own. Usually appears alongside MEDIUM or HIGH tells, which it reinforces. |

A single HIGH-severity tell in an output file is likely to result in a return. Two or more MEDIUM-severity tells in the same file constitute a HIGH-severity pattern. When in doubt, fix it. The effort required to address a tell is almost always less than the effort of a revision cycle.

## 3. LLM Output Tells: Full Reference

The table below covers tells across all file types. File-type-specific categories follow the general language and structural tells. Each category opens with a brief note on why that category of tell is particularly persistent or visible to reviewers.

### Visual and Color Tells

Color and layout choices are the most immediately visible LLM signals. They appear before a reviewer reads a single word of content.

| Tell | How It Appears | Model(s) | Applies To | Fix |
| --- | --- | --- | --- | --- |
| AI-blue color scheme [HIGH] | Excel header fills or Word/PDF table fills in hex #1C3557 or the surrounding navy-blue family (#1A3A5C, #1F3864, #2E4057, #1e2d56). Gradient fills in the same blue family. Blue-on-white slide masters with no other palette variation. | Claude, ChatGPT, Gemini | Input files, Output files | Replace header fills with neutral grays, industry-appropriate colors, or colors from your actual organization's palette. The hex range #1C3557 to #2E4A6B is a known, named rejection signal. Reviewers are trained to spot it. |
| Default Office theme, no customization [MEDIUM] | Entire document uses the out-of-box "Office Theme" palette with no modification: default blues, oranges, and grays in their default proportions. No logo, no custom color, no sector-appropriate aesthetic. | ChatGPT, Gemini | Input files, Output files | Apply a color palette, font set, or visual identity appropriate to your sector and document type. A law firm and a logistics company do not share the same document aesthetic. |
| Perfectly uniform visual hierarchy [LOW] | Every heading level is exactly the same size differential apart. Every table has identical column widths. Spacing is mathematically consistent throughout in a way no human-produced document sustains. | Claude, ChatGPT, Gemini | Input files, Output files | Real professional documents have minor inconsistencies: a slightly wider column, a condensed section, a bolded exception. Introduce natural variation that reflects how a practitioner would actually build the file. |
| Gradient fills on every element [LOW] | Slide backgrounds use soft gradients. Chart fill areas use gradient fills. Table headers have gradient shading. Every element has a subtle design treatment applied uniformly. | Gemini | Output files | Most professional workplace decks use flat color fills. Unless your sector specifically favors gradient-heavy design (design agencies, marketing firms), replace with flat fills that match your industry's visual conventions. |

### Prose and Language Tells

LLM prose has consistent stylistic fingerprints. These patterns are most visible when you read the document aloud (e.g., register shifts, hedging, and transitional filler become obvious in spoken form).

| Tell | How It Appears | Model(s) | Applies To | Fix |
| --- | --- | --- | --- | --- |
| Em dash overuse [HIGH] | Em dashes used as clause connectors throughout the document: "The analysis confirmed — as expected — that..." or "Three vendors were evaluated — all of which met the threshold." Appears every two to three sentences. | Claude, ChatGPT | Input files, Output files | Rewrite sentences using standard punctuation: commas, periods, semicolons, or parentheses. One or two em dashes in a multi-page document is normal. One per paragraph is a rejection signal. |
| Hedged and qualified language throughout [HIGH] | "It is worth noting that..." / "It is important to consider..." / "This may suggest..." / "One could argue..." Hedging appears even when stating established facts or making definitive recommendations. | Claude, ChatGPT, Gemini | Input files, Output files | Practitioners make decisions and state findings directly. Replace hedged constructions with direct statements: "The data shows..." not "The data may suggest..." Reserve qualifiers for genuinely uncertain claims only. |
| Transitional meta-sentences between sections [MEDIUM] | "Having reviewed the above, we now turn to..." / "With this context established, the following section addresses..." / "As outlined in the previous section..." These appear at the start or end of every major section. | Claude, ChatGPT | Input files, Output files | Delete transitional meta-sentences entirely. Real professional documents use structure — headings, numbered sections, visual dividers — to orient the reader, not prose signposting. |
| Uniform formal register regardless of document type [MEDIUM] | An internal ops update reads like a board memo. A field log reads like an executive summary. An email reads like a legal brief. Every document type gets the same formal, measured prose register regardless of audience. | Claude, ChatGPT, Gemini | Input files, Output files | Match tone and register to the document type and audience. Internal ops notes are terse. Client-facing reports are polished but direct. Field documentation is functional and abbreviated. The register should vary with purpose. |
| Corporate buzzword density [MEDIUM] | "Leverage synergies," "leverage existing infrastructure," "optimize stakeholder alignment," "facilitate best practices." The word "leverage" — and similar: "optimize," "facilitate," "robust," "holistic" — appears in nearly every paragraph. | ChatGPT, Gemini | Input files, Output files | Replace with specific, concrete language. "Use the existing CRM data" instead of "leverage existing infrastructure." The more specific the language, the more practitioner-authored it reads. |
| Lists for content that should be prose [MEDIUM] | Information that would naturally flow as a sentence is broken into 3-5 bullet points. A recommendation becomes a bulleted summary. Every analysis section ends in bullets regardless of whether the content is actually enumerable. | ChatGPT | Input files, Output files | Write prose where prose is appropriate. Bullets are for genuinely enumerable items: process steps, vendor names, criteria lists. Analysis, interpretation, and recommendation belong in paragraph form. |
| Passive voice to avoid taking a position [MEDIUM] | "Opportunities have been identified..." / "Challenges were noted across the portfolio..." / "Several risks were observed..." The agent performing the action is absent throughout. No one in the document actually does anything. | Claude, ChatGPT, Gemini | Input files, Output files | Write in active voice and assign responsibility directly: "The procurement team identified three risks..." or "Vendor B exceeded cost thresholds in Q3." Active voice signals practitioner authorship. |
| Stacked adjective quality filler [MEDIUM] | Two adjectives, a filler word, then a list of failures avoided: "clear, well-structured analysis, not vague or incomplete"; "a robust, comprehensive review, not shallow or rushed." The praise-pair-plus-negation shape recurs across prose, and applies equally to prompts and rubric criteria. | Claude, ChatGPT, Gemini | Input files, Output files (and prompts and criteria) | Name the specific thing to check and its correct value instead of describing quality with paired adjectives. Write "States the three questioned costs and the $11,042 total" rather than "provides a clear, thorough cost analysis, not vague or incomplete." The more specific and checkable the statement, the more practitioner-authored it reads. |

### Structural and Header Tells

LLMs default to recognizable document templates. The structure is often technically correct for the document type but lacks the domain-specific judgment that determines how a practitioner in that field would actually organize information.

| Tell | How It Appears | Model(s) | Applies To | Fix |
| --- | --- | --- | --- | --- |
| Generic section headers [HIGH] | "Executive Summary" / "Key Findings" / "Recommendations" / "Next Steps" / "Overview" / "Background" / "Introduction" / "Conclusion" — appearing in this exact sequence with no domain-specific modification. | Claude, ChatGPT, Gemini | Input files, Output files | Reframe headings to reflect actual content and professional context. "Q3 Supplier Risk Summary" not "Executive Summary." "Site Remediation Priorities" not "Recommendations." Headers should be specific enough that a subject matter expert can find content by scanning them. |
| Pre-counted considerations or factors [MEDIUM] | "There are three key considerations: 1)... 2)... 3)..." Every analysis section opens with a count of considerations, factors, challenges, or opportunities, then proceeds to enumerate exactly that count. | ChatGPT, Gemini | Input files, Output files | Real practitioner analysis does not pre-count its findings. The number of considerations is a product of the analysis, not a structural frame for it. Present findings in order of importance, not as a predetermined enumeration. |
| Balanced two-column analysis framing [MEDIUM] | Every comparison defaults to a Strengths/Weaknesses, Pros/Cons, or Advantages/Disadvantages structure. Every vendor, option, or scenario gets exactly equal treatment with equal space on both sides regardless of what the data supports. | ChatGPT, Gemini | Input files, Output files | Practitioners do not allocate equal analytical space to every dimension. Significant findings get more depth. Minor considerations get a sentence. The structure of the analysis should follow the data, not a template. |
| Document names or describes itself [HIGH] | Internal text such as "Golden Solution," "AI-generated output," "This VP-ready strategy memo," "As requested, this document provides," or subheadings that describe what the document is rather than what it contains. | Claude, ChatGPT, Gemini | Output files | Delete any text that describes the document rather than constituting it. Professional deliverables do not announce themselves. The title and headings communicate purpose through content, not self-description. |
| Five-paragraph essay structure [MEDIUM] | Document or section opens with a general statement, develops three supporting points in the middle, and closes with a summary restating the opening. Structure is more high school essay than practitioner deliverable. | ChatGPT | Input files, Output files | Real professional documents lead with the finding or recommendation, then support it with evidence. They do not restate conclusions at the end. The pyramid principle — conclusion first, evidence second — is the professional standard. |

### Spreadsheet-Specific Tells

Spreadsheet tells are often the most reliable rejection signals because they are quantifiable and binary: either the formulas are live or they are not, either the numbers are plausible or they are round.

| Tell | How It Appears | Model(s) | Applies To | Fix |
| --- | --- | --- | --- | --- |
| All values hard-coded, no formulas [HIGH] | Every cell contains a typed number. Totals that should sum a column are typed manually. Percentages that should divide two cells are static values. The spreadsheet cannot be updated by changing any assumption. | Claude, ChatGPT, Gemini | Input files, Output files | Totals, ratios, and all derived values must use formulas that reference source cells. Only primary data entry cells — raw inputs and assumptions — should contain hard-coded values. If you are building the file, use formulas. |
| Round, suspiciously clean numbers [HIGH] | Revenue figures are exactly $1,000,000. Headcount is exactly 100. Margins are exactly 25.0%. Dates are always the 1st of the month. Every number is a clean integer or one-decimal value with no realistic variance. | Claude, ChatGPT, Gemini | Input files | Real data has irregular values: $1,247,382 in revenue, 73 employees, 23.7% margin. If you are creating illustrative data, introduce realistic irregularity. Round numbers are an immediate synthetic data signal. |
| Generic placeholder entity names [HIGH] | Company A, Company B, Company C. Vendor 1, Vendor 2. John Smith, Jane Doe. Region 1, Region 2. Product A, Product B. Names and identifiers that are clearly placeholders rather than realistic entities from your field. | Claude, ChatGPT, Gemini | Input files | Use realistic but fictitious names grounded in your sector: "Meridian Logistics" not "Company A," "Sarah Okonkwo" not "Jane Doe," "Southwest Region" not "Region 1." Names should feel like they belong to a real business context. |
| Single-tab workbook for multi-faceted data [MEDIUM] | A complex analysis, evaluation, or financial model is presented on a single worksheet with no supporting tabs, no assumptions tab, no data source tab. Everything is compressed onto one sheet with no navigation structure. | Claude, ChatGPT | Input files, Output files | Real professional spreadsheets organize data across logical tabs: a summary tab, data tabs, an assumptions tab, and supporting references. Single-tab workbooks for complex tasks signal low effort and synthetic construction. |
| Mismatched or incorrect field labels [HIGH] | A sales report uses "Current Customer" where "Current Supplier" would be correct. An invoice shows "Service Fee" where "Material Cost" was expected. Field labels do not match the terminology the task context requires. | Claude, ChatGPT, Gemini | Input files | Review every field label against the context of your task and occupation. LLMs generate plausible-sounding labels that may not match the actual terminology of your field. Check that your sector's specific terms — not generic business terms — are used throughout. |
| Filler text in data cells [HIGH] | Cells contain "TBD," "Enter value here," "Placeholder," "Lorem ipsum," or "N/A (to be completed)" in fields that should contain actual data. Present in input files that are supposed to drive task difficulty. | Claude, ChatGPT, Gemini | Input files | Every data cell in an input file must contain realistic content. Filler text means the file does not represent a real professional document and cannot drive meaningful model evaluation. Replace with substantive, plausible data. |

### Document-Specific Tells (Word / PDF)

Document tells are most visible in the mismatch between structural correctness and practitioner authenticity. A document can have the right sections in the right order and still read as synthetically produced.

| Tell | How It Appears | Model(s) | Applies To | Fix |
| --- | --- | --- | --- | --- |
| TOC that does not reflect actual content [MEDIUM] | A table of contents is present and correctly formatted but lists generic section names that do not match the document's actual heading text, or headings that were generated from a template rather than from the content itself. | Claude, ChatGPT | Output files | Every TOC entry must match the actual heading in the document exactly and reflect specific content. TOC section names should be unique to this deliverable, not generic placeholders that could apply to any document in this category. |
| Citations referencing non-existent or vague sources [MEDIUM] | "According to industry reports (Source: Industry Report 2023)..." / "As documented in internal policy (Policy Ref: HR-001)..." Citations are present but reference vague, non-specific, or non-verifiable sources. | ChatGPT, Gemini | Input files, Output files | Either use real, specific citations with author, publication, and date, or write in the direct practitioner voice that does not require citations at all. Invented citations are more damaging than no citations. |
| AI-referencing confidential or watermark labels [HIGH] | "CONFIDENTIAL — AI Generated" / "DRAFT — Do Not Distribute (Auto-Generated)" / Watermarks referencing AI generation, draft status, or model output in language no human preparer would ever include. | Claude | Output files | If a confidential label is appropriate to the document type, use a realistic professional label: "CONFIDENTIAL," "PRIVILEGED AND CONFIDENTIAL," or "INTERNAL USE ONLY." Remove any language referencing AI generation, auto-draft status, or model output. |
| Inconsistent voice or register mid-document [MEDIUM] | A document shifts register mid-section: two paragraphs of polished prose followed by a paragraph that reads casual, then back to formal. The voice is inconsistent because different sections were generated with different prompts. | Claude, ChatGPT, Gemini | Input files, Output files | Read the full document aloud before submitting. Voice inconsistencies become obvious when you hear the shift. Edit all sections to maintain a consistent register appropriate to the document type and audience throughout. |

### Presentation-Specific Tells (PowerPoint)

Presentation tells tend to be structural and visual simultaneously. The most immediate signal is the absence of any visual identity: a blank white slide with default fonts is the baseline LLM output for presentations.

| Tell | How It Appears | Model(s) | Applies To | Fix |
| --- | --- | --- | --- | --- |
| Plain white slides with no master or background [HIGH] | Slides have no background color, no slide master, no company branding, and no visual identity. Title text sits directly on a white background with default fonts. Looks like a blank presentation that was never formatted. | Claude, ChatGPT | Input files, Output files | Apply a slide master with a background color, header bar, or footer treatment appropriate to your sector. Every professional presentation has at least a minimal visual identity. White-on-white with default fonts is not presentation-ready. |
| Title slide describes the deliverable type [HIGH] | "AI-Generated Presentation: Quarterly Review" / "Output File: Strategic Analysis" / "Golden Solution: Market Entry Recommendations." The title slide names the file category rather than giving the presentation a real, specific name. | Claude, ChatGPT, Gemini | Output files | Give the presentation a real professional title: "Q3 Operations Review: Midwest Region" or "Vendor Selection Recommendation: ERP Platform." The title should name the specific content and context, not the file type or generation status. |
| Data as text bullets instead of charts [HIGH] | A slide that should show a trend uses a bulleted list of data points instead of a chart. Comparative data appears as a list of percentages rather than a bar chart. Numerical results are narrated in text rather than visualized. | Claude, ChatGPT | Input files, Output files | Any data with a trend, comparison, distribution, or relationship should be visualized: bar chart, line chart, scatter plot, or table. Practitioners use charts because they communicate faster. Text-only data slides are a strong LLM signal. |
| Speaker notes in LLM voice [MEDIUM] | Speaker notes say "As an AI, I would present this by..." or "This slide covers..." or "The presenter should note that..." Notes describe what the slide does rather than providing actual talking points a real presenter would use. | Claude, ChatGPT, Gemini | Output files | Speaker notes should be actual talking points: the specific insight to highlight, the anticipated question to address, or the context that does not fit on the slide itself. Delete any notes that describe the slide rather than extending it. |
| Rigid three-part agenda/content/summary structure [MEDIUM] | Slide 1: Title. Slide 2: Agenda listing three sections. Slides 3 to X: Content sections in that order. Final slide: Summary repeating the opening. The structure is a tutorial template with no variation for audience or purpose. | ChatGPT, Gemini | Output files | Professional decks vary structure based on purpose and audience. A board update starts with the recommendation. An operational briefing starts with current status. Not every deck needs an agenda slide. Structure should serve communication, not template compliance. |

### File Naming and Metadata Tells

File names are checked before the file is opened. Naming errors that reveal AI origin or production method are an immediate red flag, and double-extension errors cause packaging failures that result in automatic returns.

| Tell | How It Appears | Model(s) | Applies To | Fix |
| --- | --- | --- | --- | --- |
| File named "golden solution" or similar [HIGH] | Output file named golden_solution.xlsx, golden_solution_final.docx, ai_output.pptx, model_response.pdf, or any variant that names the file category or AI output status rather than the deliverable content. | Claude, ChatGPT, Gemini | Output files | Name files the way a practitioner would name a real deliverable: Q3_Budget_Review.xlsx, Vendor_Evaluation_Report.docx, Site_Assessment_Presentation.pptx. The file name should communicate content and context to someone finding it in a shared drive months later. |
| AI tooling referenced in subheadings or body [HIGH] | Subheadings contain "AI-Assisted Analysis," "Generated Section," or "AI Summary." Document body includes "Based on the information provided," "As an AI language model," or "Using the input data supplied." | Claude, ChatGPT, Gemini | Input files, Output files | Remove every reference to AI tooling, model assistance, or synthetic generation from document body, headings, metadata, and file names. Professional deliverables do not narrate their production method. |
| Double extensions or synthetic naming patterns [HIGH] | report.xlsx.xlsx, analysis.docx.docx, output_final_v2_FINAL.xlsx, document_1_revised_final_APPROVED.docx. Either double extensions or naming patterns that reveal iterative AI regeneration rather than human file management. | Claude, ChatGPT, Gemini | Input files, Output files | Use a single, clean extension. Use a version convention appropriate to your organization: v1, v2, or a date suffix such as 2026-05. The double-extension version is a packaging failure that causes immediate rejection regardless of content quality. |

## Pre-Submission Self-Checks

Before submitting any task, run this checklist against your files. If you cannot check every item, do not submit yet.

### Input Files

- [ ] Does every file look like something you would actually find in a real workplace for this occupation?
- [ ] Are all numbers, names, and identifiers specific and realistic, not round or generic?
- [ ] Are field labels correct for your sector's terminology, not generic business labels?
- [ ] Is all data substantive, with no "TBD," "Placeholder," or "Enter value here" anywhere?
- [ ] Are entity names (companies, people, products) realistic rather than "Company A" or "John Smith"?
- [ ] Does the file have enough content and complexity to require expert-level interpretation?

### Output Files (Golden Solutions)

- [ ] Have you changed every header fill that defaulted to the AI-blue hex range (#1C3557 and family)?
- [ ] Have you replaced all generic section headers with headings specific to your deliverable content?
- [ ] Have you read the full document and removed or rewritten hedged, transitional, or self-describing language?
- [ ] For spreadsheets: do totals and derived values use formulas, not hard-coded numbers?
- [ ] For spreadsheets: have you personally verified at least 2 to 3 calculated values against the source data?
- [ ] For presentations: is there a slide master or background? Are data comparisons shown as charts, not text bullets?
- [ ] For documents: is the register consistent throughout? Have you removed transitional meta-sentences?
- [ ] Does the file name describe the deliverable, not the file type or AI output status?
- [ ] Have you removed every reference to AI tooling, model assistance, or platform-specific language?
- [ ] Would you hand this file to a client or present it to your manager without embarrassment?

**Final Check**

If your output can be produced by pasting your prompt into a model and accepting the first response without meaningful editing, it is not meeting the standard. The goal is practitioner-quality work that happens to have started with a model draft, not a model draft that received surface-level edits.
