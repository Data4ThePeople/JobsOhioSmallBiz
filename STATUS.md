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
  verified one at a time against dockets, SEC filings and local news, 29
  confirmed ($86,537,093) in `data/failures.csv` with every reject and its
  reason kept. Two new story leads written. Open: pull the JobsOhio v. Olive AI
  suit; settle Columbus Steel Castings' payment timing and court; Goodlevel
  Enterprises unresolved; rebuild `dist/` and regenerate
  `data/review_cleared.csv`; independent tie-out before closing Step 1; FY2025
  XML and FY2012-13 PDFs still owed from Eric.
