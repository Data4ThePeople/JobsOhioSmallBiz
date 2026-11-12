# JobsOhio Grants by Business Size and Home State

An analysis of every grant JobsOhio reported paying on its IRS Form 990, Schedule I, from fiscal year 2014 to fiscal year 2024. It asks what share of recipients and what share of paid dollars went to small businesses (ultimate parent under 500 employees at the time of the grant) and to businesses whose ultimate parent was headquartered in Ohio.

It also asks two follow-on questions: what conditions JobsOhio publishes for each grant, including whether the money can be taken back if the jobs never arrive; and which recipients went bankrupt, closed the funded site or cut it back after being paid.

The analysis is still in progress. Results are not yet published.

## Live link

No published page or post yet. The built interactive page is in `dist/index.html`.

## What's here

- `DATASETS.md`: one section per data source, with coverage, quirks and known traps.
- `TIEOUT.md`: every headline number, recomputed from the data files by `scripts/09_analyze.py`.
- `scripts/`: the numbered pipeline, from download to analysis, plus the page and chart builders.
  - `names.py`: company-name normalization and conservative name matching, shared by the scripts.
  - `template.html`: the page template that `build.py` fills with data.
- `data/`
  - `raw/990/`: JobsOhio's Form 990 e-file XMLs, one per fiscal year.
  - `raw/metrics/`: JobsOhio's monthly executed grants and loans reports (PDF).
  - `grants_raw.csv`: one row per Schedule I line, as filed.
  - `reconcile_990.csv`: Schedule I cash totals compared with Part IX line 1, by year.
  - `commitments.csv`, `commitments_norm.csv`: parsed monthly reports; `commitments_anomalies.csv` lists rows set aside for hand review.
  - `recipients.csv`: one row per distinct Schedule I recipient, with totals across years.
  - `parents.csv`: the crosswalk from each recipient to its ultimate parent, size bucket, home state, source and confidence grade.
  - `edgar_ein_matches.csv`, `f5500_participants.csv`: SEC and Department of Labor signals used in research.
  - `verify_*`: the independent re-check of a random sample of classifications.
  - `research/`: inputs and outputs of the parent-resolution research batches.
  - `air_service_routes.csv`, `breeze_jobsohio_routes.csv`: airline route checks against DOT flight data.
  - `program_terms.json`: the published guidelines for all 12 JobsOhio programs, read for how the grant is paid, what the company must do, what it must report and what happens if it falls short, each with the exact quote it rests on.
  - `grant_conditions.csv`: every Schedule I payment labelled with the conditions published for the program that paid it.
  - `distress_candidates.csv`: every recipient scanned for failure headlines, with the headlines found.
  - `failures.csv`: the verified outcome for each candidate, including the rejects and why each was rejected.
  - `research3/`: the per-candidate verification files behind `failures.csv`, including `sitecheck.json`, which records for each confirmed failure whether the operation that failed was the operation the grant paid for.
  - `warn/`: Ohio's own register of mandatory layoff and closure notices, 810 of them from 2020 to 2026, with each year's page and CSV cached so the parse can be re-checked.
  - `failure_warn.csv`: each Ohio closure or mass layoff tied to the employer's own notice to the state, or the reason the state has none.
- `docs/`: the written research method, the verification write-up and research notes.
- `dist/`: the built page (`index.html`), an embeddable version (`embed.html`) and the data it reads (`data.json`).
- `posts/images/`: static charts for the post.
- `assets/`: Data 4 The People logos used on the page.

## Data sources

| Agency | Dataset | Use |
|---|---|---|
| Internal Revenue Service (via GivingTuesday 990 Data Lake and ProPublica Nonprofit Explorer) | JobsOhio Form 990, Schedule I, Part II (EIN 45-2798687) | Every grant paid, by recipient and year. The spine of the project. |
| JobsOhio | Monthly Executed Grants and Loans Reports | Program type, county, industry and jobs for each executed agreement (commitments, not payments). |
| U.S. Securities and Exchange Commission | EDGAR company submissions, Form 10-K and Exhibit 21 | EIN matches, employee counts, headquarters and subsidiaries for public companies. |
| U.S. Department of Labor, EBSA | Form 5500 and 5500-SF datasets, plan years 2015, 2019 and 2023 | Plan participant counts as a size signal. |
| Ohio Secretary of State | Business search | Entity type and formation date, to spot project LLCs. |
| Good Jobs First | Subsidy Tracker | Spot checks of parent companies. |
| U.S. Department of Transportation, Bureau of Transportation Statistics | T-100 Domestic Segment, U.S. carriers | Checks on routes tied to air service grants. |
| JobsOhio | Published program guidelines (12 programs) | What each program says about payment, performance, reporting and repayment. |
| Google | News RSS search | Used only as an index to find candidate failures. Findings rest on the court docket, SEC filing or local story it points to, never on the headline. |
| Federal and state courts; SEC | Bankruptcy dockets (via CourtListener) and 8-K filings | Confirming or rejecting each candidate failure. |

Full details, including IRS object IDs for each filing, are in `DATASETS.md`.

## How to rebuild

Requirements: Python 3 with `pdfplumber`, `pypdf` and `matplotlib` (`pip install -r requirements.txt`). No API keys are needed. SEC requests need a User-Agent with a contact address.

Run from the repo root, in order:

```
python scripts/01_fetch_990.py        # download Form 990 XMLs (FY2014 to FY2024 are already in data/raw/990/)
python scripts/02_parse_sched_i.py    # Schedule I to data/grants_raw.csv, plus reconcile_990.csv
python scripts/03_parse_metrics.py    # monthly report PDFs in data/raw/metrics/ to data/commitments.csv
python scripts/04_normalize.py        # data/recipients.csv and metrics matching
python scripts/06_edgar_ein.py        # needs EDGAR submissions.zip in data/raw/edgar/ (not committed)
python scripts/07_f5500.py            # needs DOL Form 5500 zips in data/raw/f5500/ (not committed)
python scripts/05_seed_parents.py     # refresh data/parents.csv; hand-filled columns are kept
python scripts/09_analyze.py          # every published number, dist/data.json and TIEOUT.md
python scripts/build.py               # dist/index.html and dist/embed.html
python scripts/static_charts.py       # PNG charts in posts/images/
```

The conditions and failures work runs separately and its results are saved in the repo:

```
python scripts/19_grant_conditions.py # label every payment from data/program_terms.json
python scripts/17_distress_scan.py    # scan recipients for failure headlines (slow; hits Google News)
python scripts/21_failures.py         # consolidate data/research3/*.json into data/failures.csv
python scripts/32_fetch_warn.py       # download Ohio's WARN register into data/warn/
python scripts/33_match_warn.py --write   # tie each closure and layoff to the state's notice
python scripts/34_apply_sitecheck.py  # apply the funded-site verdicts to data/failures.csv
```

Two audits run before every publish and exit non-zero on any mismatch:

```
python scripts/30_audit_summary.py          # recompute all 28 summary figures from source
python scripts/31_audit_failures.py --fetch # check every failure claim, and that each source resolves
```

`09_analyze.py` picks up `grant_conditions.csv` and `failures.csv` if they are present and adds a `Conditions` and an `After the grant` column to the page. Both are optional: the analysis runs without them.

The parent research and checks (`08_research.py`, `10_verify_sample.py`, `11_auto_classify.py`, `13_apply_subsidiary.py`) feed `data/parents.csv`. Their results are already saved in the repo, so a rebuild does not need to rerun them. `15_fetch_t100.py` downloads the DOT flight data used for the air service checks into `data/raw/t100/` (not committed).

## Method notes

- Dollars are cash paid as reported on Schedule I, not commitments and not accrued grant expense. JobsOhio states that Schedule I is on a cash basis, so it does not tie to Part IX line 1. Grants of $5,000 or less are not listed on the form.
- Each recipient is resolved to its ultimate parent, and the count of recipients is a count of unique parents, not rows. Size is the parent's worldwide employee count at the time of the grant. Home state is the parent's headquarters, not the recipient's mailing address or state of incorporation.
- Totals are net of 33 reversed payments. A parent is counted as a recipient only if its net payment is above zero.
- The headline uses for-profit businesses as the denominator. Results for all recipients, and at cutoffs of 100 and 5000 employees, are also in `TIEOUT.md`.
- A seeded random sample of classifications was re-checked by an independent second pass. The method and results are in `docs/VERIFICATION.md`.
- The conditions columns describe what JobsOhio **publishes**, not what is in force. Individual grant agreements are not public, and at least one case shows terms exist that the guidelines do not print. Only 2 of 12 programs publish a clawback, covering 6.8% of paid dollars.
- The failure count is a floor, not a count. It is found from news coverage, so a failure without coverage is missing; it treats the payee as the company, so a parent's filing that left the Ohio site running is excluded. Of 102 candidates checked one at a time, 52 were thrown out because the company was named in somebody else's case and 17 were a different company sharing a name. Every reject is kept in `data/failures.csv` with its reason, and the page shows them.
- A failure counts only if the operation that failed is the operation the grant paid for. Every confirmed failure was re-checked on that question, and three companies came out of the count: they closed an Ohio site, but not one the money went to. They are still shown on the page, under their own heading, with the site that took the money and the site that failed.
- Where Ohio holds the employer's own layoff notice, that is the source rather than the news story. 15 of the 19 Ohio closures and mass layoffs have one. The four that do not each record why, and one of those four, Sauder Woodworking, is an unexplained gap rather than a threshold: its 150-job figure rests on press reporting alone.

Data 4 The People
