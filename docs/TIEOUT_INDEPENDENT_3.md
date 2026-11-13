# Independent tie-out #3 — the failure block

> **Scope.** This pass checks the failure block only: the 43 confirmed failures
> and $97,009,323, how they were found, and whether each one holds. It was
> written from `DATASETS.md` and the data files alone. `09_analyze.py`,
> `30_audit_summary.py`, `31_audit_failures.py`, `33_match_warn.py`,
> `35_warn_join.py`, `37_merge_warncheck.py`, `TIEOUT.md`, `STATUS.md` and
> `docs/STORY_LEADS.md` were not read. Tie-out #2 was read as context.
>
> **My code:**
> `/private/tmp/claude-501/-Users-ericpachman-PycharmProjects-JobsOhioSmallBiz/a1dd38a2-e88f-41d4-b535-c2283e8b5104/scratchpad/tieout3/`
> (`recompute.py` the Part 1 block, `warnjoin.py` / `warnjoin2.py` /
> `warnjoin3.py` three independent WARN joins, `warnparse.py` a re-parse of
> Ohio's register from the cached year CSVs, `part3.py` and `headline.py` the
> Part 3 items). Date of run: November 13, 2026.

**Headline verdict.** *The arithmetic is clean. The labelling is not.*

Every published figure in the failure block reproduces from my own code, to
the dollar and to sixteen decimal places on the shares. Nothing in Part 1
differs. The grant join behind it is exact: every one of the 43 `paid` figures
equals that payee's net Schedule I cash under its own EIN, and Ohio's whole
WARN register re-parses to 810 notices and 106,128 affected without a single
row's difference.

Three things in the block I would not hand to a reporter as they stand.

1. **The page says "35 of the 43 failures rest on a filing or an official
   record."** That 35 is the A/B research grade for the company's *employee
   count*, not for the failure. Petmin's Chapter 7 petition counts as weak
   because Petmin's headcount came off a South African corporate page;
   CoverMyMeds, which has no Ohio job number and no state notice, counts as
   firm because McKesson's 10-K gives a headcount. On the grade that actually
   measures the failure evidence the number is **21 of 43**, not 35.
2. **Ultium Cells is 51.5% of the published failure dollars and the plant is
   open.** The project's own row records that 850 of the 1,300 cuts were
   temporary and that workers have since been recalled.
3. **Speedway's category is contradicted by its own file.** It is published as
   "Mass layoff at the funded site"; `failure_warn.csv` explains the missing
   state notice by saying the Enon cut was fewer than 35 people.

And one gap the method cannot see, which a reporter will find: **$28.6 million
went to an ethane cracker that was never built, and none of it is a candidate.**

---

## 1. Every figure checked

### 1.1 Verdicts and the candidate set

| Figure | Project | Mine | Difference | Verdict |
|---|---:|---:|---:|---|
| Confirmed failures: companies | 43 | 43 | 0 | ties |
| Confirmed failures: paid | $97,009,323 | $97,009,323 | $0 | ties |
| Failed away from the funded site: n / paid | 3 / $3,850,000 | 3 / $3,850,000 | 0 | ties |
| Not a failure | *52 (DATASETS.md)* | **53** | 1 | **doc is stale** |
| Different company | 17 | 17 | 0 | ties |
| Before the grant | 1 | 1 | 0 | ties |
| Unresolved | *1 (DATASETS.md)* | **0** | 1 | **doc is stale** |
| All verdicts sum to the rows in `failures.csv` | 117 | 117 | 0 | ties |

The two stale rows cancel, so the total is right. `Goodlevel Enterprises`,
which `DATASETS.md` still lists as unresolved, now carries `Not a failure`.
`DATASETS.md` also still says "84 candidates checked one at a time"; the file
holds 117.

### 1.2 The five categories

| Category | Project companies | Mine | Project paid | Mine | Verdict |
|---|---:|---:|---:|---:|---|
| Mass layoff at the funded site | 12 | 12 | $72,926,340 | $72,926,340 | ties |
| Bankruptcy or receivership | 10 | 10 | $14,680,000 | $14,680,000 | ties |
| Funded site closed | 17 | 17 | $8,402,983 | $8,402,983 | ties |
| Sold or absorbed | 3 | 3 | $800,000 | $800,000 | ties |
| Subsidized service ended | 1 | 1 | $200,000 | $200,000 | ties |
| **Sum** | **43** | **43** | **$97,009,323** | **$97,009,323** | ties |

### 1.3 Central tendency and concentration

| Figure | Project | Mine | Difference | Verdict |
|---|---:|---:|---:|---|
| Median paid | $500,000 | $500,000 | $0 | ties |
| Mean paid | $2,256,031 | $2,256,030.77 → $2,256,031 | $0 | ties |
| Largest | $50,000,000 | $50,000,000 | $0 | ties |
| Largest name | ULTIUM CELLS | ULTIUM CELLS | — | ties |
| Largest share | .5154143792963074 | .5154143792963074 | 0 | ties |
| Top three share | — | 68.67% | — | computed |
| Median / mean without Ultium | — | $462,500 / $1,119,269 | — | computed |
| Companies carrying $0 | — | **2** | — | see 2.6 |

### 1.4 Bands and the evidence split

| Figure | Project | Mine | Difference | Verdict |
|---|---:|---:|---:|---|
| Band `<100` | absent | 0 | 0 | ties |
| Band `100-499` | 7 | 7 | 0 | ties |
| Band `500-4999` | 18 | 18 | 0 | ties |
| Band `5000+` | 18 | 18 | 0 | ties |
| Bands sum | 43 | 43 | 0 | ties |
| `evidence.n` | 43 | 43 | 0 | ties |
| `evidence.a_or_b` | 35 | 35 | 0 | **reproduces, but measures the wrong thing — 2.1** |
| `evidence.weak` | 8 | 8 | 0 | same |
| Failure-verification grade (`failures.csv`) | not published | **21 High / 22 Medium** | — | **the figure the sentence claims** |

### 1.5 Failures that were also sued

| Figure | Project | Mine | Verdict |
|---|---:|---:|---|
| Confirmed failures with a JobsOhio suit | 3 (`sued:true` on three rows) | 3 | ties |
| Which | Olive AI, Republic Steel, Mitec Powertrain | same | ties |
| Their paid dollars | — | **$1,060,770** (Olive AI $560,770, Republic Steel $500,000, Mitec $0) | computed |
| Sums pleaded against them | — | $598,420.17 / $300,000 / $200,000 | computed |

Worth saying on the page: **JobsOhio sued 3 of the 43, over about $1.1 million
of the $97.0 million.** The recourse story and the failure story barely touch.

### 1.6 `paid` against `grants_raw.csv`, by EIN

| Check | Result |
|---|---|
| Each of the 43 `paid` figures vs. the sum of that EIN's rows in `grants_raw.csv` | **43 of 43 tie, $0 difference** |
| Each of the 43 vs. `parents.csv` `total_cash` | **43 of 43 tie** |
| Same two checks across all 117 rows, every verdict | **117 of 117 tie** |
| Speedway EIN disambiguation (two Speedway LLCs) | correct one used, `EIN:271287018`, $1,700,000 |

### 1.7 The three views in `dist/data.json`

| View | Project rows | Mine | Ids match `failures.csv`? | Verdict |
|---|---:|---:|---|---|
| `failed_payees` | 43 | 43 | yes, exactly | ties |
| `failed_elsewhere` | 3 | 3 | yes | ties |
| `rejected` | 71 | 71 | yes (Not a failure + Different company + Before the grant) | ties |
| `failed_payees` cash sum | $97,009,323 | $97,009,323 | — | ties |
| `failures.parent_cash_total` − `payee_cash_total` | $9,015,727 | $9,015,727 | — | ties |
| `failures.matched_to_a_parent` | 41 of 43 | 41 (the two $0 payees have no parent above zero) | — | ties |

### 1.8 Ohio's WARN register, re-parsed from source

| Figure | Project (`notices.csv`) | My re-parse of `data/warn/csv/*.csv` | Verdict |
|---|---:|---:|---|
| Notices | 810 | 810 | ties |
| By year 2020 / 2021 / 2022 / 2023 / 2024 / 2025 / current | 376 / 29 / 59 / 85 / 93 / 89 / 79 | identical | ties |
| Sum of affected | 106,128 | 106,128 | ties |
| Rows in one and not the other | — | **0 in either direction** | ties |
| March 1 – June 30 2020 notices | 225 (28%) | 225 (27.8%) | ties |
| `covid_window` flag vs. that date test, in `warn_join.csv` | — | **0 disagreements in 201 rows** | ties |

---

## 2. Method concerns

### 2.1 The "evidence" sentence on the page measures the wrong thing

**This is live, and it is the finding I would fix first.**

`dist/index.html` renders:

> "…**35 of the 43 failures rest on a filing or an official record**, against
> 32 of 51 on the sued side, where 19 sit on a company website, a directory or
> a best guess."

`summary.failures.evidence.a_or_b` is the count of A and B grades in the
`confidence` column of **`parents.csv`**. That column grades how well the
company's **employee band and headquarters** are evidenced. It is the same
grade that feeds the `confidence` panel and the worst case. It has nothing to
do with the failure.

`failures.csv` has its own `confidence` column, High or Medium, and that is the
grade of the failure verification. The two do not agree:

| Company | Failure evidence | What it rests on | `parents.csv` grade | Panel counts it as |
|---|---|---|---|---|
| Petmin USA | High | Chapter 7 petition, docket read in full | C (`petmin.co.za`) | **weak** |
| Nestlé USA | Medium | company announcement, no WARN for the 2027 closure | C (Wikipedia) | **weak** |
| CoverMyMeds | Medium | **no Ohio job number, no state notice** | A (McKesson 10-K) | **firm** |
| Speedway | Medium | **own file says the Enon cut was under 35** | A (Marathon 10-K) | **firm** |
| Ultium Cells | Medium | WARN, 484 permanent of 1,300, plant open | B (`tribtoday.com`) | **firm** |

On the grade that does measure the failure, the sentence is **21 of 43**, not
35 of 43. The mirror claim about the sued side has the same defect; tie-out #2
caught the arithmetic there but not the semantics.

**Fix:** compute `summary.failures.evidence` from `failures.csv.confidence`,
and say which grade the sentence is quoting. If both are wanted, label them
differently — "the failure is documented" and "the company's size is
documented" are two different claims.

### 2.2 Ultium Cells is half the money and the plant is running

$50,000,000, **51.5% of the published failure dollars**, category "Mass layoff
at the funded site", confidence Medium. What the project's own row says:

- 1,300 jobs cut from January 5, 2026, which the state notice breaks out as
  **484 permanent and 850 temporary**.
- "The plant stayed open."
- *Business Journal Daily*, 2026-08-27: "**Ultium Cells in Lordstown recalls
  laid-off workers**."
- JobsOhio's own November 2020 commitment was **1,000 jobs created**.

So the single largest entry in the block is a plant that is open, where the
majority of the cut was temporary and has been partly reversed, and where the
permanent cut of 484 is set against a job commitment of 1,000 that the project
has not tested. The page does say Ultium is 52% of the panel and does lead with
the median, which is the right instinct. It is not enough. A reporter handed
"43 companies, $97 million" and a tool will discover within an hour that half
the money is a battery plant that is hiring back, and the rest of the block
will be discounted with it.

**Recommendation, one:** publish the failure total **both ways** — $97.0m with
Ultium, $47.0m without — and give Ultium its own `caveat` string saying the
plant is open, 850 of the 1,300 were temporary, and workers have been recalled.
The `caveat` field for Ultium is currently empty; the recall is buried in
`notes`, which the page does not render.

### 2.3 Three categories are not supported by the evidence recorded under them

**Speedway LLC, $1,700,000, "Mass layoff at the funded site."** The row's own
account: 7-Eleven cut "fewer than 35 jobs at the Enon headquarters in October
2021 and cut more Enon staff in July 2022 as part of about 880 corporate job
cuts"; "the exact Enon job count for 2022 was not published."
`failure_warn.csv` explains the missing state notice as "the reported Enon cut
was fewer than 35 people in October 2021, which is below the 50 that triggers a
notice." **No mass layoff at the funded site is established anywhere in the
file.** I would not hand this to a reporter. It is a company that was sold out
of state and whose Ohio head office was cut back during the integration, which
is a real finding and a different one.

**CoverMyMeds LLC, $6,613,235, "Mass layoff at the funded site."** 815 jobs cut
company-wide; "the Ohio share was not broken out"; no state notice. The
evidence that the *Ohio site* had a mass layoff is a sublease listing. The
stated reason for the missing notice — "Ohio requires a notice only for 50 or
more at one site, so the threshold can be cleared without a notice" — is an
argument that absence is not disproof. It is not evidence of presence. Second
largest row in the block after Ultium.

**Hyland Software Inc, $2,500,001, "Mass layoff at the funded site."** Same
shape: 1,000 cut, 20% of a global workforce, Ohio share never disclosed, no
state notice, two Westlake buildings listed for sale. Stronger than CoverMyMeds
because Hyland is headquartered in Westlake, but still no Ohio number.

Together these three are **$10,813,236**, 11% of the block, carrying a
site-level category that no site-level number supports.

**Sauder Woodworking Co, $200,000**, is the fourth and the project grades it
honestly already: "a real gap rather than a threshold… the 150 figure rests on
press reporting alone." I checked the premise and it holds — Ohio's register
does record tiny notices in that window (Fellers LLC, Sharonville, **1**
affected, 8/27/2025; First Student, Cincinnati, **39 part time**, 8/18/2025),
so a 150-person permanent cut at Archbold should have produced one.

**Recommendation, two:** rename the category for Speedway, CoverMyMeds and
Hyland to something the evidence carries — "company-wide cuts, Ohio share not
disclosed" — or state the limit in the `caveat` for each. Keep the dollars;
change the claim.

### 2.4 The funded-site test: two rows where "same site" is not supported

`sitecheck.json` covers all 46 (43 confirmed + 3 away), with no row missing and
no extra. Verdicts: **37 same site, 5 partly, 3 different site, 1 unresolved.**
`DATASETS.md` still says "24 … 4 … 3" and names four `partly` rows; there are
five and one `unresolved`.

Two rows do not clear the test:

| Row | Verdict | `same_site` | What the addresses say |
|---|---|---|---|
| **Pier 1 Imports (US) Inc**, $30,000 | **unresolved** | false | funded 5701 Meadows Drive, **Grove City**; failed 5235 Westpoint Dr, **Groveport**. Different places. No JobsOhio project record for Pier 1. The file's own instruction: "do not assert that the $30,000 paid for the Groveport building." |
| **ATW Ohio LLC**, $261,110 | partly | false | funded site is 200 Front Street, Mt Orab (Brown County) and the failed site is the same address, but JobsOhio's project record also covers Clermont County, which stayed open. |

Pier 1 is in the count of 43 with a funded-site verdict of `unresolved`. Dollars
are trivial; the count is not, because "43 companies" is the headline. It also
gets no badge on the page — `template.html` adds "· partly" only for
`verdict === "partly"`, so an `unresolved` row renders like any other.

Two further inconsistencies worth fixing because downstream code reads them:

- `same_site` is encoded differently for rows with the same verdict. Multi-Color,
  Nestlé, FirstMerit and AK Steel are `partly` with `same_site: true`; ATW is
  `partly` with `same_site: false`.
- Seven matched notices carry a blank `notice_at_funded_site` (GXO, Air
  Wisconsin, Pixelle, ATW, Dorel, Morgan Truck Body, syncreon). The page's
  tooltip has only a `=== "no"` branch, so a blank renders as "This is the
  employer's own filing with the state, **for the county the money was paid
  into**" — asserting the test's result for rows where it was never run. The
  site check independently says "same site" for six of the seven, so the
  substance survives; the sentence should not be printed on an undetermined row.

### 2.5 The WARN join — four recipients it missed, and one of them is $1.5 million

I ran three independent joins against all 1,789 recipients and both their payee
and parent names: a loose distinctive-token join, a strict head-of-name join,
and an exact-normalised-name join. The matches the project *made* are sound —
I found no confirmed failure whose matched notice is implausibly a different
company. The misses are the problem.

**Not present anywhere in `warn_join.csv` or `failures.csv`:**

| Recipient | Paid | Ohio WARN notice | Why it matters |
|---|---:|---|---|
| **TOLEDO INNOVATION CENTER LANDLORD LLC**, parent **Bitwise Industries** | **$1,500,000** (FY2023) | *Bitwise Industries, Inc.*, Toledo/Lucas, 18 affected, 6/14/23 | Exact parent-name match. JobsOhio committed a $1,500,000 Revitalization Grant and a $3,000,000 Revitalization Loan to "Bitwise, Inc. (BW Industries Inc.)", Lucas County, March 2022, for 378 jobs. Bitwise collapsed in mid-2023. The grant was drawn in full in the same fiscal year as the collapse. |
| **TECHNICOTE INC**, parent Beontag | **$700,000** (FY2024 + FY2025) | *Technicote Inc dba Beontag*, **Trotwood/Montgomery**, 53 affected, Layoff, received 3/25/2026 | The payee name is the notice name. The FY2025 payment was remitted to **Trotwood**, the notice's own city. JobsOhio committed $700,000 in Dec 2023 for **163 jobs created / 70 retained** in Montgomery County; the full $700,000 was drawn; 53 were laid off 15 months later. |
| **FirstEnergy Generation LLC** | **$12,408,019** (FY2017) | *Energy Harbor Generation LLC*, Stratton/Jefferson, 140 affected, 1/13/23 | Successor-entity name the join cannot see. The notice is the Sammis plant, not the funded Belmont County site, so it is probably not a funded-site failure — but see 2.7. |
| **Keihin Thermal Technology of America Inc** | $50,000 (FY2018) | *MAHLE Thermal and Fluid Systems*, Mt. Sterling/Madison, 141 affected, Closure, 9/30/2025 | Successor-entity name. MAHLE took over Keihin's thermal business; Mt. Sterling is the Keihin plant. Small money, same blind spot. |

Two parent-level exact matches are also absent and are probably correct to
leave out, but should be recorded as decisions rather than omissions:
Worthington Industries (Wooster/Wayne, 120 affected, 2/14/20) against
`THE WORTHINGTON STEEL COMPANY` ($75,000) and `Clarkwestern Dietrich Building
Systems LLC` ($300,000); and Amcor Flexibles North America (Akron/Summit, 109,
12/3/20) against `Amcor Rigid Plastics USA LLC` ($400,000).

**The likeliest mechanism for Bitwise**, which I could not confirm without
reading `35_warn_join.py`: the `parent` field carries research prose in
parentheses — "Bitwise Industries (joint venture with ProMedica Health System)".
Tokenised whole, the overlap with "Bitwise Industries, Inc." falls to about
0.3, below any sensible threshold. Miami University ("Miami University (State
of Ohio public university)") and Clarkwestern ("Worthington Industries, Inc.
(joint-venture partner)") are both absent and both carry a parenthetical. **If
the join does not strip parentheticals from `parent` before matching, every
parent with a research note in its name is invisible to it.** That is worth one
test run.

**Recommendation, three:** strip parentheticals from `parent` before the join,
re-run it, and verify Technicote and Bitwise by hand. Technicote looks like a
clean addition to the 43 on the facts available; Bitwise needs a funded-site
check because the payee is a landlord entity classed `site_development`.

### 2.6 Two of the 43 were paid nothing

`CURATION FOODS INC` and `MITEC POWERTRAIN INC` carry `paid = 0`. Both were paid
and then fully reversed — $350,000 in FY2021 against −$350,000 in FY2022, and
$200,000 in FY2019 against −$200,000 in FY2020. The research on both is
excellent and the `caveat` on each says so plainly.

Two consequences the page does not state:

- Neither company is among the **1,700 parents** anywhere else on the site,
  because `DATASETS.md`'s own rule drops a parent whose net is zero or less.
  So "43 companies" and "1,700 companies" are counted on different rules, and
  41 of the 43 are in the 1,700. `failures.matched_to_a_parent: 41` records
  this but nothing explains it.
- "43 companies failed after being paid" is true of 41. For two of them Ohio
  got everything back. That is the *good* news in the dataset and Mitec's own
  row argues it should be led with, not hidden in a hover.

### 2.7 The ethane cracker that was never built — $28.6 million the method cannot see

This is the largest hole I found, and it is structural rather than a bug.

| Recipient | Paid (net) | Years | What for |
|---|---:|---|---|
| PTTGC America LLC | **$11,451,981** | FY2017, FY2020, FY2021 | Belmont County, Economic Dev. Grant $1,451,980 + Revitalization Grants $30,000,000 and $20,000,000. Paid $31,451,981, returned $20,000,000 in FY2021. |
| FirstEnergy Generation LLC | **$12,408,019** | FY2017 | Belmont County Revitalization Grant + Phase II — the R.E. Burger plant site, cleared for the cracker |
| Ohio-West Virginia Excavating Co | **$4,739,868** | FY2015–FY2018 | Belmont County Revitalization Grant; FY2017 and FY2018 remitted to **Shadyside**. The project's own `site_dev_review.csv` note: "to prepare land it owned for PTT Global Chemical cracker that was never built." |
| **Total** | **$28,599,868** | | |

**None of the three is a candidate in `failures.csv`.** They are not rejects;
they were never scanned into the set. The reason is the method: a project that
is abandoned before it is built produces no bankruptcy, no closure notice and
no layoff, so neither the Google News distress scan nor the WARN join can see
it. `DATASETS.md`'s list of reasons the count is a floor covers a company that
failed quietly and a subsidiary under a healthy parent. It does not cover
**money paid for a thing that never happened**, which is the single largest
such item in this data.

The $20,000,000 return is already the dominant item in the "money returned"
tile. The other $28.6 million is not anywhere.

**Recommendation, four:** add a sixth category or a named sidebar — "the
project was not built" — and put the Belmont County cluster in it, with the
reversal shown against it. It is the most reportable thing in the file and it
is currently invisible on the page.

A second-order note: Ohio-West Virginia Excavating is **the largest company in
the whole analysis that is counted as a small business** ($4,739,868, 2.6% of
all small-business dollars), its employee band is grade D and the project's own
review file calls it "still a guess", and the money went to a cracker that was
never built. A reporter who pulls one thread will pull that one.

### 2.8 The pandemic exclusion holds up

| Check | Result |
|---|---|
| Notices received 1 Mar – 30 Jun 2020 | 225 of 810 (27.8%) — matches `DATASETS.md` |
| `covid_window` flag vs. that test, over 201 join rows | **0 disagreements** |
| Covid-window rows in `warn_join.csv` | 46, of which 2 carry a verdict and 44 do not |
| Individually verified in `warncheck_b.json` | 10 pandemic-task rows + 8 "funded after layoff" rows |

Two of the ten pandemic candidates were kept, and both calls are right:

- **Mitec Powertrain** (notice 5/4/20) is *in* the count, and the letter gives a
  non-COVID cause in terms — "business being transferred from Mitec's largest
  customer to another supplier, who is moving the production lines to Mexico and
  Canada" — and is signed by a chief restructuring officer. That is the
  pandemic rule working exactly as it should.
- **Pier 1** (notice 6/3/20) is in, correctly, because the company liquidated.

Nothing in the excluded 44 looks to me like a permanent failure wrongly
dropped. The large residual names are tier-C and tier-D false matches (Great
Lakes Services against Great Lakes Cheese; Cooper Tire against Goodyear;
ArcelorMittal Cleveland against ArcelorMittal Tubular Shelby; B&C Research
against four unrelated "Research" payees), not real companies that failed.
The nine un-verified tier-A and tier-B covid rows I checked by reasoning —
Taiho, Deceuninck, Kirchhoff, Matsu, General Aluminum, Profusion, JSW, Belcan,
GLBC — all have the project's own verdict or are plants that still operate.

I did not re-read any 2020 WARN letter myself; this environment has no OCR and
most 2020 notices are scanned images.

### 2.9 Double counting — none found

| Check | Result |
|---|---|
| Duplicate `recipient_id` among the 43 | none |
| Duplicate nine-digit EIN among the 43 | none |
| Duplicate normalised payee name among the 43 | none |
| Any parent contributing two confirmed payees | none |
| Parent money counted twice | no — the block counts payee cash, and `parent_cash_total` is reported separately |

The one real exposure is the opposite: **five** of the 43 sit inside a parent
that was paid more, and reading them as whole-parent losses would overstate by
**$9,015,727**. `DATASETS.md` still says "Four … $8,715,727"; ATW Ohio
($261,110 of American Trailer World's $561,110) is the fifth. The number in
`dist/data.json` is right; the prose is a revision behind.

| Payee | Paid | Parent group paid | Overstatement |
|---|---:|---:|---:|
| Nestlé USA | $3,200,000 | $9,200,000 | $6,000,000 |
| iMFLUX (P&G) | $350,000 | $1,715,727 | $1,365,727 |
| CoverMyMeds (McKesson) | $6,613,235 | $7,413,235 | $800,000 |
| Speedway (Marathon) | $1,700,000 | $2,250,000 | $550,000 |
| **ATW Ohio (American Trailer World)** | $261,110 | $561,110 | $300,000 |

### 2.10 The sample of 12

RNG: Python `random.seed(20261113)`, weighted draw without replacement over the
43 sorted by `recipient_id`, weight `sqrt(paid) + 1`, which tilts toward large
dollars. The draw covers **$79,893,253, 82% of the block.**

| # | Company | Paid | My read |
|---|---|---:|---|
| 1 | FCA US LLC | $4,540,017 | **Holds, and is well handled.** The row itself says 1,094 of the 1,225 in the 2023 notice are supplemental workers and leads the reader to the 2024 notice of 1,134 instead. The plant is open and the row says so. |
| 2 | AmplifyBio LLC | $1,500,000 | **Confirmed independently.** RECAP `gov.uscourts.ohsb.846937`, petition stamped "Case 2:25-bk-52140 Doc 1 Filed 05/16/25". Court and date match. |
| 3 | Petmin USA Inc | $10,000,000 | **Not independently confirmed.** CourtListener answers automated fetches with an empty 202 and the case is not on the RECAP mirror. The row's own quotation of the docket is detailed and internally consistent; I could not reach a second source. |
| 4 | **Ultium Cells** | $50,000,000 | **Overstated as published.** See 2.2. |
| 5 | Columbus Steel Castings | $500,000 | **Confirmed independently.** RECAP `gov.uscourts.deb.163957` docket JSON: case 16-11215, filed 2016-05-16, "Chapter 11 Voluntary Petition", Judge Christopher S. Sontchi. Matches the row and `DATASETS.md`'s judge correction. |
| 6 | Nostrum Laboratories Inc | $250,000 | **Confirmed on court and date.** RECAP `gov.uscourts.njb.1117690`, petition stamped "Case 24-19611-JKS Doc 1 Filed 09/30/24". The petition is image-only, so I could not match the debtor EIN against the payee's 20-5877688. |
| 7 | **CoverMyMeds LLC** | $6,613,235 | **Category overstated.** See 2.3. |
| 8 | Republic Steel Inc | $500,000 | **Holds, and I settled the open wrinkle. One caveat needs rewriting.** See below. |
| 9 | Morgan Truck Body LLC | $1,000,000 | **Confirmed independently.** I fetched the WARN letter: 2 June 2025, "600 E. Chestnut Street, Orrville, Ohio, 44667", permanent, 110 affected. Matches exactly. The site tie to the grant remains circumstantial and the row says so. |
| 10 | **Speedway LLC** | $1,700,000 | **Category not supported.** See 2.3. |
| 11 | P. Graham Dunn Inc | $790,000 | Not independently confirmed — the WARN PDF is a scanned image with no text layer. The state register row (Dalton/Wayne, 92, received 10/1/24) matches the file. |
| 12 | **Hyland Software Inc** | $2,500,001 | **Category overstated.** See 2.3. |

Also verified outside the sample: **80 Acres Urban Agriculture** — RECAP
`gov.uscourts.deb.202392`, Chapter 7 voluntary petition, D. Del., debtor EIN
**83-3394582**, which is the payee's EIN exactly, address 345 High Street,
Hamilton, OH. And **Sarepta** — I fetched the WARN letter, counted the enclosed
Ohio position list and it is **exactly 80 lines**, matching the state register
and the project's figure, with a company-wide total of 493.

**Republic Steel, settled.** I read Grupo Simec's Form 20-F for FY2022 (filed
2023-05-01) and for FY2025 (filed 2026-07-31) direct from EDGAR.

- FY2022 20-F: Lorain "did not produce any steel billets or finished steel bars
  in 2022 as it has been idled since 2016"; production 0 against 900,000 tons of
  installed capacity; $130.7 million impairment in 2015; no coking coal bought
  2018–2022. **The core finding is solid: the mill made no steel when the
  $500,000 was paid in FY2022.**
- But the same filing says Lorain was **"temporarily idled"**, that Simec
  "continues to incur costs to maintain the … facility … in anticipation of
  bringing the entire facility back on line", that it put **$27.1 million of
  construction-in-progress into Lorain over 2020–2022** to prepare a restart,
  and that **"the Lorain 9/10″ Mill … is in the process of being
  recommissioned."** So at the moment the money was paid there was an active
  reactivation programme at the funded site. A press office will reach for that.
- FY2025 20-F resolves the contradiction the project flagged as open: **"In
  August 2023, Republic Steel announced the cessation of its operations,
  **including its steel mill in Canton and Lorain, Ohio** and its rolling mill
  in Lackawanna, New York, all of which remain idled as of the date of this
  report"**; "the Lorain Facility remains idle with no current plans to resume
  activities"; Lorain's net book value is down to $3.1 million; asbestos has been
  removed and buildings demolished. The 2016 idling and the August 2023
  cessation are not in conflict — one is steelmaking, the other is the formal
  end.

**This makes the row's current caveat wrong in one respect.** It says "The 209
jobs and the August 2023 date that appeared on this row are the Canton mill, a
different site Ohio did not fund." The 209-person WARN notice was Canton, but
Simec's own filing says the August 2023 cessation announcement **covered
Lorain**. Rewrite the caveat to separate the notice from the announcement, add
the $27.1 million restart programme, and note that JobsOhio's own 2023 complaint
pleads 55 of the 125 promised jobs were created — so people were hired at Lorain
in the grant period.

---

## 3. The three findings left open by tie-out #2

### 3.1 The mixed-class parent rule — the doc is wrong, and so is the row behind it

There are exactly **two** mixed-class parents, and tie-out #2 is right that only
one discriminates:

| Parent | Payees | Written rule ("non-business") | Output | Largest-payee rule |
|---|---|---|---|---|
| Nationwide Children's Hospital | Research Institute $8,500,000 `hospital`; Andelyn Biosciences $5,000,000 `business` | hospital | hospital | hospital |
| **Tractor Supply Company** | TRACTOR SUPPLY COMPANY $1,500,000 `business`; **NAVARRE FACILITY LLC $850,000 `site_development`** | site_development | **business** | business |

The size rule and the home-state rule do behave as written (Geis and NorthPoint
take the smaller band; Avery Dennison takes OH over CA).

**Which is right: the code, and the doc should change — but the real defect is
one level down.** `NAVARRE FACILITY LLC` has `recipient_class_auto = business`
and was hand-moved to `site_development`. Its own note in `parents.csv` says it
is "the project entity for Tractor Supply Co.'s … distribution center in
Navarre." The project's November 3 site-developer test says: "an operating
company that received money to build, expand or clean up **its own** facility is
that operating company, whatever the payee vehicle is called." Navarre is
Tractor Supply's own distribution centre. **It should be `business`.**
`DATASETS.md` even names this error class — "GBQ Partners … classed as a
developer by a name rule because 'Partners' is in the name, which is the same
error as Tractor Supply" — and then does not fix the Navarre row.

It was never re-checked: **Tractor Supply is not in `site_dev_review.csv`.** Nor
are 21 other parents currently classed `site_development`, carrying **$16,406,867**
between them (largest: 305 Prosperity Parkway LLC $1,600,000, Navarre $850,000,
BH (Ohio) Leasing $800,000, Cooke Building $800,000, SR 29 West Jeff $800,000).
The review file holds 122 rows and 122 parent keys, but 22 of today's
site_development parents are not among them — the keys have drifted.

**What the doc should say:** "Where two payees of one parent disagree, the
analysis takes the smaller size band and Ohio for home state. **A class conflict
is resolved by hand and printed in `TIEOUT.md`; there are two in the data.**"
Reclassify Navarre to `business` and the conflict disappears entirely, so the
rule never has to fire.

### 3.2 The recourse denominator — confirmed, with a correction to the correction

`DATASETS.md`: "Size and home-state shares run on dollars net of the 33 reversed
payments ($1,171,884,901). The conditions shares run on positive payments only
($1,197,924,989)."

Both dollar figures are a fiscal year out of date, and the rule is not the rule
in force. The `recourse` block sums to **$1,346,076,114**, which is
`meta.resolved_cash`, the **net** figure. True positive payments are
**$1,371,358,950**.

**A further defect tie-out #2 did not name: `meta.cash_positive` is mislabelled.**
It is published as $1,346,076,114, identical to `resolved_cash`. The actual sum
of positive rows in `grants_raw.csv` is $1,371,358,950. Anyone re-using
`dist/data.json` and reading `cash_positive` as "positive payments" is off by
**$25,282,836**.

| Grade | `DATASETS.md` | As published (net, $1,346,076,114) | On the rule as written (positive, $1,371,358,950) |
|---|---:|---:|---:|
| agreement seen | 0.65% | **0.61%** | 0.60% |
| standard form | 64.38% | **64.85%** | 63.66% |
| published clawback | 5.63% | **5.63%** | 5.53% |
| loan | 1.40% | **1.40%** | 1.38% |
| none found | 1.27% | **1.32%** | 1.30% |
| service not cash | 0.10% | **0.10%** | 0.09% |
| program unknown | 26.57% | **26.09%** | 25.61% |
| **recourse established** | **70.7%** | **71.09%** | **69.78%** |

**Recommendation, five: change the doc, not the code.** The recourse grade is
assigned per parent and the parent's cash in the table is net. Dividing
parent-net numerators by a positive-payments denominator gives shares that only
sum to 98.1%, because the $26,040,088 of reversals have no grade. One
denominator is correct here. Delete the "Two denominators, stated on purpose"
paragraph, say the recourse shares run on resolved net cash of $1,346,076,114,
and rename `meta.cash_positive` or set it to $1,371,358,950.

### 3.3 Stale prose in `DATASETS.md`

All thirteen of tie-out #2's stale figures still stand, and I reproduced every
"current" value independently from `grants_raw.csv`, `parents.csv` and
`dist/data.json` (business parents 1,469 / $956,764,828; small 18.90%; Ohio
36.22%; Intel $125,415,416 = 13.11%; Intel-out 41.68% and 21.75%; worst case
57.13%; ECONOMIC DEVELOPMENT on 2,014 rows; 83.6% Ohio-address rows). Nine more
are in the failure sections, which tie-out #2 did not read:

| Statement in `DATASETS.md` | Current value |
|---|---|
| "Verdicts: … `Not a failure` (52) … `Unresolved` (1)" | **53 and 0.** Goodlevel Enterprises is now `Not a failure` |
| "84 candidates checked one at a time" | **117 rows** in `failures.csv` |
| "49 of 84 candidates were the company appearing in somebody else's case" | denominator is now 117; the 49 was not re-derived |
| "24 came back `same site`, 4 `partly`, and 3 `different site`" | **37 / 5 / 3, plus 1 `unresolved`** |
| "The four `partly` rows — Nestle, Multi-Color, FirstMerit, AK Steel" | **five** — add ATW Ohio LLC |
| "15 of the 19 match; the other four record why the state has none" | **27 of 32 match; five** record why (add Republic Steel) |
| "Four come back no [`notice_at_funded_site`]: Republic Steel … and the three companies that failed away" | **three come back no**; Republic Steel now has no notice at all; **seven are blank** |
| "Four of the 43 confirmed failures sit inside a parent that was paid more … overstate by $8,715,727" | **five**, **$9,015,727** (add ATW Ohio) |
| "of the 52 sued companies on the grant schedule, 20 employ fewer than 100" | **51** — `data.json` was fixed after tie-out #2, the prose was not |

Two code comments in `scripts/template.html` are also stale and will mislead the
next person to read them: "turn 29 companies and $86.5m into 26 and $96.5m" and
"Ultium Cells alone is **58%** of the failed dollars" (it is 51.5%).

Things I checked and found **correct**: "810 notices"; "46% of all 810 notices
are 2020"; "March to June 2020 alone is 225 of them, 28%"; "the state recorded
notices for one person and for 39 part-time workers" in the Sauder window; "of
the 43 that failed after being paid, none [employs fewer than 100]"; "`Confirmed
failure` (43, $97,009,323 paid)"; "`Failed away from the funded site` (3,
$3,850,000)".

---

## 4. What I would not hand to a reporter without more work

In the order I would fix them.

1. **The "35 of 43 rest on a filing or an official record" sentence.** It is on
   the live page and it is wrong about what it measures. The honest number is 21.
2. **Ultium Cells as 51.5% of the failure dollars.** Publish the total with and
   without it, and put the recall in the caveat.
3. **Speedway's "Mass layoff at the funded site."** The file's own evidence says
   fewer than 35 people.
4. **CoverMyMeds and Hyland as site-level mass layoffs.** $9.1m between them,
   no Ohio job number for either.
5. **Pier 1 Imports in the 43** with a funded-site verdict of `unresolved` and
   two addresses that do not match.
6. **The Technicote and Bitwise WARN misses** — $2.2 million between them,
   found by a name join anyone can re-run. If a reporter finds them before the
   project does, the floor claim loses its credibility.
7. **Republic Steel's caveat**, which says the August 2023 date belongs to
   Canton. Simec's own 20-F says the announcement covered Lorain.

Everything else in the block I would be comfortable handing over. The grant
arithmetic is exact, the WARN register parse is exact, the bankruptcies I could
reach all verify against the petition, the Sarepta Ohio count verifies line by
line against the notice, the funded-site test is a real test that really moved
three companies out, and the rejects are published with reasons. Row for row
this is the most carefully evidenced failure set I would expect to see outside a
newsroom's own files. The exposure is in the labels above the rows, not in the
rows.

---

## 5. What I could not check, and why

1. **Petmin USA's Chapter 7.** CourtListener returns an empty HTTP 202 to every
   automated fetch, and `archive.org`'s RECAP mirror has no item for
   `gov.uscourts.ohnb.*` matching Petmin — the case is a year old and has not
   been uploaded. The $10,000,000 row rests on the project's own reading of the
   docket. It is the second-largest row in the block and the only large one with
   no second source I could reach.
2. **Any 2020 WARN letter, and most scanned ones.** `tesseract`, `ocrmypdf`,
   `pdftoppm` and `pytesseract` are all absent from this environment, so a
   scanned notice is unreadable to me. That covers the Ultium notice, P. Graham
   Dunn, Mitec, Pier 1 and most of 2020. I verified those from the state's own
   register CSV instead, which I re-parsed from the cached files.
3. **Whether the Ultium layoff has in fact been reversed, and by how much.** The
   project cites *Business Journal Daily*, 2026-08-27 without a URL, and this
   session's web-search budget was exhausted before it began, so I can only
   fetch URLs I can name. The recall is the single fact that most changes how
   the headline should read and I could not confirm it independently.
4. **Whether Technicote's 53-person layoff is at the funded operation**, and
   whether Bitwise's $1,500,000 paid for something that survived the collapse.
   Both need the funded-site test the project applies to everything else.
5. **The "22 companies carrying about $23.5m with two or more weak signals."**
   The weak-signal definition is in `TIEOUT.md`, which I was asked not to read,
   and I could not reconstruct it from `DATASETS.md`. I assessed the five named
   companies on their own files instead.
6. **AmplifyBio's and Nostrum's chapter and debtor EIN.** Both petitions are
   image-only; I confirmed court, case number and filing date from the CM/ECF
   header stamp only. 80 Acres' petition has a text layer and its EIN matches
   the payee exactly.
7. **Why `35_warn_join.py` missed Bitwise, Technicote, Worthington and Amcor.**
   The script is on the do-not-read list. The parenthetical hypothesis in 2.5 is
   a hypothesis.
8. **The merits of the 22 site_development parents absent from
   `site_dev_review.csv`.** I established that they are absent and what they
   carry; I did not judge any of them except Navarre.
9. **Whether anything failed that produced neither a news headline nor a WARN
   notice.** The Belmont County cluster in 2.7 is one class of that blind spot
   found by reasoning about the method rather than by a sweep. There is no
   dataset that would let me sweep for the rest.
