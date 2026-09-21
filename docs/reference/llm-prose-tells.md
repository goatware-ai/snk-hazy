# LLM prose tells

> Scope: the prose classes the platform's own style-guide table does not list (the three-beat rhythm, tautology, aphorism and the shapes below), with the flagged evidence for each.
> The platform's list is `../submission/platform/style-guide-llm-tells.md`; read that first and this second.

> Every phrase or pattern that has been flagged as "this reads like an LLM", collected so
> the next task is written clean instead of scrubbed after the fact.
> Companion to `memory/prose-standard.md` (the grammar side).
>
> Enforced mechanically by rule **A10** (`tools/gcheck/authorship/prose.py`, run by `tools/autoeval_check.py`), which scans
> `instruction.md`, every input `.docx` and the solution workbook's text cells. A10 is a
> pattern net, not a substitute for reading the prose aloud.

## Why it gets caught

One flagged note named the mechanism precisely, and it is worth keeping verbatim because
it describes a *structure*, not a word list:

> LLM sounding language needs to be eliminated. It follows a pattern of messy workplace
> detail --> artificial shorthand/idioms ---> analytical requirement.

That three-beat rhythm is the tell. A real buyer writing a real memo does not set up
concrete detail, pivot on an aphorism, then land an analytical demand, paragraph after
paragraph. The aphorism is the giveaway: it exists to sound busy and lived-in, and it is
the one part of the sentence carrying no information.

Second, from the same note: **"It is not how most people really speak at work."** Ordinary
workplace writing is flatter and more redundant than fiction about workplace writing. It
repeats nouns instead of finding a fresh idiom for them, and it explains things at more
length than a slogan would.

---

## Pattern classes, with the flagged evidence

### 1. Tautology / "X is X"

The highest-confidence tell. Three of these were flagged in a single package.

| Flagged | Where | Round |
| --- | --- | --- |
| "Committed work is committed" | a prompt AND the input memo beside it | 2026-08-22 |
| "policy 6.3 is still policy" | an input memo | 2026-08-22 |
| "paragraph 8 is the whole story" | an input email | 2026-08-22 |

**Fix:** say the rule and its consequence. "Committed work is committed" becomes "Released
project work is covered before counter stock, and it does not get cut to protect the
counter."

### 2. Aphorism / slogan as a sentence

Short declarative punch lines, usually opening or closing a paragraph.

| Flagged | Where | Round |
| --- | --- | --- |
| "September is use it or lose it" | a golden briefing | 2026-08-22 |
| "Chestnut Ridge is where the money hurts" | a golden briefing | 2026-08-22 |
| "leave them and they are gone and October is short by the same amount" | a golden briefing | 2026-08-22 |
| "nobody promises what is not coming" | a golden briefing | 2026-08-22 |
| "anything that goes short has to show as short" | a prompt | 2026-08-22 |

The recorded summary of the class: *"typical punchy phrases that are stylistic of an LLM
trying too hard to sound real and busy."*

**Fix:** state the mechanism instead of the moral. "September is use it or lose it" becomes
"September ceiling that we do not order against is not available later in the period."

### 3. Idiom and metaphor in place of the fact

| Flagged | Where | Round |
| --- | --- | --- |
| "I would rather walk into that call knowing where we are naked than find out in November" | an input memo | 2026-08-22 |
| "what we leave on the counter where we cannot cover it" | a prompt | 2026-08-22 |
| "not quietly dropped" | a prompt | 2026-08-22 |
| "where he and the notice disagree, Steve is the one we go with" | a prompt | 2026-08-22 |

**Fix:** name the quantity. "What we leave on the counter" becomes "the counter sales we
cannot fill, and the margin on them."

### 4. Compressed first-person filler

Narration of the author's own legwork, in shorthand.

| Flagged | Where | Round |
| --- | --- | --- |
| "I pulled the rest" | a prompt | 2026-08-22 |
| "the rest of it has to follow her without me rebuilding the file" (flagged: "this one doesn't even make sense") | a prompt | 2026-08-22 |

**Fix:** drop the narration, or make it a plain complete sentence. Note the second one was
read as *incoherent*, not merely stylised: compressed shorthand stops parsing
before the writer notices.

### 5. Fragment used as a heading inside prose

| Flagged | Where | Round |
| --- | --- | --- |
| "Front tab: what she needs to run that call" | a prompt | 2026-08-22 |
| "Terms. Subject to prior sale, and I mean that this month, the phone has not stopped since Sandusky put everybody on allocation. Net 15." | an input quotation | 2026-08-22 |

The second was flagged as **not even clear** — a fragment, a comma splice and a second
fragment in one breath. Trade documents do use terse terms lines, but they punctuate them.

**Fix:** complete sentences, or a real labelled line ("Terms: net 15 days.").

### 6. Em-dash density

The reason for the standing zero-em-dash house rule. One input was flagged for em dashes in
its heading and in nearly every short paragraph; a second showed the pattern more strongly,
with nine em dashes across four short messages.

**Fix:** zero em dashes in every artifact. Coded as A6.

House note: `../submission/platform/style-guide-llm-tells.md` lists em-dash overuse as HIGH.
The house rule is stricter and does not depend on the severity band: zero em dashes in every
artifact (prompt, inputs, golden, rubric), coded A6.

### 7. Run-ons, comma splices and missing punctuation

One note opened with this, ahead of the style points:

> Fix run-on sentences, fragments, and missing punctuation throughout all docs.

Two clauses joined by a comma is the commonest instance ("Not one classified breaker goes
into Hamilton or Stroud township, Meixell has been red tagging them since the spring").
See `memory/prose-standard.md`.

### 8. Aphoristic parallelism (the semicolon-balanced maxim)

| Flagged | Where | Round |
| --- | --- | --- |
| "A charge a customer hears about from their salesman is a policy; a charge they meet cold on a statement is an insult, and I have watched an insult cost this house an account that took ten years to win." | an input email set | 2026-08-31 |

The balanced "X is a noun; Y is a noun" maxim is a class-2 slogan doubled: two aphorisms
hinged on a semicolon. The same shape has turned up in another memo ("... is a schedule; a
missed date they discover is a lost ..."), found by the A10 probe.

**Fix:** state the consequence once, plainly. "A charge the salesman explains in advance is
accepted as policy. A charge a customer first discovers on a statement causes lasting
resentment."

### 9. Scene-setting fragments as openers

| Flagged | Where | Round |
| --- | --- | --- |
| "Word travels. Two things before the pencil comes out." | an input email set | 2026-08-31 |

The recorded standard: *"Nobody but an LLM really speaks like that... nobody who has a
truly urgent issue that needs resolving immediately is going to speak in less-than-clear
language."* Real senders open with the subject, not atmosphere.

**Fix:** "I heard the delivery sheet is being reworked. Two things need to be settled
before any changes are made."

### 10. Urgency performed instead of stated, and folksy metonymy

| Flagged | Where | Round |
| --- | --- | --- |
| "The July statement has the outbound delivery line circled in my handwriting, and it is going to stay circled until the sheet we hand customers matches what the trucks cost." | an input memo | 2026-08-31 |
| "The seventy five was old when gas was cheap." | an input email set | 2026-08-31 |
| "if a charge shows up they will drive to Quincy before they pay it, and honestly that is fine with me and probably with the trucks." | an input email set | 2026-08-31 |
| "Just build it so I can stand at a counter and defend it, zone by zone, with the cost on paper." | an input email set | 2026-08-31 |

The rule recorded for the first: *"If there is urgency, state it."* An urgent memo says
"This is urgent" and names the deadline; it does not stage a prop (the circled line, the
pencil, the counter) and let the image carry the demand. The prompt side of the same round
flagged "How did Emmett come out of a statement?" — metonymy that stops parsing.

**Fix pattern that satisfied the examples:** same speaker, same facts, the image replaced
with the plain statement. "This is urgent. The outbound delivery line on the July statement
is far out of line with what the trucks actually cost us, and the delivery sheet we hand
customers has to be corrected before the October statements go out."

### 11. Place metonymy for the deliverable, and the unpunctuated clause break

| Flagged | Where | Round |
| --- | --- | --- |
| "that is what goes on the door" | a prompt | 2026-09-08 |
| "What goes on the door" | a golden, `Keep out!A1` | 2026-09-08 |
| "Then the part their staff can act on the first morning." | a prompt | 2026-09-08 |
| "Whichever way a tech decides Vermed, they are wrong about between 35 and 56 items." | a golden | 2026-09-08 |
| "Read quickly that is the clean end of the account." | a golden, `Suppliers!A2` | found 2026-09-10 |

The heading for this class is **"Remove unclear LLM slang"**, with the standing instruction
**"State it clearly."** Two shapes sit under it. The first is a physical
surface standing in for the document: there is no door, and "what goes on the door" means the
posted screening list. The test is whether the phrase says which artifact it
is — *"Is that a posted warning, an exclusion list, a brand level restriction?"* The second is a
clause break left unpunctuated, so the sentence reads as a fragment and the sense only arrives
in the next one.

The metonymy pattern requires the subjectless relative (`what goes on the …`), because that is
what makes the surface stand in for the noun. A declarative with a real subject, "the notice
goes on the noticeboard", is literal and stays silent.

**Fix:** name the artifact. "What goes on the door" becomes "Lines to keep out of the magnet
room". And close the sentence: "Read quickly, that is the clean end of the account."

---

## Writing rules that follow

1. **No sentence whose only job is to sound like a person.** If deleting it loses no fact,
   it was a tell.
2. **Never restate a noun as itself.** No "X is X", no "still X", no "the whole story".
3. **Prefer the longer, flatter sentence.** Real memos over-explain; LLM pastiche compresses.
4. **One idiom per document, at most.** A single "we are not going to argue about it" reads
   human. Three in a page reads generated.
5. **Punctuate fragments into sentences** unless the document form genuinely uses labels
   (an invoice line, a spec paragraph, a table cell).
6. **Read the golden's prose under the same rule as the inputs.** A golden briefing has
   been flagged as hard as the memo beside it: the deliverable is prose too.

## Prompt-specific corollary

The same note pairs the style finding with a scope finding, and they share a root:

> The prompt is too prescriptive. It tells exactly where to find info and what to do with
> it. Tell the LLM what you want, what files are included - nothing more. Let it figure out
> what files to pull what info from, in what order, and how to make sense of it.

A prompt that walks the solver file by file needs connective idiom to carry itself between
the files, which is exactly where the tells cluster. Listing the files plainly and stating
the business ask removes the need for the voice. See
`memory/prompt-overspecification-giveaways.md`.
