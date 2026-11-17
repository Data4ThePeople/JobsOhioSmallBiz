# Status

Project: JobsOhioSmallBiz
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: ohio-income-health (working slug)
Step: 1
Since: 2026-11-17

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
| 3  | Social posts | | |
| 4a | Outreach list | | |
| 4b | Outreach drafts in Gmail | | |

## Completed: jobsohio-grants (published 2026-11-17)

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-11-16 | Three independent tie-outs plus a words tie-out. 40 failures, $95,209,323. |
| 2a | Draft with brackets resolved | 2026-11-16 | `posts/jobsohio-grants/POST.md`. Eric's Purpose section, Claude's method, terminology, limits and FAQ. |
| 2b | Eric's edit, Claude's look-over | 2026-11-17 | Two rounds. Subtitle, journalist warning, Purpose trimmed, Belmont stated once; then the repayment panel pulled, versioning added, both-views guidance written. Every figure tied to `dist/data.json`. |
| 2c | Slice markup | 2026-11-17 | 98 blocks, converts clean. Publication date 2026-11-17T07:30:00-05:00, embed cache-buster `?v=1.0`. |
| 2d | Hero 1680x1080 + alt text | 2026-11-17 | `scripts/48_hero.py`, built from `dist/data.json` so it cannot drift from the tool. Alt text 471 characters. |
| 2e | SEO | 2026-11-17 | `schema_type: dataset`. meta_title 51 chars, description 152, 8 keywords, 6 FAQ entries, 5 CSV downloads in the Dataset graph. |
| 2f | Pushed to Prismic (draft) | 2026-11-17 | Document `avxHXBIAACoALY7g`, 56 slices, Migration Release, not live. Section still to be set by hand. |
| 2g | Mailchimp teaser | 2026-11-17 | `EMAIL.md`. Subject 32 chars, preview 68, hero JPG 152 KB, the 2x2 at the 500 setting as the chart. |
| 3  | Social posts | 2026-11-17 | `SOCIAL.md`. X 275, Bluesky 294, LinkedIn 1,386 with the link in the first comment. Cutoff GIF, 11s, 141 KB. |
| 4a | Outreach list | 2026-11-17 | `OUTREACH.md`, 14 names. Schladen dropped by Eric (already in touch). Confirmed when Eric moved to drafts. |
| 4b | Outreach drafts in Gmail | 2026-11-17 | 13 drafts saved. Eric sent 5 (Evans, Hancock, Hicks, Signal, Stein); WOSU dropped; 7 left in Gmail, all addressed, none sent by Claude. |

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

- 2026-11-16 **Step 1 and Step 2a confirmed.** Three things moved on the last
  day before confirming, all of them from Eric reading the output.
  (1) **Being bought is not failing.** The `Sold or absorbed` category held
  four companies that were acquired or divested and kept operating. Eric set
  the rule: acquired and still running is not a failure, acquired and shut
  down is. All four came out and the category with them
  (`scripts/46_apply_acquired_rule.py`). **The count goes from 44 companies
  and $97,709,323 to 40 and $95,209,323.** None is deleted; each is now
  `Not a failure` with the reason on the row, in the rejected view.
  (2) **Grade D was described wrongly.** "The owner could not be established"
  was false for all 186 rows carrying it: every one names a parent, a home
  state and a size band, and 145 cite a URL. D now says what it is, an owner
  named from web research rather than a filing. The words tie-out had passed
  this sentence because it checked the sweep logic and never checked the
  sentence against the data.
  (3) **The largest reversal has a published reason.** Eric found The
  Intelligencer, March 30, 2022: PTTGC America repaid $20,000,000 after
  failing to make an investment decision on the Belmont County cracker. That
  is 77% of all money the tool reports as returned, and it was an inference
  from a negative tax row until now. The tile says it and links the story.
  The Belmont total stays $28,599,868, which was already net of the reversal.
  Also: the embed drops the "open the full tool" callout, because Prismic
  frames it where a link cannot open, and that text moved into the post. The
  worst-case line under the two-by-two now shows in the embed.
  Open for 2b: Eric's edit. Still outstanding from earlier and not blocking,
  the Sauder Woodworking call, the request for comment, FY2025 XML and
  FY2012-13 PDFs, and the FY2025 distress scan (AmplifyBio) noted above.

- 2026-11-16 **Step 2b confirmed.** What Eric changed on his read:
  (1) **The subtitle was selling the wrong thing.** It counted payments and
  dollars, which is the one part that is not new: the same Schedule I rows
  are on ProPublica's Nonprofit Explorer. It now names the two things that
  are not there, size and home state, and the verified outcomes. The post
  says the same in "Where this comes from", with the link, so a reader can
  check the raw returns and see what was added.
  (2) **A full-width journalist warning above Purpose.** A tool to aid
  research, not one to publish from without checking the individual grant.
  (3) **Purpose before the viz, and shorter.** 6 paragraphs and 560 words
  down to 4 and 300. The failure-data story moved to its own section below
  the frame, and the never-built paragraph with it, since it opened "Note
  another factor" and pointed at the one above it.
  (4) **Belmont is stated once**, in the limits section, with what we know
  and what we do not. It was in two places saying the same thing.
  (5) Two blurbs under the frame merged into one.
  Two tool fixes came out of Eric's questions rather than any tie-out.
  **Sued is not a failure category and the panel did not say so**, which
  invited adding the tiles: 51 sued, 3 of them also in the 40 failures, 48
  not. And **the panel showed three of the four failure categories**, so the
  tiles added to 39 of the 40 the same panel claimed. Both fixed, the
  overlap computed rather than typed.
  Final tie-out of the post against `dist/data.json`: every figure matches.
  Also new: `scripts/47_preview_post.py` renders POST.md to an embargoed
  page at /preview/ for sharing a draft before publication. Not the
  publishing path; Prismic is.

- 2026-11-17 **Step 2b confirmed a second time**, after a round Eric drove by
  reading the tool rather than the draft.
  (1) **Court links take two clicks.** The Franklin County clerk gates every
  deep link behind a disclaimer and discards the case number when it fires, so
  the first click lands on the clerk's home page. Verified directly: a cold
  request returns the disclaimer page with the case number nowhere in it.
  Nothing we can do, so it is said on every case hover, in the Sources key and
  in the post's limits.
  (2) **The "Does Ohio get the money back?" panel is gone**, Eric's call. Its
  headline was 71% of dollars going to a recipient whose agreement allows
  repayment, and two thirds of that 71% is inferred from the standard form
  rather than read from the company's own contract. The figure moved to the
  post where the caveat can travel with it. The per-company column stays.
  (3) **The returned tile's explanation came back** as a note under the
  outcome tiles, with the Intelligencer link, and its numbers are now computed
  in `09_analyze.py` instead of typed into the template.
  (4) **The returned filter had never worked.** It filtered on `p.returned`,
  which was never emitted, so clicking that tile showed an empty table. 17
  parents carry it now, holding $23,263,601 of the $26,040,088 in the tile;
  the gap is payees netting to zero or less and the filter bar says so.
  (5) **Versioning.** `CHANGELOG.md` is the single source. `build.py` reads
  the newest entry into the footer and refuses to build without one, so the
  tool cannot show a version nothing explains. v1.0 is this release.
  (6) **README brought current** for publication: it still said the analysis
  was in progress with no published page.
  (7) **Lead 20 written**, the McKesson and CoverMyMeds split, after Eric
  could not get the detail he wanted out of the tool. $6,613,235 to
  CoverMyMeds and $800,000 to a Fayette County distribution project; the
  Columbus job number does not exist in public and the Tax Incentive Review
  Council filings are where it would be. The shape of that case is now the
  worked example in the post's how-to-use section.
  Final tie-out: every figure stated in the post matches `dist/data.json` or
  `grants_raw.csv`. Both audits pass.

- 2026-11-17 **Steps 2c and 2d confirmed.**
  2c converted clean at 98 blocks: the journalist warning as
  `highlited_page_blurb` defaultFullWidth, the drop cap on the first Purpose
  paragraph rather than the blurb, the embed as `html_embed` fullWidth with
  its 40px spacer, `divider_dots` once above "Where this comes from", and a
  5px spacer under all eight `##` headings. Publication date set to
  2026-11-17T07:30:00-05:00. The embed carries `?v=1.0` so a reader cannot
  get a stale copy of a page that changed all week.
  2d is `scripts/48_hero.py`, which lays out a selection of the tool's cards
  at hero scale instead of screenshotting the page, because a screenshot is
  unreadable at 1680x1080 and cropping one cuts the cards in half. Every
  figure is read from `dist/data.json`, so the hero cannot drift from the
  tool, and the script checks the output is exactly 1680x1080 before
  accepting it.
  **Three rounds of Eric's edits on it, and two of them were the same
  mistake.** The first cut used the page's type sizes and the page's density,
  so nothing read at thumbnail size, and it carried "40 companies failed
  after being paid" and "63 lawsuits", using words the post has not defined
  at the point someone meets the image. The matrix then read "Small" and
  "Large" with nothing defining either, which is fine on the page where the
  control sits above the chart and meaningless on a hero where it does not.
  **A label that depends on a control is not portable**; anything lifted out
  of the tool has to carry its own definition.
  Eric also replaced the two left cards, which had been a count beside a
  dollar share, with two dollar shares at the two cutoffs, 19% under 500 and
  7.8% under 100, so the only thing moving between them is the line for
  small. The matrix stays at 500, the page default.
  Edge padding went up twice, to 84px by 112px, measured on the rendered
  image rather than trusted from the CSS.

- 2026-11-17 **Step 2e confirmed.** The page is published as a schema.org
  `Dataset` rather than an `Article`, which is the one structured-data lever a
  tool page has that a news story does not: Dataset is what Google Dataset
  Search indexes. The Prismic custom type is unchanged and still `blog_post`.
  The optional Dataset fields are filled rather than left blank, because they
  are the ones that get read: temporal coverage FY2014 to FY2025, spatial
  Ohio, four variables measured, four upstream sources, and five CSV
  downloads straight off the repo, every URL fetched and returning 200. Six
  FAQ entries harvest from the Common questions section.
  **Two things found while doing it, both worth remembering.** `section:` in
  front matter reaches Prismic through no field at all, and `articleSection`
  is only emitted by the Article schema builder, so moving to Dataset dropped
  it. Setting `section: Visualization` therefore does nothing on this post and
  **the section has to be set by hand in the Prismic editor.** Making the
  breadcrumb read Home > Visualization > title would be a change to the shared
  schema builder in `~/.claude/tools/prismic/`, affecting every future post,
  so it was deliberately not done mid-publish.

- 2026-11-17 **Step 2f confirmed.** Draft `avxHXBIAACoALY7g` created in the
  Migration Release, type `blog_post`, uid `jobsohio-grants`, 56 slices, hero
  uploaded as `featured_image` and `meta_image`, tags and author empty. Not
  live.
  **The first push was rejected and the lesson is reusable.** Prismic's
  `published_date` is a **Date** field, not a Timestamp, so the 7:30am EST
  publication time could not ride on `date:`. The clock goes in a separate
  `time:` key which the schema builder joins to the date. Prismic now gets
  `2026-11-17`, the JSON-LD gets `2026-11-17T07:30:00-05:00`.
  That split also fixed a bug nothing had caught: with a time already on
  `date:`, the schema builder appended its default clock on top and emitted
  `2026-11-17T07:30:00-05:00T07:00:00-04:00`, invalid structured data on a
  page whose whole SEO case is its structured data.
  **By hand in the Prismic editor, because the importer cannot set either:**
  the section to Visualization, and a check that the embed renders in preview
  since Prismic serves it sandboxed.

- 2026-11-17 **Step 2g confirmed, and Step 2 is closed.** `EMAIL.md` is the
  Mailchimp teaser: subject 32 characters, preview 68 and not a repeat, hero
  exported to JPG at 152 KB.
  Eric rejected the first draft of both body halves and pointed at his own
  post text instead. Part one is now the guiding question and the narrow
  thing the project set out to do, sorting every grant into the 2x2. Part two
  is "The part we did not plan on", condensed, in his words. Together they
  tell one story: we set out to do a small thing and the big thing fell out
  of it, which the first draft did not.
  The chart is the 2x2 itself at the 500-employee setting, rendered by a new
  `scripts/48_hero.py --matrix` from the same `dist/data.json` as the tool,
  so it cannot drift. It replaced the recipients-vs-dollars bars, which
  answered a question the new copy no longer asks.
  **A rule was deliberately relaxed and the decision is recorded in
  `EMAIL.md`.** The process says the email carries no number that is not in
  the post. The chart and the hero alt text carry eight percentages that are
  not in the post's prose. Eric's call: acceptable, because they are
  descriptions of images rather than claims in copy. Every number in the
  email's own prose is in the post.
  **Two overclaims caught in the closing line**, which Eric rewrote twice.
  "Understand how well JobsOhio has performed" contradicted the paragraph two
  sentences above it saying we cannot tell which grants succeeded; it became
  "ask better questions about how JobsOhio has performed". And "we are not
  writing the stories in here" read as a permanent position, which post two
  would break; it became "we are not writing any of the stories on these
  grants today".
  Also fixed during 2g: `scripts/static_charts.py` had its source line
  hard-coded to "FY2014 to FY2024" and had been stamping the wrong range on
  every chart in the repo since FY2025 was added. It reads the range from the
  data now.
  **Still to do by hand in Prismic, neither of which the importer can set:**
  the section to Visualization, and a check that the embed renders in preview
  since Prismic serves it sandboxed.

- 2026-11-17 **Step 3 confirmed.** `SOCIAL.md`: X 275 characters with the link
  counted at 23, Bluesky 294 with the full URL, LinkedIn 1,386 with the link
  held back to the first comment and the hook in the first two lines.
  The animation is the two-by-two as the "small" line moves, 100 to 500 to
  5,000 and back to 500 held five seconds, so the loop ends on the page
  default and the published figures. `scripts/49_social_gif.py`, four frames,
  11 seconds, 141 KB, read from the same `dist/data.json` as the tool, every
  frame a real setting with nothing interpolated. Chosen because it is the one
  thing a still cannot show: small Ohio companies take 7.2%, 16% and 23% of
  the dollars across the three settings, so the tool's own argument is the
  animation.
  Where every number comes from is written at the top of `SOCIAL.md`,
  including that X and Bluesky round to $1.35 billion to fit the limit, a
  figure already on the hero and in `hero_alt`.

- 2026-11-17 **Step 4a confirmed** (recorded at close of 4b; Eric confirmed
  by moving to drafts after dropping Schladen).

- 2026-11-17 **Step 4b confirmed, and the post is complete.** Thirteen drafts
  were saved to Gmail after a relaunch exposed the connector. Eric sent five
  himself (Evans, Hancock, Hicks, Signal, Stein), checked against his Sent
  folder, with no duplicates. WOSU dropped because Eric had already sent the
  post to a WOSU producer. Eric gave addresses for Evans, Hancock, Staver,
  the Dispatch, Good Jobs First and the Business Courier; Gnau and Kasler
  were found and read on their own pages.
  **Wording change:** at Eric's direction, "40 companies failed" became "for
  40 of those companies, we have documented and auditable evidence that they
  underperformed expectations after being paid," because the email gives no
  context for what failure means.
  **Open for Eric before sending:** a web search could not find the stories
  the Dispatch, Good Jobs First and Business Courier drafts open on.
  **Lesson:** the first address search fetched only the outlets' own pages,
  which block automated requests; a plain web search found more. Search first.

- 2026-11-17 **Step 1 opened for the next post** (publishing 2026-11-18).
  Two GIFs. One: Ohio tracts only, median household income against seven
  PLACES measures (diabetes, obesity, smoking, no leisure-time physical
  activity, short sleep, food insecurity, loneliness), cycling one measure
  per frame, a sneak peek of TractEconHealth. No health index, so there is
  nothing to explain. Two: the existing Ohio map (income by tract, JobsOhio
  money by county) cycling between total dollars and dollars per person.

- 2026-11-17 **Step 1 work, ohio-income-health.** Both GIFs built and approved
  by Eric: `income-health-ohio.gif` (7 frames, 3,115 Ohio tracts) and
  `jobsohio-map-total-vs-per-person.gif`. Map income moved to ACS 2020-2024 so
  the post uses one income release; per person now divides by full ACS county
  population. Circles redrawn round after Eric caught ovals.
  **PLACES checks** (scripts 53-55): CDC's own inputs explain 89% to 96% of
  tract differences and income adds at most 0.2 points, so the tight tract
  pattern is the model; income stands in for who lives there. Poverty,
  education and race and ethnicity carry most of it, order varies by measure.
  Counted county deaths move with income about as strongly (premature death
  -0.81, life expectancy +0.79), so the direction holds.
  **Eric's framing for the post:** a teaser asking whether economic
  development and public health should be handled separately given the
  overlap; the deeper look goes in Friday's TractEconHealth post.
  **Tie-outs:** Claude's (`scripts/56_tieout_post2.py`, 0 differences after
  fixing 8 tracts the map had dropped) and the independent one (every number
  matched; food insecurity subtitle corrected). Both in
  `TIEOUT-ohio-income-health.md`.
