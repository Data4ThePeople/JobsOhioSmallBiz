# Independent tie-out #2

> **Read this first: the failure figures below are one revision out of date,
> deliberately.** This tie-out ran while the failure set was 28 companies and
> $86,887,093, and it reproduced both exactly. The WARN join landed afterwards
> and the published figure is now **43 companies and $97,009,323**. Every other
> figure here — the headline size and home-state shares, the year-by-size
> cells, the reversals, the concentration — is current and unaffected, because
> none of it depends on the failure set.
>
> Two things it found were live errors and are now fixed: the sued panel
> counted lawsuits and called them companies, 52 where there are 51, which
> overstated what the sued were paid by $560,770; and `30_audit_summary.py`
> shared that bug and so agreed with the analysis rather than catching it.
> The remaining findings are tracked in `docs/ERIC_TODO.md` section 6.

A second, independent recomputation of the published figures, written from
`DATASETS.md` alone and run against `data/grants_raw.csv`, `data/parents.csv`,
`data/failures.csv` and `data/jobsohio_lawsuits.csv`. The analysis code
(`09_analyze.py`, `30_audit_summary.py`, `31_audit_failures.py`) and the
project's own `TIEOUT.md`, `STATUS.md` and `docs/STORY_LEADS.md` were not read.

**My code:**
`/private/tmp/claude-501/-Users-ericpachman-PycharmProjects-JobsOhioSmallBiz/a1dd38a2-e88f-41d4-b535-c2283e8b5104/scratchpad/tieout2/`
(`recompute.py` first pass, `recompute2.py` final). Date of run: November 13, 2026.

**Headline verdict.** The dollar figures tie. Every published share of dollars
in `dist/data.json` reproduces to the dollar and to seven decimal places from
my own code, including all four cells of the size-by-home-state grid, all
twelve fiscal years, and the worst case. Three things do not tie: the number of
companies JobsOhio has sued (the panel counts suits, not companies, and
double-counts one company), the confidence distribution (no aggregation rule I
tried reproduces it), and one parent count that is off by one. Separately,
`DATASETS.md` states a class-conflict rule the code does not implement, and
carries about a dozen numbers that are stale by one fiscal year.

---

## 1. Every figure checked

Percentages are shown as the page would round them, with the raw share in
brackets where the comparison needs it.

### Totals and coverage

| Figure | Project | Mine | Difference | Verdict |
|---|---:|---:|---:|---|
| Payment rows | 2,415 | 2,415 | 0 | ties |
| Total cash, net of reversals | $1,345,318,862 | $1,345,318,862 | $0 | ties |
| Positive payments only | $1,371,358,950 | $1,371,358,950 | $0 | ties |
| Distinct recipients (payees) | 1,789 | 1,789 | 0 | ties |
| Parents with net above zero | 1,700 | 1,701 | 1 | **differs** (see 2.3) |
| Fiscal years | 2014–2025 (12) | 2014–2025 (12) | 0 | ties |
| Reversal rows | 33 | 33 | 0 | ties |
| Reversal dollars | −$26,040,088 | −$26,040,088 | $0 | ties |
| Parents netting to zero or less | 16 | 16 | 0 | ties |
| Their net | −$757,252 | −$757,252 | $0 | ties |
| Resolved cash (the share denominator) | $1,346,076,114 | $1,346,076,114 | $0 | ties |
| Non-cash assistance | zero every row | zero every row | — | ties |
| Rows with no EIN / placeholder EIN | 2 / 2 | 2 / 2 | 0 | ties |
| Rows with a foreign address | 1 (UK) | 1 (UK) | 0 | ties |

Schedule I cash by fiscal year ties to `DATASETS.md`'s own table in all twelve
years, to the dollar, including the FY2025 PDF parse ($173,433,961 on 377 rows).

### The two headline questions

Denominator: 1,469 parents classed `business`, $956,764,828.

| Figure | Project | Mine | Difference | Verdict |
|---|---:|---:|---:|---|
| Business parents | 1,469 | 1,469 | 0 | ties |
| Business dollars | $956,764,828 | $956,764,828 | $0 | ties |
| Small (under 500) share of parents | 65% (.6466984) | 65% (.6466984) | 0 | ties |
| Small share of dollars | 19% (.1889726) | 19% (.1889726) | 0 | ties |
| Small parent count / dollars | 950 / $180,802,311 | 950 / $180,802,311 | 0 | ties |
| Ohio share of parents | 66% (.6582709) | 66% (.6582709) | 0 | ties |
| Ohio share of dollars | 36% (.3621812) | 36% (.3621812) | 0 | ties |
| Ohio parent count / dollars | 967 / $346,522,263 | 967 / $346,522,263 | 0 | ties |
| Under 100: parents / dollars | 651 / $75,080,295 | 651 / $75,080,295 | 0 | ties |
| Under 5,000: parents / dollars | 1,201 / $333,921,311 | 1,201 / $333,921,311 | 0 | ties |

### Size by home state, business parents

| Cell | Project parents | Mine | Project dollars | Mine | Verdict |
|---|---:|---:|---:|---:|---|
| small, Ohio | 844 (57.45%) | 844 | $153,004,133 (15.99%) | $153,004,133 | ties |
| small, elsewhere | 106 (7.22%) | 106 | $27,798,178 (2.91%) | $27,798,178 | ties |
| large, Ohio | 123 (8.37%) | 123 | $193,518,130 (20.23%) | $193,518,130 | ties |
| large, elsewhere | 396 (26.96%) | 396 | $582,444,387 (60.88%) | $582,444,387 | ties |

### Business dollars by fiscal year, split at 500 employees

All 24 cells tie to the dollar.

| FY | Large (project = mine) | Small (project = mine) |
|---|---:|---:|
| 2014 | $200,000 | $100,000 |
| 2015 | $10,324,218 | $1,181,290 |
| 2016 | $15,824,850 | $6,897,730 |
| 2017 | $29,453,950 | $6,286,137 |
| 2018 | $37,797,747 | $6,931,164 |
| 2019 | $50,241,082 | $10,043,617 |
| 2020 | $128,408,420 | $18,238,193 |
| 2021 | $39,710,905 | $50,788,560 |
| 2022 | $67,115,565 | $16,121,355 |
| 2023 | $224,258,470 | $24,654,035 |
| 2024 | $71,452,853 | $17,110,143 |
| 2025 | $101,174,457 | $22,450,087 |

### Money returned

| Figure | Project | Mine | Verdict |
|---|---:|---:|---|
| Dollars returned | $26,040,088 | $26,040,088 | ties |
| As a share of positive payments | 1.8989% (.018988528) | 1.8989% (.018988528) | ties |

### Concentration

| Figure | Project (page) | Mine | Verdict |
|---|---:|---:|---|
| Largest recipient | Intel, $125,415,416 | Intel, $125,415,416 | ties |
| Intel's share of business dollars | — | 13.11% | see 3.6 |
| Top three | Intel, Honda, Ultium | same | ties |
| Top three dollars / share | — | $227,848,751 / 23.81% | computed |
| Business share of dollars without Intel: small | — | 18.90% → 21.75% | computed |
| Business share of dollars without Intel: Ohio | — | 36.22% → 41.68% | computed |

### All recipients, every class

| Figure | Project | Mine | Verdict |
|---|---:|---:|---|
| Small (under 500) dollars | $338,765,030 (25.167%) | $338,765,030 (25.167%) | ties |
| Ohio dollars | $694,788,935 (51.616%) | $694,788,935 (51.616%) | ties |
| Small parents | 1,096 | 1,097 | +1 (see 2.3) |
| Ohio parents | 1,168 | 1,169 | +1 (see 2.3) |
| Parents with no employee bucket | 64 | 64 | ties (all 64 are Ohio, none is a business) |

### By class

| Class | Project parents / dollars | Mine | Verdict |
|---|---:|---:|---|
| business | 1,469 / $956,764,828 | same | ties |
| government | 43 / $31,877,122 | same | ties |
| hospital | 7 / $100,785,000 | same | ties |
| nonprofit | 38 / $42,885,073 | same | ties |
| site_development | 131 / $109,515,340 | 132 / $109,515,340 | +1 parent (see 2.3) |
| university | 12 / $104,248,751 | same | ties |

### Worst case and confidence

| Figure | Project | Mine | Verdict |
|---|---:|---:|---|
| `worst_case.cash_large_min` | .5712572389837056 | .5712572 | ties |
| `worst_case.parents_small_min` | .4792375765827093 | .4792376 | ties |
| `confidence` A/B/C/D parents | 149 / 1,002 / 366 / 183 | not reproduced | **could not reproduce** |
| `confidence` A/B/C/D dollars | $382.4m / $540.5m / $341.8m / $81.4m | not reproduced | **could not reproduce** |

### The summary panel

| Figure | Project | Mine | Difference | Verdict |
|---|---:|---:|---:|---|
| Confirmed failures: companies | 28 | 28 | 0 | ties |
| Confirmed failures: paid | $86,887,093 | $86,887,093 | $0 | ties |
| Median / mean paid | $500,000 / $3,103,110 | same | 0 | ties |
| Failure bands 100-499 / 500-4999 / 5000+ | 6 / 12 / 10 | same | 0 | ties |
| Failures by category (5 categories) | all five | all five | 0 | ties |
| Failure evidence n / weak / A-or-B | 28 / 4 / 24 | same | 0 | ties |
| Suits filed | 63 | 63 | 0 | ties |
| Sought | $13,548,404 | $13,548,404 | $0 | ties |
| Median sought | $125,000 | $125,000 | $0 | ties |
| **Sued companies (`recipients_matched`)** | **52** | **51** | **1** | **wrong** |
| **Paid to sued companies** | **$12,007,805** | **$11,447,035** | **$560,770** | **wrong** |
| **Median paid to them** | **$140,956** | **$131,911** | **$9,045** | **wrong** |
| **Mean paid to them** | **$230,919** | **$224,452** | **$6,467** | **wrong** |
| **Sued bands `<100` / `100-499` / `500-4999` / `5000+`** | **20 / 14 / 12 / 6** | **20 / 13 / 12 / 6** | **1** | **wrong** |
| **Sued evidence n / weak / A-or-B** | **52 / 19 / 33** | **51 / 19 / 32** | **1** | **wrong** |
| Rejected candidates shown | 71 | 71 | 0 | ties |
| `rows` block | 2,415 / $1,345,318,862 | same | 0 | ties |

### Raw-source claims in `DATASETS.md`

| Claim | Mine | Verdict |
|---|---|---|
| 33 negative rows, all FY2019–FY2022 | 33 rows, FY2019–FY2022 | ties |
| 15 rows where the state contradicts the ZIP | 15, and the same 15 named | ties |
| 13 of them in FY2024, 12 the same city-name error | confirmed, including Honda's Marysville "PA" | ties |
| Non-cash assistance zero in every year | confirmed | ties |
| "84% of rows carry an Ohio address" | 83.6% (2,019 of 2,415) | rounds to 84%; ties |
| "ECONOMIC DEVELOPMENT on 1,637 rows" | 2,014 rows | **stale** (1,637 is the FY2014–2024 count) |

---

## 2. Where I disagree with the published output

### 2.1 The sued panel counts lawsuits and calls them companies

`summary.sued.recipients_matched` is 52. There are **51** distinct recipients
among the 63 suits in `data/jobsohio_lawsuits.csv`. The 52 is the number of
*suit rows that matched a recipient*: Olive AI Inc (EIN 46-4455633) is a
defendant in two suits and is counted twice.

Everything derived from that list carries the same double count:

- `paid_to_them` $12,007,805 includes Olive AI's $560,770 twice. The true
  figure is **$11,447,035**, so the published number is 4.9% too high.
- `median_paid` $140,956 and `mean_paid` $230,919 should be **$131,911** and
  **$224,452**.
- The `100-499` band should be 13, not 14, and the bands should sum to 51.
- `evidence.a_or_b` should be 32 of 51, not 33 of 52.

This is live on the page. `scripts/template.html` line 823 renders
`S.sued.recipients_matched` as "of the 52 sued companies on the grant
schedule", and line 830 prints the inflated mean. `DATASETS.md` itself says
"51 of the 63 defendants tie to a Schedule I recipient," which contradicts the
panel, and then repeats the panel's 52 in the size-contrast section. The
sibling field `lawsuits.suits_matched` is also 52 and is correctly labelled;
only the summary panel mislabels it.

It is worth saying that `30_audit_summary.py` is described as recomputing all
28 published figures and exiting non-zero on a mismatch, and it passes. It
reproduces this defect rather than catching it, which is what happens when the
audit shares the join with the thing it audits.

### 2.2 `DATASETS.md` states a class rule the code does not follow

The November 3 entry says that where two payees of one parent disagree, the
analysis "takes the smaller size band, Ohio for home state, and the
non-`business` class."

There are exactly six parent strings whose payees disagree. The size rule and
the home-state rule hold in all of them (Geis Companies takes 100-499 over
500-4999; NorthPoint takes 100-499; Avery Dennison takes OH over CA). The class
rule does not:

| Parent | Payee classes | Written rule says | Output |
|---|---|---|---|
| Nationwide Children's Hospital | business, hospital | hospital | hospital |
| Tractor Supply Company | business, site_development | site_development | **business** |

Tractor Supply's two payees are TRACTOR SUPPLY COMPANY ($1,500,000, business)
and NAVARRE FACILITY LLC ($850,000, site_development). The output puts the
whole $2,350,000 in the business denominator. The behaviour of both cases is
consistent with taking the class of the **larger payee**, not the non-business
class.

Applying the written rule instead moves 1 parent and $2,350,000 out of the
business denominator and gives: small share of business dollars 18.94% rather
than 18.90%, Ohio share 36.31% rather than 36.22%, business parents 1,468. The
dollars are trivial. The documentation is wrong, and with only one
discriminating case in the data, the rule in the code is not pinned down by the
data at all — one more mixed-class parent could move it either way.

### 2.3 The placeholder-parent fix is incomplete, and costs one parent

The November 3 entry says a recipient whose owner was not found is now its own
parent, because keying on the word "unknown" had merged unrelated project LLCs.
The fix catches the bare strings `unknown` and `unresolved` (13 payees, which
correctly become 13 parents) but not the 25 parenthesised variants:
`unresolved (Lima downtown redevelopment project)`,
`Unknown (unidentified spec-building developer)`,
`Unresolved (Louisville, KY-registered project LLC)` and so on. Those are still
used as merge keys.

One of them actually merges two payees: `unresolved (Lima downtown
redevelopment project)` covers two SPRING & MAIN LLC rows under different EINs
($240,000 and $60,000). Here the merge is almost certainly right, because both
payees carry the same name — but it is right by accident. The mechanism the
November 3 note says was removed is still there, and the next unresolved
developer that picks up a second payee will merge silently.

This is the whole of my 1,701-vs-1,700 difference. No dollar share moves.

### 2.4 The confidence distribution does not reproduce under any rule

`worst_case` ties exactly, and it ties on the rule `DATASETS.md` states: the
weakest confidence grade under a parent. The `confidence` panel, over the same
1,700 parents, does not tie under that rule or any other I tried:

| Aggregation | A | B | C | D |
|---|---:|---:|---:|---:|
| Published | 149 | 1,002 | 366 | 183 |
| Weakest grade in the group | 142 | 995 | 378 | 186 |
| Best grade in the group | 154 | 1,006 | 357 | 184 |
| First payee read | 149 | 1,005 | 363 | 184 |
| Last payee read | 146 | 998 | 371 | 186 |
| Largest payee | 149 | 1,004 | 363 | 185 |

The gaps are small (the published A share is 8.76% against 8.35% on the
weakest-grade rule, and the published A dollars are $382.4m against $367.6m).
But the page shows a confidence mix computed one way beside a worst case
computed another, and the worst case uses the harsher grading. If a reader
takes "28% of dollars are grade A" and the worst-case floor from the same
screen, those two numbers are grading the same companies differently. The rule
behind the panel is not in `DATASETS.md` and I could not infer it.

### 2.5 The recourse table runs on the wrong denominator for what the method says

`DATASETS.md`: "Size and home-state shares run on dollars net of the 33
reversed payments. The conditions shares run on positive payments only
($1,197,924,989), because a reversal has no program to label. Any sentence
using either must say which."

The `recourse` block in `dist/data.json` sums to **$1,346,076,114**, the *net*
resolved figure, not the positive figure. So there is one denominator in the
output, not two, and the recourse shares are computed on net dollars. Nothing
in the published shares is wrong by much, but the rule as written is not the
rule in force, and the share table printed in `DATASETS.md` does not reproduce
either: `agreement seen` is 0.61% against the stated 0.65%, `standard form`
64.85% against 64.38%, `program unknown` 26.09% against 26.57%, `none found`
1.32% against 1.27%, and recourse established is 71.09% against the stated
70.7%.

---

## 3. Method concerns

### 3.1 The parent resolution: a seeded sample of 20

RNG: Python `random.seed(20261113)`, `random.sample` over the 1,789 recipients
sorted by `recipient_id`.

| # | Payee | Paid | Recorded parent / HQ / band | My read |
|---|---|---:|---|---|
| 1 | SILFEX INC | $3,882,369 | Lam Research, CA, 5000+ | **Confirmed.** SEC lists Lam Research at Fremont, CA. |
| 2 | PACCAR INC | $1,300,000 | PACCAR, WA, 5000+ | **Confirmed.** SEC: Bellevue, WA. |
| 3 | 2509 HAYES LLC | $1,040,000 | own name, IL, <100, site_development | Not checked; outside the business denominator either way. |
| 4 | TAIHO CORPORATION OF AMERICA | $635,000 | Taiho Kogyo, Japan, 500-4999 | Not checked (site unreachable). Band is on the 500/5000 line; either way the company is large. |
| 5 | STANDARD TECHNOLOGIES LLC | $600,000 | self, OH, 100-499 | **Questionable reasoning.** The band rests on the Inclusion Grant eligibility rule, but the company was paid $600,000, twelve times the $50,000 Inclusion Grant cap this project relies on. The 119 retained jobs support 100-499 independently, so the answer is probably right and the stated reason is not. |
| 6 | GROB SYSTEMS INC | $500,000 | Grob-Werke, Germany, 5000+ | Not checked (site unreachable). Plausible. |
| 7 | Columbus Steel Castings | $500,000 | self, OH, 500-4999 | Consistent with the Form 5500 count of 783 cited in the file. |
| 8 | Matalco Realty Inc | $500,000 | Giampaolo Group, Canada, 500-4999 | Not externally checked. Reasoning in the file is specific and sourced. |
| 9 | THE JAMES B OSWALD COMPANY | $500,000 | Unison Risk Advisors, OH, 500-4999 | Not externally checked. |
| 10 | BWXT GOVERNMENT GROUP | $475,000 | BWX Technologies, VA, 5000+ | **Confirmed.** SEC: Lynchburg, VA. |
| 11 | RONFELDT MANUFACTURING LLC | $400,000 | self, OH, 100-499 | **Weakest row in the sample.** Grade D, the file says "best guess", and `emp_source` is `https://www.jobsohio.com/sitemap.xml`, which is not evidence of a headcount. $400,000 counted as small on nothing. |
| 12 | CENTURY MOLD COMPANY | $200,000 | Century Mold, NY, 500-4999 | **Confirmed.** The company's own contact page gives headquarters at 25 Vantage Point Drive, Rochester, NY, with Middletown OH as a plant. The method's point — the payee address is not the headquarters — is working here. |
| 13 | SOLE CHOICE INC | $175,000 | self, OH, <100 | Not externally checked; 35 retained jobs supports it. |
| 14 | FIRE MANUFACTURING INNOVATIONS | $100,000 | INNOMOTIVE Solutions Group, Canada, <100 | **Duplicate parent.** See 3.2. The file itself says the band "could be 100-499". Both bands are small, so nothing moves. |
| 15 | NOVO MANUFACTURING LLC | $100,000 | ADENTRA, Canada, 500-4999 | **Confirmed.** ADENTRA's own site lists Novo as one of its six flagship brands. |
| 16 | Sandusky County Economic Development Corp | $90,000 | self, OH, government | **Arguably miscategorised.** A county economic-development *corporation* is normally a nonprofit, not a government. Outside the business denominator under either label, so no published figure moves. |
| 17 | SCHERER INC | $50,000 | self, SD, <100 | Not externally checked; address matches the 990. |
| 18 | DOMINION LIQUID TECHNOLOGIES | $50,000 | self, OH, <100 | 47 retained + 25 created jobs supports it. |
| 19 | WISCO PRODUCTS | $25,000 | self, OH, <100 | Form 5500 shows 14 participants; supports it. |
| 20 | SIGN SOLUTIONS INC | $25,000 | self, OH, <100 | 2 retained jobs; supports it. |

Nothing in the sample is wrong in a way that moves a published number. Two are
weakly evidenced (11, 5), one is arguably in the wrong non-business class (16),
one is half of a duplicate parent (14). Five were confirmed against a primary
source. Nine could not be checked externally this session; see section 5.

### 3.2 Duplicate parents, and merges that should not have happened

I scanned all 1,700 published parents for same-company pairs by distinctive-word
overlap, and separately scanned every recipient EIN for a neighbour one digit
away. Three true duplicates survive de-duplication, all for the documented
reason that the merge requires the band, state and class to agree first:

| Pair | Dollars | Why they did not merge | Effect |
|---|---:|---|---|
| NorthPoint Development / NorthPoint Development LLC | $1,900,000 + $800,000 | bands 100-499 and 500-4999 | **One developer counted as two companies, one small and one large.** Both are `site_development`, so no business share moves, but it is the clearest case of the de-duplication rule producing a contradiction it can see. |
| King's Command Foods LLC / King's Command Foods, LLC | $250,000 + $425,000 | states WI and WA | Two parents for one company; one of the two states is wrong. Neither is Ohio, so no share moves. |
| INNOMOTIVE Solutions Group (parent of AMDOR…) / INNOMOTIVE Solutions Group LLC | $100,000 + $33,197 | bands <100 and 100-499, states Canada and NY | Two parents, both small, both non-Ohio. Parent count only. |

A fourth is a resolution miss rather than a merge failure:

**BH (OHIO) LEASING LLC is in the data twice under two EINs with two different
parents.** EIN 34-1838868 ($800,000, Akron OH) carries parent `unknown`; EIN
82-4447517 ($200,000, Longmont CO) carries parent "Brennan Holdings, LLC". The
research note on the second one says in terms that BH (Ohio) Leasing, LLC is
"an affiliate of Brennan Holdings, LLC". The $800,000 should resolve the same
way. Both rows are `site_development`, so no business figure moves, but the
project's largest single unresolved developer is identified inside its own file.

A fifth is the rule working as designed and worth stating anyway: **ECS Tuning
appears as two parents** — EIN 11-3682720 ($50,000, FY2014, parent "ECS Tuning,
Inc.", 100-499, small) and EIN 47-1395397 ($100,000, parent "Enthusiast Auto
Holdings, LLC", 500-4999, large). That is correct under "ownership at the time
of the grant," since the holding company came later. But it means the count of
1,700 companies contains some companies twice, once per ownership era, and the
page does not say so.

Four more pairs of near-identical EINs do merge correctly and are worth
recording because they show how fragile the EIN key is: Total Quality Logistics
(20-5152100 / 20-5152109), Hynes Industries (34-0971763 / 34-0871763),
Youngstown Business Incubator (34-1751707 / 31-1751707) and Phillips Meat
Processing (61-1493910 / 61-1394910). In each case the two EINs differ by one
digit and the join survives only because the researched parent names normalise
to the same string. Nothing checks EINs for this.

Note for `DATASETS.md`: the reversals section says Hynes Industries' −$50,000
has "no positive row under the same EIN," which is true but reads as
unexplained. It has a positive row of $150,000 under an EIN one digit away, and
the pipeline does net them to $100,000.

### 3.3 The net-of-reversals rule does what it says, with one side effect

16 parents net to zero or below and all 16 are dropped from the recipient count
and from the dollars; 14 of them net exactly zero and two are negative
(Foundation Software −$750,000, INEOS −$7,252), summing to −$757,252. That
matches `meta` exactly, and the handling is consistent: no net-zero parent
appears anywhere in `parents_table`.

The side effect is that the share denominator, $1,346,076,114, is **$757,252
larger than the actual net Schedule I cash of $1,345,318,862**, because
discarding those parents also discards their negative dollars. The page carries
both numbers — `meta.cash_total` and `meta.resolved_cash` — and they differ by
0.06%. Trivial in size, but a reader who adds up the class table will not get
the total.

A second consequence worth a sentence in the post: 16 companies that were in
fact paid on Schedule I are not in the count of 1,700, because they gave all of
it back. Bon-Ton, Pactiv, Tramec Sloan, AJM Packaging, Webster Industries,
Sky Climber and ten others. "1,700 companies" means 1,700 companies that kept
something.

**And the returned-money tile is one company.** PTTGC America's single
−$20,000,000 row in FY2021 is **76.8% of the entire $26,040,088 returned**. The
next largest is −$927,060. The `DATASETS.md` paragraph on reversals names
Bon-Ton at −$200,000, Pactiv, Tramec Sloan and the AJM Packaging clawback, and
never mentions the $20 million. Any sentence that reads $26 million as a
pattern of money coming back is really describing one failed ethane cracker.

### 3.4 What the "small" flag actually rests on

For the 1,548 business recipients, the employee band cites:

| Source | Recipients |
|---|---:|
| Form 5500 | 426 |
| other URL | 384 |
| the Inclusion Grant eligibility rule | 257 |
| SEC filing | 143 |
| Wikipedia | 115 |
| prose, no URL | 113 |
| **a Google News search URL** | **56** |
| LinkedIn | 31 |
| **the JobsOhio sitemap.xml** | **12** |
| **an EDGAR search page** | **10** |
| **blank** | **1** |

The bottom four are not evidence of a headcount at all — they are the record of
a search that was run, not of what it found. That is **79 business recipients
carrying $36,545,463**, of which **48 recipients and $18,441,340 are counted
small**. That is 10.2% of the $180,802,311 small-business figure resting on a
search URL or nothing. The largest are MadTree Brewing ($1,100,000, grade D,
source an EDGAR company-search URL), Ursa Major Technologies ($1,309,730), and
Pointe Ventures ($900,000, grade D).

The Inclusion Grant rule covers 248 recipients and $9,816,315. It is internally
consistent except for six recipients paid more than the $50,000 Inclusion Grant
cap the rule depends on, the largest being Standard Technologies at $600,000.

### 3.5 "At the time of the grant" is a rule the data cannot fully carry

Each parent holds one employee band and one headquarters state, so the phrase
"at the time of the grant" has to mean one time for a company paid across
several years.

- **59 business recipients, $91,223,999**, have a first and last payment five or
  more fiscal years apart and carry a single band.
- **116 business recipients, $23,923,306**, have an `emp_asof` year three or
  more years *after* their last grant; 58 of them, $7,862,073, are counted small.
- `DATASETS.md` says 71 parents carrying $13,562,349 take their home state from
  a Form 5500 address at least three years after the last grant, and says the
  list is reproducible from `parents.csv`. Reading `hq_source` for a Form 5500
  pattern and comparing the cited year to `years`, I get **56 recipients and
  $10,187,349**. Either the stated recipe is not the one used or the figure is
  stale; the exposure is the same order of magnitude either way.

Avery Dennison is the case that shows the limit rather than a bug: it is
recorded CA on its FY2022 payment and OH on its FY2025 payment, because the
company moved, and the conflict rule collapses both to OH. That is the
conservative call, and it is also an admission that one flag per parent cannot
express the rule the method states.

### 3.6 What single items carry a headline

| Drop this one parent | small share of business $ | Ohio share of business $ |
|---|---|---|
| nothing (published) | 18.90% | 36.22% |
| Intel ($125,415,416) | 21.75% (+2.9) | 41.68% (+5.5) |
| Honda ($52,433,335) | 19.99% | 38.32% |
| Ultium Cells ($50,000,000) | 19.94% | 38.22% |
| Sherwin-Williams ($45,432,587) | 19.84% | **33.04% (−3.2)** |

Intel is named in the post and should stay named. Two more belong beside it:

**Sherwin-Williams is 13.1% of all Ohio business dollars on its own.** Drop it
and Ohio's share falls from 36% to 33%. The Ohio finding rests on one Cleveland
company nearly as much as it rests on Intel.

**Ultium Cells is a $50,000,000 home-state judgment call that the post does not
mention.** It is recorded as Michigan. It is a 50/50 joint venture of GM
(Detroit) and LG Energy Solution (Seoul) whose plant and operating base are in
Lordstown/Warren, Ohio, and the project's own research note concedes "no single
ultimate parent, so a skeptic could argue for either owner or a 'Korea' HQ."
**Count Ultium as Ohio and the Ohio share of business dollars goes from 36.2%
to 41.4%** — a 5.2 point swing from one row, almost the size of the Intel
sensitivity the post does name. The reasoning for choosing Michigan over Ohio
or Korea is not stated anywhere a reader can see it.

It also sits oddly beside the treatment of sponsor-owned Ohio companies:
altafiber ($7,470,000, owned by Macquarie of Sydney) and Ensemble Health
Partners ($4,919,985, majority owned by Golden Gate Capital of San Francisco)
are both recorded Ohio. Financial owners do not move the home state; corporate
joint-venture owners do. That may be the right line, but it is not written down.

At the row level: **Intel's single FY2023 payment of $123,181,109 is 12.9% of
all business dollars.** One row out of 2,415.

The small-dollar finding is the robust one. The largest small-business
recipient, Ohio-West Virginia Excavating at $4,739,868, is 2.6% of small
dollars, and the top five together are 9.6%. No single company carries it.
Worth noting all the same that the biggest "small business" in the data is a
grade-D recipient that was moved into the business class by hand during the
November site-developer re-check.

### 3.7 The class boundary, recomputed

`DATASETS.md` calls this the largest exposure in the project and quantifies it
as 101 parents carrying $117,746,967 moved out of `business` by hand, 96 of
them worth $97,096,967 that would have scored small, with the small share going
from 18.1% to 26.2% on the automatic class.

Recomputing from `recipient_class_auto` against `recipient_class`:

| Figure | `DATASETS.md` | Mine |
|---|---:|---:|
| Parents auto=business, hand-moved out | 101 / $117,746,967 | **90 / $92,582,324** |
| …of those that would have scored small | 96 / $97,096,967 | **88 / $88,782,324** |
| Small share of business dollars on the auto class | 18.1% → 26.2% | **18.90% → 25.71%** |
| Ohio share of business dollars on the auto class | not stated | 36.22% → 38.50% |
| Parents hand-moved *into* business | 11 / $11,139,868 | 7 / $2,239,975 |

Direction and order of magnitude hold: the counterfactual is worth about 6.8
points, not 8.1. The paragraph is a pre-FY2025 computation and should be
re-run. The substantive point stands and the post should keep making it.

The single largest item outside the business denominator remains Seefried
Industrial Properties at $17,205,000, flagged in `DATASETS.md`. The next
largest non-business parents are the Cleveland Clinic ($45,000,000), the
University of Cincinnati ($37,500,000) and Ohio State ($32,000,000) — all
plainly correct exclusions.

### 3.8 Numbers in `DATASETS.md` that no longer hold

These are prose figures, not pipeline outputs, and all of them are the
FY2014–2024 values left behind when FY2025 was merged:

| Statement in `DATASETS.md` | Current value |
|---|---|
| "Size and home-state shares run on dollars net of the 33 reversed payments ($1,171,884,901)" | $1,345,318,862 net; $1,346,076,114 as the share denominator |
| "The conditions shares run on positive payments only ($1,197,924,989)" | positive payments are $1,371,358,950 — and the recourse block runs on net, not positive (2.5) |
| "Intel Corporation alone is $124,422,793, 15.2% of business dollars" | $125,415,416, 13.11% |
| "Leave Intel out and Ohio's share goes from 35.8% to 42.2%" | 36.22% to 41.68% |
| "Ohio's share of business dollars fell from 36.8% to 35.8%" | 36.22% |
| "The small share of business dollars moved 18.1% to 19.0%" | 18.90% |
| "The published floor is now 61.3% of dollars to large" | 57.13% |
| "101 parents carrying $117,746,967… 18.1% to 26.2%" | 90 / $92,582,324; 18.90% to 25.71% |
| recourse share table (7 grades) and "70.7% of paid dollars" | 71.09%; four of the seven grades are out by 0.05–0.5 points |
| "71 parents took their home state from a Form 5500 address… $13,562,349" | 56 recipients / $10,187,349 on the recipe as written |
| "'ECONOMIC DEVELOPMENT' (upper case) on 1,637 rows" | 2,014 rows |
| "of the 52 sued companies on the grant schedule" | 51 companies (2.1) |
| "51 of the 63 defendants tie to a Schedule I recipient" | correct, and contradicts the panel |

`DATASETS.md` already warns that recourse shares must be recomputed from
`dist/data.json` rather than copied from prose. The same warning applies to its
own size, home-state and class-boundary figures, and the post should not be
drafted from them.

---

## 4. Things that are right and worth saying plainly

- The grant spine is clean. 2,415 rows, twelve fiscal years, every annual total
  equal to the filer's own Schedule I cash to the dollar, non-cash zero
  throughout, two missing EINs and two placeholders, one foreign address.
- The recipient key reconstructs exactly. Grouping the raw rows by nine-digit
  EIN, falling back to a normalised name where there is none, reproduces all
  1,789 recipients in `parents.csv` and every one of their `total_cash` values,
  with no unmatched rows on either side.
- The headline arithmetic is correct. Both shares, both units, all four grid
  cells, all 24 year-by-size cells and the worst case reproduce exactly from
  independent code.
- The address trap is real and the method avoids it. 83.6% of rows carry an
  Ohio address against 65.8% of parents actually headquartered in Ohio. Century
  Mold in my sample is a clean demonstration: Middletown OH on the 990,
  Rochester NY in fact.
- The failure count and its five categories reproduce exactly, including the
  three companies moved out for failing away from the funded site.
- FY2014 really is too thin to read, and it is worse than "ten companies":
  seven parents were paid at all, four of them operating businesses, $300,000
  between them, and one of those four ($50,000 to ECS Tuning) is the small-era
  half of a company that appears elsewhere as large. The small share of that
  year's business dollars is two grants.

---

## 5. What I could not check, and why

1. **The confidence distribution.** No aggregation rule I tried reproduces the
   published A/B/C/D split. The rule is not in `DATASETS.md` and I did not read
   `09_analyze.py`.
2. **Whether `summary.sued` is the only place the double count appears.** I
   checked the panel and the template string; I did not trace every consumer.
3. **Ultium Cells' registered headquarters.** `ultiumcells.com` returned no
   response from this environment and `businesssearch.ohiosos.gov` returned
   403 to both a descriptive and a browser User-Agent. The sensitivity is
   computed; the fact is not independently confirmed.
4. **Nine of the twenty sampled recipients.** Taiho Kogyo and Grob-Werke
   (company sites unreachable; neither is an SEC registrant), Matalco /
   Giampaolo Group, Unison Risk Advisors, Sole Choice, Scherer, Dominion Liquid
   Technologies, 2509 Hayes LLC and Ronfeldt Manufacturing. This session's web
   search budget (200 calls) was already exhausted before my first query, so I
   could only fetch URLs I could name in advance. Five of the twenty were
   confirmed against SEC submissions or the company's own site; the rest rest
   on the project's own cited sources.
5. **Employee counts generally.** The analysis uses bands, and verifying a band
   needs a headcount at a date. I confirmed none independently except through
   SEC records already cited in the file. The 79 recipients with no headcount
   source are flagged above but not researched.
6. **Whether the 90 hand-reclassified parents are correctly classified.** I
   recomputed the counterfactual's size, not the merits of any individual call.
   `data/site_dev_review.csv` records the reasoning; I did not audit it.
7. **The FY2025 PDF parse.** I verified that its row count and total match what
   `DATASETS.md` states and that it foots with the other eleven years, but I
   did not re-parse
   `b200_jobsohio_990_fed_pdc_ty24.pdf` independently.
8. **Anything resting on the monthly metrics files, program terms, WARN notices
   or court dockets.** Out of scope for this tie-out, which was asked to check
   the grant arithmetic and the parent resolution.
9. **`DATASETS.md`'s claim that all eleven XML filings are original returns.**
   The note says "to confirm: `AmendedReturnInd` absent" and the raw XML is not
   in the repository.

---

## 6. What I would fix before publishing

1. Change `summary.sued.recipients_matched` to count distinct recipients, and
   recompute `paid_to_them`, `median_paid`, `mean_paid`, `bands` and `evidence`
   off the deduplicated list. The page currently says 52 companies and
   $12,007,805 where the answer is 51 and $11,447,035.
2. Decide what the class-conflict rule is, make `DATASETS.md` and the code
   agree, and say which way Tractor Supply's $2,350,000 falls.
3. Extend the placeholder test to the 25 parenthesised "unknown" and
   "unresolved" parent strings, and resolve BH (Ohio) Leasing's $800,000 to
   Brennan Holdings, which the project's own note already identifies.
4. Name Sherwin-Williams and Ultium Cells beside Intel. One company is 13% of
   the Ohio dollars and another is a $50 million home-state judgment the reader
   cannot see.
5. Say in the reversals paragraph that $20,000,000 of the $26,040,088 returned
   is one PTTGC row.
6. Re-run every prose figure in `DATASETS.md` against `dist/data.json`. Roughly
   a dozen are a fiscal year out of date.
7. Make the confidence panel and the worst case use the same grading, or say on
   the page that they do not.
