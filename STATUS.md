# Status

Project: JobsOhioSmallBiz
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: none yet
Step: 1
Since: 2026-09-18

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | | |
| 2a | Draft with brackets resolved | | |
| 2b | Eric's edit, Claude's look-over | | |
| 2c | Slice markup | | |
| 2d | Hero 1680x1080 + alt text | | |
| 2e | SEO | | |
| 2f | Pushed to Prismic (draft) | | |
| 2g | Mailchimp teaser | | |

## Stale

None.

## Reminders for writing (raise at Step 2a)

- Story leads are in `docs/STORY_LEADS.md`. Eric asked to be reminded:
  **Petmin USA** ($10M paid in FY2020-21 for an Ashtabula pig iron plant that
  was never built; Chapter 7 filed November 3, 2025). Open question to answer
  before publishing: does Ohio get the money back?
- Also there: $26.0M in reversed grants; foreign-owned units inside the
  small-business Inclusion Grant; the Breeze and other air-service routes
  checked against DOT flight data; Intel's $124.4M with the plant now due
  2031; JPMorgan's 75 promised jobs at Otterbein's The Point.
- Eric asked (Sept 22, 2026) to be reminded to write about **Supply Line
  International Medical**: $1,612,500 on the FY2020 grants schedule to a
  Michigan distributor of syringes, gloves and COVID tests, with no JobsOhio
  project record, while JobsOhio was buying PPE. Lead 8 in
  `docs/STORY_LEADS.md`. No board connection found; JobsOhio disclosed no
  insider transactions that year (no Schedule L). Open: ask JobsOhio grant or
  purchase; check the state checkbook; run a board-conflict check across all
  years.
- New (Nov 3, 2026), leads 9 and 10 in `docs/STORY_LEADS.md`:
  **Only 2 of 12 JobsOhio programs publish a clawback**, and they are the two
  smallest kinds of award, 6.8% of the dollars. The Economic Development Grant,
  the largest program and the one that paid Intel $123.2M, runs on a two-page
  document dated December 10, 2015 with no repayment language. The air service
  program publishes no reimbursement requirement either, which corrects what
  we told Eric earlier about the airline grants being pay-as-you-fly.
  **29 recipients failed after being paid, $86.5M**, including Petmin
  (Chapter 7 confirmed off the docket), Ultium Cells ($50M, 1,300 jobs cut),
  and Olive AI, where JobsOhio actually sued to get the money back. Pull the
  Olive AI suit in Ohio state court; it may be the only public place a JobsOhio
  grant agreement's terms appear.

- Eric asked (Nov 12, 2026) to be reminded to write up **Union Metal
  Industries** as the case that shows the whole recovery problem in one
  docket. JobsOhio paid $1,250,000 across three grants under one agreement
  (Revitalization, Workforce Training and Economic Development, contract
  SFPN_2018_455827). The company committed to 250 new jobs and $13,000,000 of
  payroll in Canton; its own 2023 annual report said 137 jobs and $7,400,784.
  JobsOhio sent two demand letters, February 14 and July 9 2025, each for
  **$200,000**. When they went unpaid it sued on October 23, 2025 for the
  **entire $1,250,000**, pleading that not paying the $200,000 was itself a
  breach. On **January 6, 2026** it filed one sentence: "Now comes Plaintiff
  JobsOhio and hereby dismisses this action with prejudice." No reason, no
  figure, no settlement filed, no reversal on any 990. With prejudice means it
  gave the claim up for good. We cannot tell whether that was a settlement, a
  payment, or a decision that the case would lose. Case 25CV009178, Franklin
  County; lead 11 in `docs/STORY_LEADS.md`.
  One point in its favour as an example: JobsOhio attached the whole grant
  agreement here, both the 2019 original and the 2020 amendment, so 21 of the
  complaint's 27 pages are the contract. That is the direct contrast with Olive
  AI, where it refused to attach the agreement as trade secret.

- New (Nov 12, 2026), lead 12: **JobsOhio sued 2 of the 29 companies that
  failed after being paid.** $85.5M of the $86.5M went to companies it never
  sued, including every one of the seven mass layoffs and all seven
  bankruptcies. Meanwhile the 63 companies it did sue are mostly small: median
  $125,000 sought, smallest $16,724, and three were sued over a missing annual
  report alone. The agreement has a waiver clause, "Market Conditions and Other
  Factors," which JobsOhio's own complaints quote around. Carry all three
  possible explanations and claim none.

- **Gap to close before publishing (found Nov 12, 2026).** The distress scan
  that produced the confirmed failures ran over the FY2014-2024 recipients
  only. The 274 recipients that first appear in FY2025 have never been scanned,
  and at least one of them failed: **AmplifyBio LLC took $1,500,000 in FY2025
  and closed its doors inside the same fiscal year.** JobsOhio's own September
  2024 project record has it retaining 155 jobs and committing to 263 more on a
  $132.75M project; Fierce Biotech reported Ohio layoffs on 2024-12-06, Fierce
  Pharma reported the closure on 2025-04-07, a former employee sued over the
  layoffs in May 2025, and Battelle reabsorbed the company through an
  assignment for the benefit of creditors in October 2025. Run
  `scripts/17_distress_scan.py` over the FY2025 recipients once they are
  merged, then verify any candidates the same way the other 84 were.

## Log

- 2026-09-18 Step 1 opened. Topic: every grant JobsOhio has disclosed on
  Form 990 Schedule I (FY2012 to FY2025), classified by recipient size
  (parent under 500 employees at time of grant = small) and by home state
  (ultimate parent headquartered in Ohio = homegrown). Two headline
  assessments, share of recipients and share of paid dollars, small vs.
  large, plus a searchable table. Decisions agreed: paid dollars (990) as
  the headline, commitments left out; 500-employee line with a
  reader-movable cutoff; headquarters not incorporation; for-profit
  businesses as the headline denominator with an all-recipients toggle;
  unique recipients as the count; Eric reviews the parents carrying 90% of
  dollars.
- 2026-09-19 Step 1 in progress. Schedule I FY2014 to FY2024 parsed (2,038
  rows, $1.17B, 1,515 recipients). 1,228 recipients classified (research
  agents plus rules R1 to R4); the 287 left carry 1.7% of dollars, none over
  $137,000. Interim, businesses only, small = under 500 employees: small
  firms are 50.5% of parents and 18.4% of dollars; large firms 27.8% of
  parents and 79.3% of dollars; worst case at least 61% of dollars to large.
  Open: research on the last 287 (agents stalled; resume in a fresh
  session with web search), 150-row re-check sample, Eric's review of
  data/review_for_eric.csv, FY2025 XML and FY2012-13 PDFs from Eric.
- 2026-09-19 Research queue complete: all 1,515 recipients classified.
  Independent re-check of 150 random rows: 6.7% of size calls wrong, all
  large read as small, concentrated in rules R1/R2 (11.9%). Ownership check
  on all 427 remaining R1/R2 rows moved 27 to a larger parent and 16 to a
  new home state. Businesses, 500 cutoff: small 61.1% of recipients, 18.4%
  of dollars; worst case at least 62.1% of dollars to large. 33 reversed
  grants (-$26.0M) found and documented. Open: Eric's review of
  data/review_for_eric.csv; FY2025 XML and FY2012-13 PDFs; optional
  search-enabled pass on the 146 grade-D parents.
- 2026-11-03 Three asks closed. (1) The review list was cleared without Eric:
  all 215 companies answered, with a confidence on each and a range where the
  employee count is uncertain. (2) Grant conditions: the published guidelines
  for all 12 programs transcribed to `data/program_terms.json` and joined to
  every payment in `data/grant_conditions.csv`. Conditional 6.8% of dollars,
  Partly conditional 68.3%, Program unknown 22.5%, nothing published 2.4%.
  (3) Failures: 1,485 recipients scanned for distress headlines, 84 candidates
  verified one at a time against dockets, SEC filings and local news, then a
  second pass joining Ohio's whole WARN register against every recipient:
  **43 confirmed ($97,009,323)** in `data/failures.csv` with every reject and
  its reason kept. Two new story leads written. Open: pull the JobsOhio v. Olive AI
  suit; settle Columbus Steel Castings' payment timing (its court and docket are
  now resolved off the petition itself); Goodlevel
  Enterprises unresolved; rebuild `dist/` and regenerate
  `data/review_cleared.csv`; independent tie-out before closing Step 1; FY2025
  XML and FY2012-13 PDFs still owed from Eric.

- 2026-11-12 Failure findings audited end to end, which is where the scrutiny
  will land. `scripts/31_audit_failures.py` checks every claim against the file
  it was verified against: join key, money tied to `parents.csv`, event against
  category, funded-site verdict, partial splits, the state's own notice, a
  resolving source URL, and a stated reason on every reject. It was tested by
  breaking four things deliberately and confirming it caught all four. What it
  found, and what changed:
  (1) **The headline moved: 28 companies and $86,887,093, not 31 and
  $90,737,093.** A standing check asked of every confirmed failure whether the
  operation that failed was the operation the grant paid for. Dana, New
  Horizons Baking and FedEx Supply Chain came back no, each verified against
  our own payment and commitment records. They keep a row and a view of their
  own rather than being deleted.
  (2) Ohio's whole WARN register pulled, 810 notices 2020-2026. 15 of the 19
  Ohio closures and mass layoffs now cite the employer's own filing. Ultium's
  notice reads 484 permanent and 850 temporary, not 1,334. Sauder Woodworking
  has no notice at all where one would be expected, so its 150 figure rests on
  press reporting alone; worth a call before publishing.
  (3) Republic Steel's funded site is Lorain and is shuttered, but the 209 jobs
  and the August 2023 date on the row are Canton, an unfunded site. Caveated.
  (4) Five rows had an `event` that contradicted their `category`; Columbus
  Steel Castings' judge was wrong (Sontchi, not Silverstein); Zulily's plant
  was Lockbourne, not Obetz. All corrected off primary records.
  (5) **A page bug worth noting: the rejected-candidates view had never
  rendered its rows.** Two `return`s inside the filter bar were exiting
  `renderTable` entirely. The filter bar is now its own function and both views
  were screenshotted to confirm they work.
  Open: the full WARN-to-recipient join, which would turn the failure count
  from a floor into something close to a count (lead 14); Sauder; the Olive AI
  state suit; Goodlevel Enterprises; FY2025 XML and FY2012-13 PDFs from Eric.

- 2026-11-13 The WARN join, and what it found. Ohio's whole register, 810
  notices, joined against all 1,789 recipients (`scripts/35_warn_join.py`),
  verified in `data/research3/warncheck_*.json`, merged by
  `scripts/37_merge_warncheck.py`. **The count goes from 28 companies and
  $86,887,093 to 43 and $97,009,323.** A third of the confirmed failures had
  no news coverage our scan could see, which is the measure of how much of a
  floor a news-based count was. The largest new one is Pixelle's Chillicothe
  mill, 780 jobs, found only once the join scored on where JobsOhio's own
  records put the project instead of where the cheque was posted; Pixelle's
  went to Pennsylvania.
  Rejections mattered as much: ProMedica, ADS Alliance Data and
  Sherwin-Williams all pass a county test and fail a street test, and 8 of 10
  pandemic-window candidates drop because the notice letters say "temporary"
  in terms.
  Two live errors found and fixed. The sued panel counted lawsuits and called
  them companies, so it said 52 where there are 51 and overstated what they
  were paid by $560,770; Olive AI is a defendant twice. And the page said 11
  suits name companies absent from Schedule I when the answer is 9.
  `30_audit_summary.py` shared the first bug and so agreed with it rather than
  catching it. The independent tie-out found it:
  `docs/TIEOUT_INDEPENDENT_2.md`, which otherwise reproduces every headline
  share to seven decimals.
  Open, tracked in the private to-do outside this repo: the Sauder call,
  the request for comment,
  and three judgment calls, the largest being whether Ultium Cells counts as
  Ohio, which alone moves the home-state share from 36.2% to 41.4%.
