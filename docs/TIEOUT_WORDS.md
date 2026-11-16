# Words tie-out — dist/index.html

Every piece of prose a reader meets on the built page, checked against its
source. The arithmetic is not re-checked here; three independent tie-outs
already cover it. What is checked is the sentence around the figure: what it
asserts, what it attributes, and whether the absolute words in it are true as
written.

**Page read:** `dist/index.html`, built 2026-11-16 09:43 (the file was rebuilt
during this tie-out; the only change was the two headline tile labels).
**Method:** the markup and the JavaScript string literals were extracted and
the page script was executed against a DOM stub, so every sentence below is
the text a reader actually gets, with the real numbers substituted. Default
state: businesses only, "small" under 500, table by company.

**Verdicts:** supported / partly supported / not supported / could not check.
A claim with no traceable source is not supported.

---

## Not fully supported, worst first

| # | Claim | Where | Verdict |
|---|---|---|---|
| 1 | The footer stops mid-way. Two whole sentences never reach the reader, including the only explanation of the "Sued" column and the only caveat that the suit count is a floor. | footer source line | **not supported** (and a defect) |
| 2 | "56 signed JobsOhio grant agreements were obtained … and **every one** carries the same Section 9(b)(ii)" | footer | **not supported** |
| 3 | "the other 22 on reporting that we could not tie to an Ohio document" | "What happened", para 1 | **not supported** |
| 4 | "the 44 that failed after being paid" / "$97.7 million" — includes four companies that were bought, one for $21 billion | "What happened", paras 1-2 | **not supported** |
| 5 | "**Most** are the company turning up in somebody else's bankruptcy" | rejected-candidates bar | **not supported** |
| 6 | "Honda's plants are **all** in Ohio" | home-state panel | **not supported** |
| 7 | "100 employees is below **every** SBA size standard, so **everything** counted as small here is small under the law in **any** industry" | SBA note, 100 setting | **not supported** |
| 8 | "found by scanning **every** recipient for distress headlines" / "**Every** recipient was scanned for signs of failure" | table key; rejected bar | partly supported |
| 9 | "51% of **everything in this panel**" | "What happened", para 2 | partly supported |
| 10 | "Three of the five … so they **should not be added together**" | table key | partly supported |
| 11 | "About half of all 63 ended in dismissal **with no terms on the record**" | "Does Ohio get the money back?", tile 2 | partly supported |
| 12 | "Ten of twelve programs publish **no repayment language**" / "no repayment language **at all**" | tile 1; footer | partly supported |
| 13 | "71.1% of dollars went to a recipient **whose agreement lets** JobsOhio demand repayment" | tile 1 | partly supported |
| 14 | "the amount shown is what the funded site was paid, **which is still running**" | failed-elsewhere filter bar | partly supported |
| 15 | "Reimbursement is separate again: the company spends first and JobsOhio repays documented costs" | footer | partly supported |
| 16 | "**Every** grant over $5,000 that JobsOhio reported paying … 2,415 **payments**" | subtitle | partly supported |
| 17 | "JobsOhio decides whether a company complied, whether to demand repayment, how much, and whether to waive it. Its standard agreement **says so**: [one quote]" | "Does Ohio get the money back?", closing line | partly supported |
| 18 | "A company name links to the best record available for it, **in that order**: its own 10-K, then the announcement, then its website" | table key, Sources | partly supported |
| 19 | "For manufacturing, **which is most of what JobsOhio funds**" | SBA note, 500 setting | partly supported |
| 20 | "One reversal, **PTT Global Chemical's** $20 million in FY2021" | tile 3 | partly supported |
| 21 | "Grade A: a filing made **under penalty of perjury**. An SEC 10-K or Exhibit 21, or an IRS return." | Evidence key and hover | partly supported |
| 22 | "the **subsidised** service" — British spelling, against house rule, and inconsistent with "Subsidized service ended" on the same page | table key | editorial |
| 23 | "Unresolved" legend swatch and "Unresolved: no size found" note, with zero unresolved businesses | both stacked-bar charts, fiscal-year chart | presentation |
| 24 | "ULTIUM CELLS alone took …" — raw all-caps payee name in prose | "What happened", para 2 | presentation |

---

## 1. Defect: the footer source line is cut in half

This is first because it is not a wording judgment, it is a bug that deletes
wording.

`dist/index.html` line 1036 ends:

```
  + "... That limits what is at risk; it is not a way to recover money already paid. "
```

and line 1037 begins:

```
  "“Sued by JobsOhio” is JobsOhio's own lawsuit against that company ... so this is a floor. " +
```

There is no `+` between them. JavaScript's automatic semicolon insertion ends
the assignment at the end of line 1036 and turns lines 1037-1038 into a dead
expression statement, which is evaluated and thrown away. Executing the page
script confirms it: `#src` ends at "…money already paid." and nothing after it
appears.

Three things are lost:

- The entire definition of the **"Sued" column**. It is the only column with a
  header on the table and no entry in the key under it, and the only place it
  was ever explained is this discarded sentence.
- The **floor caveat on the suit count**: "Suits filed in another county, in
  federal court or in another state would not appear, so this is a floor."
  Without it, "46 of 1,700 parent companies have **ever** been sued" stands as
  an unqualified absolute built on one county's docket.
- "Free to use. Built by Data 4 The People, November 13, 2026." The page
  carries no build date at all.

Present identically in `scripts/template.html` (lines 1036-1037) and in
`dist/embed.html`. One `+` fixes it. The missing date is separately stale:
`meta.built` is November 13 and the page was rebuilt November 16.

---

## 2. Headline, subtitle and the two tiles

| Claim as the reader sees it | Verdict | Checked against | Note |
|---|---|---|---|
| "Where JobsOhio's grant money went" | supported | n/a | Descriptive, no assertion. |
| "Every grant over $5,000 that JobsOhio reported paying on its IRS Form 990, fiscal years 2014 to 2025" | partly supported | `DATASETS.md` lines 14-18, 60-66, 105-120 | The $5,000 floor is the form's own rule ✓. But DATASETS records that the filer's own Schedule I line 2 and line 3 counts sum to 386 (FY2023) and 362 (FY2024) against 315 and 312 itemized rows — about 121 grantees the schedule does not itemize. "Every grant … that JobsOhio reported paying" is not true of those two years on the filer's own numbers. |
| "2,415 payments" | partly supported | `meta.rows` = 2415; 33 rows are negative | 33 of the 2,415 are reversal rows with negative cash. Calling a clawback a "payment" is loose; the back panel elsewhere calls them "negative rows". |
| "totaling $1.35 billion" | supported | `meta.cash_total` = 1,345,318,862 | Net of reversals. Note the back panel says "$1.37 billion" three panels later (gross). Both are right; a reader meets two totals. |
| "to 1,700 parent companies and organizations" | supported | `meta.parents` = 1700 | |
| "Each recipient is traced to its ultimate parent at the time of the grant, and the parent is sized by worldwide employees." | supported | `parents_table`: 0 of 1,469 businesses have a blank size band or blank HQ | "Each" holds. |
| "Share of the businesses JobsOhio paid that are small — 65%" | supported | recomputed from `parents_table` | |
| "35% are large. 1,469 parent companies paid." | supported | 1,469 business-class parents | Reads awkwardly ("companies paid" means "companies were paid"). |
| "Share of the dollars that went to small businesses — 19%" | supported | 19% of $956,764,828 business dollars | Denominator is business dollars, not the $1.35bn in the subtitle. The hint line's "$957 million paid" discloses it. |
| "81% of dollars went to large companies. $957 million paid." | supported | same | |

---

## 3. "Small companies are most of the recipients. Large ones get most of the money."

| Claim | Verdict | Checked against | Note |
|---|---|---|---|
| Chart title, both halves | supported | 65% of companies small; 81% of dollars large | Both "most" claims hold. |
| "Small: parent company under 500 employees worldwide at the time of the grant." | supported | `DATASETS.md` home-state and size method | |
| "Unresolved: no size found." + "Unresolved" legend swatch | presentation | 0 businesses unresolved; SVG title reads "Unresolved 0.0%" | A category and a legend entry with no members. Harmless but it invites a reader to look for a missing slice. |
| Legend "Small (under 500)" / "Large (500 or more)" | supported | `SMALL_AT` mapping; bands are `<100`, `100-499`, `500-4999`, `5000+` | |
| Tooltip "Small (under 500) · recipients / 65% / 950 parent companies" | supported | recomputed: 651 under 100 + 299 at 100-499 = 950 of 1,469 = 64.7% | |

---

## 4. "Most recipients are Ohio companies. Most dollars leave the state's headquarters map."

| Claim | Verdict | Checked against | Note |
|---|---|---|---|
| Chart title, both halves | supported | 66% of recipients Ohio; 64% of dollars elsewhere | |
| "Ohio: the ultimate parent was headquartered in Ohio at the time of the grant. The Ohio plant address does not count." | supported | `DATASETS.md` lines 1265-1272; "Recipient address is not headquarters. 84% of rows carry an Ohio address" | |
| "The largest recipient in the data, Intel Corporation, is Californian and took $125 million, 13.1% of all business dollars." | supported | `parents_table`: Intel $125,415,416, next is Honda at $52,433,335; 125,415,416 / 956,764,828 = 13.108% | "Largest" holds. |
| "Leave it out and the Ohio share of dollars goes 36.2% to 41.7%." | supported | `concentration.intel` | Computed in `09_analyze.py`, not typed. |
| "Ultium Cells is counted as Michigan, and that is a judgment rather than a reading." | supported | `DATASETS.md` lines 1269-1288 | The page states its own judgment and the cost of it. Good practice. |
| "It is a 50/50 joint venture of General Motors and LG Energy Solution, so it has no single ultimate parent, and its plant is in Warren." | supported | `DATASETS.md` 1271-1274 | |
| **"It sits here because Honda's plants are all in Ohio …"** | **not supported** | `DATASETS.md` line 1277 repeats the same wording; page `rows` show every Honda payment remitted to Marysville, Anna or Raymond | False of Honda, which has assembly plants in Alabama, Indiana, South Carolina and elsewhere. True only of the Honda plants in *this data*. Fix: "the Honda plants in this data are all in Ohio". `DATASETS.md` needs the same fix. |
| "and Fuyao's is in Moraine, and both are counted to their operating parents abroad" | supported | `DATASETS.md` 1278-1281; Fuyao payee rows: Moraine OH (FY2017, FY2018) and Lake Orion MI (FY2015) | Fuyao's Ohio plant is Moraine ✓. |
| "The money itself was split: $30.0 million to Warren, OH and $20.0 million to Detroit, MI, the second of those being General Motors' head office." | supported | `DATASETS.md` 1283-1285: "$30,000,000 … 7400 Tod Ave SW, Warren, and $20,000,000 to 300 Renaissance Center, Detroit" | |
| "Count it as Ohio instead and the Ohio share of dollars goes 36.2% to 41.4%." | supported | `concentration.ultium` | |

---

## 5. "Size and home state together"

| Claim | Verdict | Checked against | Note |
|---|---|---|---|
| "Share of dollars in each cell, with the share of parent companies underneath. Resolved recipients only." | supported | cells sum to 99.9%; 0 unresolved businesses | "Resolved recipients only" excludes nothing, because nothing is unresolved. |
| Cell values (16% / 2.9% / 20% / 61% of dollars) | supported | recomputed from `parents_table` | |
| "Worst case for this finding: if every unresolved or low-confidence recipient were counted the other way, at least 58% of dollars still went to large companies and at least 48% of recipients were still small." | supported | `worstCase()` re-run; 437 of 1,469 businesses are grade C or D | Honest construction: it flips C and D against the finding, and it does **not** claim the "most of the recipients are small" headline survives — 48% is not a majority, and the sentence only says "at least 48%". Consistent with the Evidence key ("C and D are counted against the finding in the worst case"). |

---

## 6. Fiscal-year chart

| Claim | Verdict | Checked against | Note |
|---|---|---|---|
| "Dollars paid each fiscal year, by company size" | supported | | |
| "Fiscal years end June 30." | supported | `DATASETS.md` line 83: "Fiscal year ends June 30; 'FY2024' means July 1, 2023 to June 30, 2024" | |
| "Grants are paid as companies submit costs, so one award can span several years." | supported | `program_terms.json` (reimbursement-based for the main grant programs); `DATASETS.md` 105-112 Schedule O quote on the cash basis | |
| "Read the early years with care. FY2014 holds 4 companies and $300,000." | supported | `DATASETS.md` lines 1398-1402: "only 4 companies and $300,000 are operating businesses" | Matches the businesses-only default exactly. |
| "A share computed on that few companies turns on one or two grants, so the bar is shown but the split should not be read as a trend." | supported | same passage: "its small-business share therefore turns on two $50,000 grants" | |
| "FY2012 and FY2013 are left out entirely: JobsOhio filed those returns on paper and no machine-readable copy exists." | supported | `DATASETS.md` line 63: "FY2012 and FY2013 are small and PDF-only" | "PDF-only" and "filed on paper" are a short step apart; the operative claim (no machine-readable copy) is sourced. |

---

## 7. The SBA size-standard note under "small means under"

Every number here ties out against `data/sba_size_standards.csv` (978 rows,
pulled from the eCFR renderer for 13 CFR 121.201 by
`scripts/28_sba_size_standards.py`). Recomputed independently:
978 industries; 500 receipts-based, 478 employee-based; employee thresholds
100 to 1,500; exactly 47 industries at 500; 346 manufacturing (NAICS 31-33)
industries, all employee-based, median 1,000.

| Claim | Verdict | Checked against | Note |
|---|---|---|---|
| "The SBA sets a separate threshold for each of 978 industries under 13 CFR 121.201" | supported | 978 rows | |
| "500 of them are measured by annual receipts rather than headcount at all" | supported | exactly 500 | |
| "among the 478 that count employees the line runs from 100 to 1,500" | supported | min 100, max 1,500 | |
| "Only 47 industries use exactly 500." | supported | exactly 47 | |
| "the median SBA threshold is 1,000 employees" (manufacturing) | supported | median of 346 = 1,000 | |
| "**For manufacturing, which is most of what JobsOhio funds**" | partly supported | `data/commitments.csv` industry labels: "Advanced Manufacturing" 36% of project rows, the largest single label but not a majority; next are Automotive 7%, Food and Agribusiness 7% | A plurality, not "most". `DATASETS.md` line 1104 makes the same claim and its own supporting note is weaker still ("coarse sector labels … for 64% of recipients"). Fix: "manufacturing, the largest sector in JobsOhio's own project reports". |
| "so this setting counts fewer companies as small than the SBA would" | supported | 500 < 1,000 | |
| "5,000 is well above every SBA size standard, the highest of which is 1,500 employees." | supported | max employee threshold 1,500 | Receipts standards are not headcounts, so "every SBA size standard" strictly means every employee-based one. Acceptable as written. |
| "At this setting 'small' means mid-sized, not small in law." | supported | same | |
| **"100 employees is below every SBA size standard, so everything counted as small here is small under the law in any industry. It is the strictest line on offer."** | **not supported** | 500 of the 978 industries measure size by average annual receipts; 13 industries have an employee standard of exactly 100 | Two problems. 100 is *equal to*, not below, the lowest employee standard. More seriously, in the 500 receipts-based industries a company with 40 employees can be far above the receipts cap, so "small under the law in any industry" cannot follow from a headcount at all. The note's own sibling (the 500 setting) says this. Fix: "Under 100 employees is below every SBA employee standard, so everything counted as small here is small in any industry that measures size by headcount." |

---

## 8. "Does Ohio get the money back?"

| Claim | Verdict | Checked against | Note |
|---|---|---|---|
| "Three numbers that have to be read together. A repayment clause in a contract is not the same as money returned." | supported | the panel's own three tiles; `README.md` line 112 | This is the frame the rest of the panel needs, and it is right. |
| **"71.1% of dollars went to a recipient whose agreement lets JobsOhio demand repayment"** | partly supported | `recourse`: agreement seen $8,179,352 + standard form $872,942,441 + published clawback $75,800,411 = $956,922,204 of $1,346,076,114 = 71.09% | Arithmetic ✓. But $872.9M of the $956.9M numerator — 91% of it — is "standard form", meaning the clause is **inferred** from other companies' agreements and was never seen for that recipient. The tile headline states inference as fact. The sub-line and the key do say "inferred, not seen", which is why this is partly rather than not supported. Fix: "went to a recipient whose agreement is seen or inferred to let JobsOhio demand repayment". |
| **"Ten of twelve programs publish no repayment language."** | partly supported | `data/program_terms.json`, all 12 read | 10 of 12 publish no *clawback* ✓ (only the Inclusion/Small Business Grant and the Ohio Site Inventory Program do). But two of those ten are loans, and the Revitalization Loan's published terms do state repayment — "principal and interest due on the published schedule". The page's own key knows this ("loan, repayable … which is not a performance clawback"). The footer's "no repayment language **at all**" is the harder version of the same overstatement. Fix: "publish no clawback". |
| "The clause is in the signed agreement instead, and 56 of those were obtained from court files." | supported | `docs/STORY_LEADS.md` lines 350-366, 750-756: "56 attach the whole signed agreement" | The count 56 is consistent across the source. |
| "46 of 1,700 parent companies have **ever** been sued by JobsOhio to get money back" | partly supported | `lawsuits.parents_sued` = 46; `data/jobsohio_lawsuits.csv` = 63 suits, Franklin County only | The figure ✓. The absolute "ever" rests on one county's docket. The caveat that answers it is the footer sentence the JS bug discards (finding 1). With that sentence restored this becomes supported. |
| "63 suits in the Franklin County Court of Common Pleas since 2018" | supported | `jobsohio_lawsuits.csv`: 63 rows with `kind=suit`, 63 distinct cases, earliest filed 2018 (2 in 2018) | |
| "seeking $13.5 million in total" | supported | `sought_total` = 13,548,404 | `STORY_LEADS.md` says $13,494,169 for 62 dockets; the $54k gap is the 63rd. Numbers, already tied out. |
| "9 of them name a company that never appears on the grant schedule at all, so whatever those are recovering is not in this data." | supported | `09_analyze.py` lines 545-556 and its comment | 11 suits have no matched recipient, but two of those *are* on the schedule and were dropped from the table for netting to zero or less. The code comment records exactly this ("an earlier version … said 11 where the answer is 9"). |
| **"About half of all 63 ended in dismissal with no terms on the record, so what was recovered is not public."** | partly supported | 34 of 63 outcomes mention dismissal (54%) ✓ "about half". But four of those dismissals carry settlement terms | Two are described in the project's own file as the only cases in the batch where a settlement figure appears (19CV001481) and where both the figure and the fact of payment are established (25CV010548). "No terms on the record" is false for those. Fix: "About half of all 63 ended in dismissal, and only two state a settlement figure, so what was recovered is mostly not public." |
| "1.9% of what JobsOhio paid out has come back" | supported | 26,040,088 / 1,371,358,950 = 1.90% | |
| "$26.0 million of $1.37 billion across 12 years, recorded as negative rows on the same tax returns." | supported | `meta.reversal_dollars`, `cash_payments_gross`, `reversal_rows` = 33; fy_max − fy_min + 1 = 12 | $1.37bn is gross; the subtitle's $1.35bn is net. Both correct, and the right choice for this ratio. |
| "Whether each one is a performance clawback or an accounting correction is not stated." | supported | `DATASETS.md` line ~431: "`Conditional` does not mean the money was clawed back … The columns describe documents, not outcomes" | |
| **"One reversal, PTT Global Chemical's $20 million in FY2021, is more than three quarters of it."** | partly supported | `DATASETS.md` lines 482-497: PTTGC America LLC, $20,000,000 reversed FY2021; 20,000,000 / 26,040,088 = 76.8% | "More than three quarters" ✓, just. The payee is **PTTGC America LLC**, the US subsidiary; "PTT Global Chemical" is the Thai parent. The page names parents elsewhere, so this is defensible, but the row a reader will search for says PTTGC America. |
| **"JobsOhio decides whether a company complied, whether to demand repayment, how much, and whether to waive it. Its standard agreement says so: 'Notwithstanding the terms of this Agreement, Grantor has the discretion to determine compliance.'"** | partly supported | `docs/STORY_LEADS.md` lines 860-872 | **The quotation is accurate word for word, and the attribution to the standard agreement is right**: it is the closing sentence of Section 5(a). But it supports only the first of the four things in the sentence before it. "Whether to waive it" is Section 5(c) ("Grantor has the discretion to waive non-compliance … and may waive repayment of all or a portion"); "how much" is the "all or a portion" of 9(b)(ii). Fix: "says so twice", and quote or cite 5(c) too. |
| "Where a case was dismissed, no filing states what, if anything, was paid." | partly supported | same as the dismissal row above | Contradicted by the two settled-and-dismissed cases where the figure is on the record. |

---

## 9. "What happened after the money went out"

| Claim | Verdict | Checked against | Note |
|---|---|---|---|
| "Counted on the company named on the Form 990, not its parent group, because that is the unit each finding was verified against." | supported | `summary.unit`; `09_analyze.py` lines 850-857 | |
| "$13.5 million / sued by JobsOhio to get money back / 63 suits, median $125,000 sought" | supported | `summary.sued` | The big number is dollars *sought*, where the other tiles are dollars *paid*. Disclosed in the sub-line. |
| "$14.7 million / went bankrupt or into receivership / 10 companies" | supported | `summary.failures.by_category` | |
| "$8.4 million / closed the funded Ohio site / 17 companies" | supported | same | |
| "$71.9 million / cut jobs at the funded site / 12 companies" | supported | same | |
| "$26.0 million / recorded as returned to JobsOhio / 1.9% of everything paid out" | supported | `summary.returned` | |
| "JobsOhio has filed 63 suits for a median of $125,000." | supported | `summary.sued.suits`, `median_sought` | |
| "33 of the 51 sued companies … employ fewer than 500 people and 20 fewer than 100" | supported | `sued.bands`: 20 + 13 = 33; all 51 banded | |
| "37 of the 44 that failed after being paid employ 500 or more and none is recorded under 100" | supported | `failures.bands`: 19 + 18 = 37; no `<100` key; all 44 banded | "None is **recorded** under 100" is the careful wording and it is right. |
| "35 of the 44 failed companies have a headcount from a filing or an official record, against 32 of 51 on the sued side, where 19 sit on a company website, a directory or a best guess." | supported | `failures.evidence`, `sued.evidence` | |
| "How firmly the failures themselves are evidenced is a separate question, and a harder one: 22 of the 44 rest on a court filing or the employer's own notice to the state …" | partly supported | `data/failures.csv` × `data/failure_sources.csv`, cross-tabbed | The 22 High-confidence findings break down as 14 state WARN notice, 2 court docket, 2 court filing, 2 other government notice, 1 SEC filing and **1 news article** (Avelo Airlines). So 18 of 22, not 22 of 22. |
| **"… and the other 22 on reporting that we could not tie to an Ohio document."** | **not supported** | same cross-tab | The 22 Medium-confidence findings break down as 10 government notice, 5 news article, 3 state WARN notice, 3 SEC filing, 1 court filing. **Fourteen of the 22 rest on a government notice or a court filing**; only 5 rest on a news article. The High/Medium grade in `failures.csv` measures how firmly the finding is established, not what kind of document it rests on, and this sentence converts one into the other. This is the same confusion the code comment immediately above it (`09_analyze.py` lines 606-618) was written to stop; the fix went half way. Fix: state it as the grade — "22 are graded High confidence and 22 Medium" — or recount by document type. |
| "What is not in doubt is the money: the companies it sued were paid a median of $132,000, the companies that failed a median of $500,000." | supported | `sued.median_paid` = 131,911; `failures.median_paid` = 500,000 | |
| **"the 44 that failed after being paid" / "$97.7 million"** | **not supported** as "failed" | `failures.csv`, category `Sold or absorbed`: Speedway LLC $1.7m (Marathon sold it to 7-Eleven for $21 billion), FirstMerit $0.5m (bought by Huntington), AK Steel $0.25m (bought by Cleveland-Cliffs), PPG $0.05m (sold its silicas business for $310 million) | Four of the 44 are acquisitions and divestitures, not failures. $2.5m of the $97.7m and 4 of the 44 companies. The key's own gloss for the category — "the recipient stopped existing as an independent company" — describes a change of owner, not a failure, and a $21 billion sale is not one on any reading. Either drop them from the "failed" count or rename the unit ("44 companies with a bad outcome after being paid"). |
| "Read the failed dollars with one company in mind. ULTIUM CELLS alone took $50.0 million of the $97.7 million" | supported (figure) | `failures.largest`, `failures.paid` | The payee name renders in raw capitals. |
| **"which is 51% of everything in this panel"** | partly supported | 50,000,000 / 97,709,323 = 51.2% | 51% of the **failed** dollars, not of "everything in this panel" — the panel also shows $13.5m sought and $26.0m returned. Worse for a reader: the three failure tiles on screen sum to $95.0m, not $97.7m, because "Sold or absorbed" ($2.5m) and "Subsidized service ended" ($0.2m) have no tile. Fix: "51% of the failed dollars". |
| "That is why the figure above is a median: the mean of the failed grants is $2.2 million, and almost all of the gap between the two is that one grant." | supported | `failures.mean_paid` = 2,220,666 | Leading with the median and naming the concentration is the right call. |
| "Each of these was then checked again on one question: was the operation that failed the operation the grant paid for? 3 companies came back no. They closed something in Ohio, but not the site the money went to, so their $3.9 million is not in the figures above." | supported | `failed_elsewhere`: Dana $3.7m, New Horizons Baking $0.1m, FedEx Supply Chain $0.05m = $3.85m | |
| "Every recipient was scanned for signs of failure, and 119 candidates were then checked one at a time. 72 were thrown out." | partly supported | `failures.csv` = exactly 119 rows; 44 confirmed + 3 failed-elsewhere + 72 rejected = 119 ✓ | The 119 and the 72 are exact. "Every recipient" is not — see §10. |

---

## 10. The table key

| Claim | Verdict | Checked against | Note |
|---|---|---|---|
| "**Evidence** grades how firmly the size and home state are established." + A/B/C/D short glosses and hovers | supported | `parents.csv` grading; `DATASETS.md`; 141 A, 891 B, 324 C, 113 D among businesses | |
| "Grade A: a filing made **under penalty of perjury**. An SEC 10-K or Exhibit 21, or an IRS return." | partly supported | n/a | True of an IRS return. A Form 10-K's officer certifications are made under 18 U.S.C. §1350, not a perjury declaration, and Exhibit 21 carries no certification of its own. Fix: "a filing carrying criminal penalties for a false statement". |
| "Grade B: an official or semi-official record. A JobsOhio or regional partner release naming the company, or a Department of Labor Form 5500 participant count." | supported | `data/f5500_participants.csv`; Form 5500 is a DOL/IRS/PBGC filing | |
| "Grade D: the owner could not be established. These are swept into the worst case against the finding." | **not supported, fixed November 16, 2026** | `data/parents.csv`; `worstCase()` flips C and D | The sweep half is right. The definition was wrong about all 186 rows that carry a D: every one names a parent, a home state and a size band, 145 cite at least one URL, and only 38 carry an explicit "nothing found" note for any field. What is thin is the evidence behind the answer, not the answer. The grade now says so. |
| "C and D are counted against the finding in the worst case." | supported | same | |
| "**Repayment clause** is whether a clause exists letting JobsOhio demand the money back, and how firmly we know it. It is not a statement that money was recovered: 1.9% has come back." | supported | `summary.returned.share_of_paid` | Exactly the right distinction, and the one the panel above it needs. |
| Seven grade glosses ("in this agreement", "in the standard agreement", "in the guidelines", "loan, repayable", "services, not cash", "none found", "program unknown") | supported | `program_terms.json`; `19_grant_conditions.py`; `STORY_LEADS.md` lead 9 | "in the standard agreement … so the clause is inferred, not seen" is honest about the weakest and largest category. "services, not cash … can bill the service value as liquidated damages" matches the Olive AI services agreement, the only instrument in the record using that phrase. |
| **"**After the grant** is a verified outcome at the funded operation, found by scanning every recipient for distress headlines and then checking each one against court dockets, SEC filings, state WARN notices and local news."** | partly supported | `data/distress_candidates.csv` (1,755 names) against `data/recipients.csv` + `data/grants_fy2025.csv` (1,789 recipients); `failures.csv` `flagged_by` | Two problems. (a) **Not every recipient was scanned.** About 20 have no scan row and no check row: 14 in FY2014-24 (Folded Pak, Bon-Ton Department Stores, Pactiv, Tramec Sloan, Webster Industries, AJM Packaging, MICC Manufacturing, Sky Climber Fabricating, TS Sales, E1 Digital Direct, BrightEdge, JKB Group, INEOS Pigments, Foundation Software) and 6 in FY2025 (Momentive Technologies, Ditsch USA, OMNOVA Solutions, Xaloy, StreetPops, Schaeffler Transmission). Bon-Ton is harmless — its two $100,000 grants were fully reversed in FY2020 and it nets to zero, so it is not on the page — but the others are simply unscanned. `DATASETS.md` line 450 still says "1,485 distinct recipients scanned", which is itself stale. (b) **The method is misdescribed.** 16 of the 44 confirmed failures were found by the Ohio WARN register join (`scripts/35_warn_join.py`), not by the headline scan; the sentence presents WARN as a checking source when for over a third of the count it was the detection source. Fix: "found by two passes — a distress-headline scan over the recipients and a join of Ohio's whole WARN register against them — and then checking each candidate against …". |
| **"Three of the five are failures of the thing Ohio paid for rather than of the company, so they should not be added together."** | partly supported | `summary.failures.by_category`: 10 + 17 + 12 + 4 + 1 = 44 companies, and $14,680,000 + $8,402,983 + $71,926,340 + $2,500,000 + $200,000 = $97,709,323 exactly | "Three of the five" is right (site closed, mass layoff, service ended). But the five categories are mutually exclusive and sum exactly to the headline 44 and $97.7m — and the page's own next paragraph adds them to get $97.7m. The caution reads as a double-counting warning when the real point is that the categories mean different things. Fix: "mean different things and should not be read as one total", or drop it, since the page adds them anyway. |
| Five category glosses (bankruptcy / site closed / mass layoff / sold / service ended) | supported with one problem | `failures.csv` categories and `ohio_outcome` text | "sold — the recipient stopped existing as an independent company" is accurate but describes something that is not a failure; see §9. |
| "the **subsidised** service, an airline route, stopped running" | editorial | house style; the page's own category label is "Subsidized service ended" | British spelling, against the standing rule, and inconsistent with itself one panel away. |
| "It is a floor, not a count: a failure without coverage is not in it, and a parent's filing that left the Ohio site running is excluded." | supported | `DATASETS.md` lines 468-474, the "why the published count is a floor" bullets, word for word | |
| "A label reading '· part' means only some of the money paid to that company group went to the operation that failed; hover for both figures and for which company it was." | supported | `renderTable()` badge logic; `09_analyze.py` payee-vs-parent split | |
| "And it counts companies that failed, not projects that never started … $28,599,868 went towards a Belmont County petrochemical plant that was never built, and none of the three recipients is in this count." | supported | `DATASETS.md` lines 475-497; `docs/TIEOUT_INDEPENDENT_3.md` §2.7 | The $28,599,868 is correctly **net**: PTTGC America is carried at $11,451,981 after the $20m reversal, so this figure does not double-count the money the "returned" tile reports. FirstEnergy Generation $12,408,019 + PTTGC $11,451,981 + Ohio-West Virginia Excavating $4,739,868 = $28,599,868 ✓. "None of the three" ✓ — none appears in `failures.csv`. This is the single best-sourced limitation statement on the page. |
| "**Sources** open in a new tab where one exists. … Every link was fetched and confirmed to resolve; where nothing did, the name is plain text rather than a dead link." | supported | `data/parent_links.csv`: 903 rows with status 200, 830 blank; 880 links on the page; `27_resolve_links.py` docstring: "A link that does not resolve is not written" | Holds for the company-name links and for the 47 failure sources (all `verified=yes`). |
| **"A company name links to the best record available for it, in that order: its own 10-K, then the announcement, then its website."** | partly supported | `parents_table` link kinds: company website 196, press release 169, **JobsOhio report or bulk data 130**, **reference page 127**, SEC filing 87, news article 86, 10-K 74, SEC search result 11 | 257 of the 880 links (29%) are a reference page (Wikipedia, ProPublica, a directory) or a JobsOhio report or bulk file. Neither is in the stated order. The per-link hovers label them honestly, which is why this is partly supported, but the key promises a three-rung ladder the data does not have. |
| "Smaller recipients, whose only public record is JobsOhio's own project report, are mostly unlinked." | partly supported | linked median cash $180,162; unlinked median $105,000; 820 of 1,700 unlinked | Directionally right, and the gap is real but modest. "Mostly unlinked" is not quantified anywhere. |
| "**Sued**" column header | **not supported** | nothing | No key entry, no hover on the header, and the one sentence that defined it is the discarded footer text (finding 1). As it stands the column is a label with no source. |
| Other column headers (Parent company, Type, Employees, HQ, Evidence, Paid, Years, Repayment clause, After the grant) | supported | all defined in the key or self-evident | |

---

## 11. Filter bars and row hovers

| Claim | Verdict | Checked against | Note |
|---|---|---|---|
| "These three companies did close an Ohio operation, but not the one the grant paid for. … They are not in the count, and **the amount shown is what the funded site was paid, which is still running**." | partly supported | `failed_elsewhere[].caveat` | Dana: "The funded sites are still running" ✓. New Horizons: "the Norwalk plant … which is still running" ✓. FedEx Supply Chain: the record says only "No Columbus closure for this payee appears in Ohio's notices for 2020 through 2026" — an absence of a notice, which `DATASETS.md` itself says "is not evidence that nothing happened". Fix: "which is still running, or for which Ohio holds no closure notice". |
| **"Most are the company turning up in somebody else's bankruptcy, which is the commonest false positive in work like this."** | **not supported** | 72 rejected rows in `failures.csv`: 53 "Not a failure", 17 "Different company", 1 "Before the grant", 1 "Unresolved". Only 18 of the 72 mention a bankruptcy at all, and 9 mention a creditor, landlord, customer or supplier | The largest group is a headline using "close" or "shut" for something that is not a business failure (Case Western, Cleveland State, GE Jacksonville, Aer Lingus schedule cuts). The creditor-in-someone-else's-bankruptcy type is real (JPMorgan, British Airways) but it is about a quarter at most. Fix: "Most are a headline about something that was not a business failure, or a different company with a similar name." |
| "Every candidate the scan flagged that was checked and thrown out, with the reason. … These are not failures and none is in the count." | supported | 72 rejected, none in `summary.failures` | |
| "Filtered to companies that [outcome]. These rows are the companies named on the Form 990 that actually failed, not their parent groups … Where a parent also paid other companies that did not fail, only the failed one is shown and the amount is its own." | supported | `failed_payees` construction; `09_analyze.py` lines 517-534 | |
| "These are parent groups, so the count can be lower than the tile where two payees share a parent." | supported | same | |
| Failure hover: category, event, date, confidence, the "part" split, caveat, court, docket, source, paywall flag | supported | `failures.csv`, `failure_sources.csv` (1 of 47 paywalled) | |
| WARN hover: "This is the employer's own filing with the state, for the county the money was paid into." / "…for a county the grant money never reached, so it records a failure somewhere else." / "Whether it is the county the money was paid into could not be checked, because the payments went to an out-of-state address." | supported | `DATASETS.md` lines 1366-1375: of 27 matched notices, 17 yes, 3 no, 7 blank | Three honest states rather than two. Exactly right. |
| "Ohio has no layoff notice for this company." + the reason | supported | `33_match_warn.py`; `DATASETS.md` lines 1352-1364 (CoverMyMeds, Hyland, Speedway, Sauder) | |
| Suit hover: case, filed, sought, outcome, "Opens the Franklin County Clerk of Courts. The clerk asks you to accept a disclaimer first." | supported | `jobsohio_lawsuits.csv`; the constructed `caseSearch?…reallySubmit=true` URL | |
| Link-kind hovers (10-K "Some are older filings"; "reference page … not its own site"; "a JobsOhio report, or a government bulk file, where this company appears among many others") | supported | `27_resolve_links.py` docstring, which records the audit that produced them | |

---

## 12. Footer source line

Everything below the break described in finding 1 never renders. Verdicts are
given for the whole intended text, since the fix is one character.

| Claim | Verdict | Checked against | Note |
|---|---|---|---|
| "Source: JobsOhio Form 990, Schedule I, fiscal years 2014 to 2025 (IRS e-file data)." | supported | `DATASETS.md` lines 12-30 | |
| "Schedule I lists grants over $5,000 on a cash basis, so the dollars are what was paid in each year, not what was committed." | supported | `DATASETS.md` lines 105-112, Schedule O quote: "Schedule I is prepared on the cash basis of accounting" | |
| "Each payee was traced to its ultimate parent at the time of the grant using SEC filings, Form 5500 plan data, JobsOhio and regional partner releases, and company sources; the evidence grade shows which." | supported | `parents.csv`, `edgar_ein_matches.csv`, `f5500_participants.csv` | |
| "Universities, hospitals, governments, nonprofits and site developers are shown separately from operating businesses." | supported | `CLASS_LABEL`; the Count control | |
| "Ten of its twelve programs publish no repayment language **at all**" | partly supported | see §8 | The "at all" makes the loan overstatement worse. |
| "**56** signed JobsOhio grant agreements were obtained from Franklin County court files, **spanning 2013 to 2023**" | supported | `STORY_LEADS.md` lines 362-363, 757-764: "56 attach the whole signed contract"; "identical across four drafting generations of the form, 2013 through 2023" | |
| "and **every one** carries the same Section 9(b)(ii), 'Demand Repayment of Grant Funds': 'Grantor may demand repayment of all or a portion of Grant Funds disbursed.'" | **not supported** | `STORY_LEADS.md` lines 361-366 | The **quotation is accurate word for word** and the section number and heading are right. The count is not. The project's own finding: the sentence "appears word for word in **49 of the 62 complaints read**", 56 attach the whole agreement, and "**six attached agreements carry no recorded 9(b)(ii) text**, because the complaint did not quote it and the exhibit was not read past its first page." It then writes the fix itself: "The defensible claim is that every agreement **whose remedy clause was actually read** carries the identical sentence." The page publishes the version the source file explicitly rejected. The same overstatement is in the "in the standard agreement" hover text generated by `19_grant_conditions.py` line 86 ("All of them, 2013 to 2023, carry the same Section 9(b)(ii) repayment clause"). Fix: "and every one whose remedy clause could be read carries the same Section 9(b)(ii)". |
| "'In this agreement' means this company's own signed contract is in a court file. 'In the standard agreement' means it was paid under a program whose agreements were obtained and are identical, so the clause is inferred rather than seen." | supported | `19_grant_conditions.py`; `DATASETS.md` line 692 | |
| "'None found' means neither: nothing published and no agreement ever obtained, which is where the air service grants to airlines sit." | supported | `program_terms.json` #7 Commercial Air Service Restoration: "No repayment, clawback or recapture language in the published guidelines"; `STORY_LEADS.md` line 1149 | |
| "A clause is not a recovery. JobsOhio decides whether to demand repayment, how much, and whether to waive it, and the agreement says so: 'Grantor has the discretion to determine compliance.'" | partly supported | `STORY_LEADS.md` lines 860-872, Section 5(a) | Quote accurate; see §8 on the waiver half resting on Section 5(c), which is not quoted. |
| "It has filed 63 suits, reaching 46 of these 1,700 parent companies, seeking $13.5 million, and $26.0 million has come back across 12 years, 1.9% of what went out." | supported | `summary.sued`, `lawsuits.parents_sued`, `summary.returned` | |
| **"Reimbursement is separate again: the company spends first and JobsOhio repays documented costs, so a company that never spends never collects. That limits what is at risk; it is not a way to recover money already paid."** | partly supported | `program_terms.json`; `STORY_LEADS.md` "Reimbursement really does hold money back" (JIT Packaging: $75,000 authorised, $16,724 drawn, which is all JobsOhio sued for) | The **reasoning is right and well evidenced** — the JIT Packaging and Champlain dockets are direct proof that reimbursement limits exposure and is not a recovery route. What is overstated is the scope. `program_terms.json` records reimbursement as published for the Economic Development, Workforce and R&D programs, but for the **main Revitalization Grant** — the program that paid $30,000,000 of the Belmont money — it says "Not stated … No reimbursement sentence is published for it", reimbursement being published only for the $200,000 Phase II Assessment Fund. And Champlain shows $108,375.03 "advanced outside the normal reimbursement process". Fix: "Most programs publish a reimbursement rule: the company spends first …". |
| "'Sued by JobsOhio' is JobsOhio's own lawsuit … Suits filed in another county, in federal court or in another state would not appear, so this is a floor." | **does not render** | finding 1 | Correct as written and needed; it is the caveat the "ever been sued" absolute depends on. |
| "Free to use. Built by Data 4 The People, [date]." | **does not render** | finding 1 | And `meta.built` says November 13 for a page rebuilt November 16. |

---

## 13. Not on the page, and worth a line

- **The pandemic is never mentioned in any sentence a reader meets.** That is
  mostly a strength — the page makes no pandemic claim to get wrong. But the
  "After the grant" key offers WARN notices as a source without saying that
  Ohio's register **starts in 2020**, that 46% of all 810 notices are 2020
  alone, or that `scripts/35_warn_join.py` holds the March-June 2020 window to
  a higher bar precisely because so much of it was temporary. A reader cannot
  tell from the page that the WARN evidence covers only the back half of the
  period. `DATASETS.md` lines 1336-1350 and
  `docs/TIEOUT_INDEPENDENT_3.md` §2.8 have the material; one clause in the key
  would carry it.
- **The "This is the short version" block** (`.openfull`) is `display:none` on
  `index.html` and only renders in `dist/embed.html`. Its claim "Every figure
  here is in the full tool" was not checked for the embed, since it is not
  reader-visible on the page under tie-out.

---

## 14. Source files that have gone stale

Not reader-visible, but `DATASETS.md` is the method of record and the standing
rule is to keep it current in the same commit as the change.

| File | Stale text | Current value |
|---|---|---|
| `DATASETS.md` line 450 | "1,485 distinct recipients scanned: 20 hard signals, 64 soft" | `distress_candidates.csv` holds 1,755 |
| `DATASETS.md` line 1104 | "which is most of what JobsOhio funds" | Advanced Manufacturing is 36% of project rows, a plurality |
| `DATASETS.md` line 1277 | "Honda's plants are all in Ohio" | true only of the Honda plants in this data |
| `DATASETS.md` line 1281 | "Honda's $47,433,335" | $52,433,335 after FY2025 |
| `DATASETS.md` lines 1258-1262 | "of the 51 sued … 20 employ fewer than 100" ✓, but the surrounding passage still says "22 of the 44" against an earlier "21 of 43" | 22 of 44 ✓ current |
| `09_analyze.py` lines 850-857 | comment: "would turn 29 companies and $86.5m into 26 and $96.5m" | 44 companies and $97.7m |
| `09_analyze.py` line 617 | comment: "it is 21 of 43, not 35" | 22 of 44 |
| `renderKey()` comment | "71 of the 102 candidates were rejected" | 72 of 119 |
| `docs/TIEOUT_INDEPENDENT_3.md` | "43 companies", "41 of the 43" throughout | 44 companies |

---

## What was checked and could not be resolved

| Item | Why |
|---|---|
| "JobsOhio filed those returns on paper and no machine-readable copy exists" (FY2012-13) | `DATASETS.md` records them as "small and PDF-only". No independent check of the IRS e-file index was run; the web-search budget for this session was spent. Marked supported on the project's own record. |
| Whether the 500 receipts-based SBA industries would in fact catch any recipient counted as small at the 100 setting | would need a per-company NAICS code and revenue, which the project does not have and says so. The claim is unsupportable as written either way. |
| Whether the 14 unscanned FY2014-24 recipients include a real failure | Bon-Ton was checked and is harmless (fully reversed, nets to zero, not on the page). The other 13 were not individually researched; that is the gap the fix should close, not this tie-out. |
