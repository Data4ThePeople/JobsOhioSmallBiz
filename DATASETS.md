# Datasets

One section per dataset, written before any analysis, updated whenever we learn
something new. The point is to know the traps before they show up in a chart.

Project question: of the grants JobsOhio has disclosed since it began, what
share of recipients and what share of paid dollars went to small businesses
(ultimate parent under 500 employees at the time of the grant), and to
businesses whose ultimate parent was headquartered in Ohio.

---

## JobsOhio Form 990, Schedule I, Part II (IRS; filed by JobsOhio, EIN 45-2798687)

**What it is.** The IRS return of a 501(c)(4). Schedule I Part II lists every
grant of more than $5,000 to a domestic organization or government during the
fiscal year: recipient name, street address, city, state, ZIP, recipient EIN,
IRC section (if the recipient is exempt), cash amount, non-cash amount, and a
purpose line. One row per recipient per year. This is the spine of the project.

**Where it comes from.** IRS e-file XML, downloaded anonymously from the
GivingTuesday 990 Data Lake:
`https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml`.
Object IDs and years:

| FY end | Object ID | Source |
|---|---|---|
| 2014-06-30 | 201413189349308116 | data lake |
| 2015-06-30 | 201630469349301988 | data lake |
| 2016-06-30 | 201700099349300615 | data lake |
| 2017-06-30 | 201811169349300106 | data lake |
| 2018-06-30 | 201900849349300615 | data lake |
| 2019-06-30 | 202020599349300902 | data lake |
| 2020-06-30 | 202140579349301709 | data lake |
| 2021-06-30 | 202231369349300238 | data lake |
| 2022-06-30 | 202321359349316252 | data lake |
| 2023-06-30 | 202421369349306592 | data lake |
| 2024-06-30 | 202531359349316618 | data lake |
| 2025-06-30 | 202641359349309474 | not in the lake yet; ProPublica browser download, or JobsOhio's PDF `jobsohio.com/files/tax-returns/b200_jobsohio_990_fed_pdc_ty24.pdf` |
| 2013-06-30 | none (PDF only) | ProPublica PDF; FY2013 total expenses $7.2M |
| 2012-06-30 | none (PDF only) | ProPublica PDF; first partial year |

ProPublica's `download-xml` endpoint returns a security-check page to scripts;
it works in a browser. JobsOhio also posts its own 990 PDFs at
`jobsohio.com/files/tax-returns/` and `jobsohio.com/files/reports/`.

**Version and vintage.** Each filing is a single vintage; the IRS does not
revise a 990 unless the filer amends it. All 11 XML filings are original
returns (to confirm: `AmendedReturnInd` absent). Schema versions run 2013v3.1
through 2023v6.0. The element names used here (`RecipientTable`,
`RecipientBusinessName/BusinessNameLine1Txt`, `RecipientEIN`, `CashGrantAmt`,
`NonCashAssistanceAmt`, `IRCSectionDesc`, `PurposeOfGrantTxt`,
`USAddress/CityNm`, `USAddress/StateAbbreviationCd`) are stable from the
2014v6.0 schema on. The FY2014 filing (schema 2013v3.1) uses the older names
`BusinessNameLine1`, `AddressLine1`, `City`, `State` and `ZIPCode`; the first
parse missed them, leaving the eight FY2014 rows without a name or address
(dollars and EINs were read correctly). Fixed September 19, 2026: the parser
accepts both names and stops if any row has no recipient name.

**Coverage.** FY2014 to FY2024 e-files: 2,038 rows, $1,171,884,901 in cash
grants. FY2025 adds 377 rows (13 to 501(c)(3)s or governments, 364 to other
organizations, per the filer's own counts). FY2012 and FY2013 are small and
PDF-only. Every row is a direct report by the filer; nothing is interpolated.
Grants of $5,000 or less are excluded by the form's own rule, so the count of
small grants is a floor. Recipient EIN is present on all but two rows.

**Changes over time.** The IRC section field changes vocabulary: `501(c)(3)`
and `501(C)(3)` both appear; from FY2020 `GOVERNMENT ENTITY` and from FY2021
`STATE OF OHIO` appear for public recipients. The purpose field is free text:
"ECONOMIC DEVELOPMENT" (upper case) on 1,637 rows, "Economic Development" on
338, blank on 28, and a handful of specific descriptions, mostly FY2015 to
FY2016. Program type (Inclusion Grant, Workforce Grant, etc.) is not in the
990 in any year; it comes from the monthly metrics reports below.

**Suppressed, censored or masked values.** None on the face of the form. The
$5,000 floor is the only exclusion.

**Missing data.** Two rows lack an EIN (FY2016, FY2024). 28 rows have a blank
purpose. Non-cash assistance is zero on every row in every year.

**Revisions.** None unless amended. We pin the object IDs above.

**Units and rounding.** Whole dollars. Fiscal year ends June 30; "FY2024" means
July 1, 2023 to June 30, 2024. Grant dates within the year are not given.

**Known quirks.**

- *Schedule I does not tie to Part IX line 1.* JobsOhio reports on the accrual
  basis. Part IX line 1 (grants to domestic organizations, accrued expense)
  and the Schedule I cash total differ every year, in both directions:

  | FY | Schedule I cash | Part IX line 1 |
  |---|---|---|
  | 2014 | $1,308,000 | $3,862,966 |
  | 2015 | $19,302,675 | $46,551,991 |
  | 2016 | $28,135,693 | $31,763,625 |
  | 2017 | $41,326,967 | $55,950,421 |
  | 2018 | $68,814,015 | $72,468,892 |
  | 2019 | $76,872,922 | $112,393,413 |
  | 2020 | $192,865,029 | $233,138,690 |
  | 2021 | $116,309,674 | $210,000,654 |
  | 2022 | $151,122,798 | $238,403,120 |
  | 2023 | $311,677,347 | $481,659,666 |
  | 2024 | $164,149,781 | $138,478,131 |

  Confirmed by the filer. Schedule O in the FY2022 to FY2024 returns says:
  "The statement of functional expenses is prepared on the accrual basis of
  accounting and Schedule I is prepared on the cash basis of accounting.
  Accordingly, a variance exists between the amounts reported for grant
  expense on each schedule." So Schedule I is cash paid in the year, which is
  what the headline measures. A year of large new commitments (FY2023)
  accrues more than it pays; a later year (FY2024) pays out prior accruals.
  Grants of $5,000 or less also sit in the gap. The post says "grants paid,
  as reported on Schedule I," not "all grant spending."
- *FY2023 and FY2024 row count mismatch.* The filer's line 2 and line 3
  counts sum to 386 (11 + 375) in FY2023 and 362 (12 + 350) in FY2024, but
  the tables have 315 and 312 rows. Other years match. The XML has one
  Schedule I, no attachments and no rows elsewhere, so the counts may include
  grantees under the $5,000 floor or be a preparer's error. Unexplained; the
  dollars are summed from the rows, which are what the return actually
  discloses.
- *Recipient address is not headquarters.* 84% of rows carry an Ohio address.
  This is the grantee entity's mailing address, often the Ohio plant or a
  project LLC. It must not be used as the home-state flag.
- *One recipient files a foreign address.* British Airways plc (FY2024,
  $5,681,149) carries `ForeignAddress`, not `USAddress`. The first parser read
  only `USAddress` and left its street and city blank. Fixed November 3, 2026;
  a `country` column now carries the country code where there is one.
- *Recipients include project vehicles.* Rows like "101 WEST FIFTH LLC" and
  "300 CLINTON LLC" are real-estate or single-project entities. Each must be
  resolved to the operating company that benefited before size or home state
  can be judged.
- *Multi-year payments.* One commitment is often paid across several fiscal
  years (reimbursement basis, per Schedule I Part IV), so one company appears
  in several years. Counting rows overstates "grants" for large multi-year
  awards; the headline count uses unique parents.
- *Reversed grants.* 33 rows carry negative cash amounts, all in FY2019 to
  FY2022, totaling -$26,040,088. They record money returned or reversed:
  Bon-Ton Department Stores (-$200,000 in FY2020, after its 2018
  bankruptcy), Pactiv, Tramec Sloan and others; one payee is literally named
  "AJM PACKAGING CLAWBACK." 16 parents net to zero or below. Some negative
  rows have no positive row under the same EIN (Foundation Software,
  -$750,000 in FY2021; Hynes Industries, -$50,000 in FY2019), so the original
  payment was either before FY2014 or under another name or EIN. Dollar
  totals are net of reversals; a parent is counted as a recipient only if its
  net payment is above zero. Whether a reversal is a performance clawback or
  an accounting correction is not stated on the form.
- *The state code can be wrong,* and the errors fall into two patterns. In 15
  rows the state abbreviation contradicts the ZIP code. Ohio ZIP codes run 430
  to 459, which is how they were found.

  Thirteen are in FY2024 alone and twelve of those are the same mistake: an
  Ohio town whose name also exists in another state, entered with that other
  state's abbreviation while the ZIP stayed Ohio. Cambridge filed as MA, Troy
  as MI, Northfield as IL, Hillsboro as OR, Marysville as PA, Aurora as CO,
  Barnesville and Paulding as GA, Brooklyn Heights as NY, Franklin as TN,
  Trenton and Dayton as NJ. The thirteenth runs the other way: American Craft
  Brewery (Samuel Adams) in Boston, Massachusetts, ZIP 02210, filed as Ohio.
  The shape of it suggests a city-name lookup that picked the wrong state, and
  it is confined to one filing year.

  The other two, Arconic in FY2017 and FY2019, are a different error: city and
  state are the Pittsburgh headquarters while the ZIP, 44105, is the Cleveland
  plant. Address fields in one row can refer to two different places.

  Home state is taken from researched parent headquarters rather than this
  field, so three classifications had inherited the error and were corrected.
- *Case and punctuation vary* across years for the same recipient
  ("Company, Inc." vs "COMPANY INC"). Dedupe by EIN first, then normalized name.
  The same problem reappears one level up, in the researched parent name:
  "McKesson Corporation" and "MCKESSON CORPORATION" were counted as two
  companies, and research notes written into the name ("First Solar, Inc.
  (self; public company)") split a parent further. `09_analyze.py` merges
  parents whose normalized name, size bucket, home state and class all agree,
  and prints the merges and any same-name pair it refused to merge to
  `TIEOUT.md`. This moves counts, not dollars.

**Uncertainty.** None stated by the filer. The return is signed under penalty
of perjury and prepared by an outside firm.

**License and attribution.** Public record under IRC 6104. Cite as "JobsOhio
Form 990, Schedule I, fiscal years 2012 to 2025, via IRS e-file data
(GivingTuesday 990 Data Lake) and ProPublica Nonprofit Explorer."

---

## JobsOhio Monthly Executed Grants and Loans Reports (JobsOhio)

**What it is.** A monthly PDF table of projects whose incentive agreements were
fully executed that month: company, county, region, industry, jobs created,
new payroll, jobs retained, fixed-asset investment, program type, program
value. Annual compilations exist for 2015 to 2025. These are commitments, not
payments.

**Where it comes from.** `https://www.jobsohio.com/newsroom/reports-publications`,
files under `jobsohio.com/files/reports/` (e.g.
`2024_annual_monthly_metrics.pdf`, `monthly-metrics-<month>-2026.pdf`). PDF
tables, one row per agreement, parsed with pypdf.

**Version and vintage.** Published monthly; annual compilations are the monthly
tables stacked. No known revisions.

**Coverage.** Executed agreements 2015 to present. Program types seen:
Economic Development Grant, Workforce Grant, Research & Development Grant,
Revitalization Grant, Inclusion Grant, Vibrant Community Grant, Spec
Development Grant (OSIP), Growth Fund Loan. Loans and OSIP site grants are in
this list but are not Schedule I grants to businesses in the same way; the
match to Schedule I is by name and county, and unmatched rows on either side
are reported.

**Changes over time.** Two layouts. 2015 to 2021: a wide table with one
dollar column per program (Growth Fund Loan, Workforce Grant, Economic Dev.
Grant, Revitalization Grant, Revitalization Loan, Revitalization Grant Phase
II, Research and Development Grant; Inclusion Grant and OSIP columns appear in
2020 and 2021). 2022 onward: one line per agreement with "Program Type" and
"Program Value" columns; some 2022 months label the column "Record Type"; 2023
months prefix program names with codes (JOG, JOW, JORG, JOIG, JOL, JOSDGO).
From 2026 the Inclusion Grant is called the "JobsOhio Small Business Grant."
Column order also differs: Company, Industry, Region, County in the wide
layout; Company, County, Region, Industry in the long one. Program names are
folded to one family each in `scripts/names.py` (`program_family`).

**Suppressed, censored or masked values.** "TBD" appears in jobs and payroll
columns for site-development projects. Company names are as JobsOhio wrote
them, sometimes a holding company or a project LLC.

**Missing data.** Months missing from the site, if any, are logged in the parse.

**Units and rounding.** Whole dollars; jobs as integers.

**Known quirks.**

- The agreement date is the month of the report, not the payment date, so a
  2022 agreement may appear on Schedule I in FY2023 through FY2026, or never,
  if the company does not draw the grant.
- The company named here can differ from the Schedule I payee (parent vs.
  subsidiary), so matching is by normalized name with a conservative
  threshold; 76% of Schedule I recipients and 77% of dollars (FY2014 to
  FY2024) match a metrics record.
- Ten pages of the 2016 compilation were exported with a broken font: the
  space glyph reads as "!" or "&" and the hyphen as "0" or "Y"
  ("JobsOhio0funded"). The parser splits on the glyph; hyphenated company
  names on those pages may carry a stray digit or letter.
- In two 2021 months the Inclusion Grant column touches its neighbor and the
  two headers merge; those 54 rows are resolved by amount (Inclusion caps at
  $50,000) and flagged.
- 22 of 2,984 parsed rows (0.7%) lack a county, jobs or investment value
  because a wrapped line split them; they are listed in
  `data/commitments_anomalies.csv` for hand review.
- Loans (Growth Fund, Revitalization Loan) and OSIP site grants are in the
  list; they are kept for matching but are not grants to businesses in the
  Schedule I sense.

**Uncertainty.** None stated.

**License and attribution.** Public report by JobsOhio. Cite as "JobsOhio
Monthly Executed Grants and Loans Reports, 2015 to 2026."

---

## SEC EDGAR company submissions and Exhibit 21 (U.S. Securities and Exchange Commission)

**What it is.** For every SEC registrant, `data.sec.gov/submissions/CIK##########.json`
carries the legal name, IRS EIN, state of incorporation, business-address
state, and the filing index. Form 10-K text gives the employee count and
headquarters. Exhibit 21 to the 10-K lists subsidiaries.

**Where it comes from.** Bulk `https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip`
(1.5GB, one JSON per CIK) for the EIN-to-CIK map; per-filing 10-K via the
EDGAR archive; Exhibit 21 hits via full-text search at `efts.sec.gov/LATEST/search-index`.
Requests need a User-Agent with a contact address.

**Version and vintage.** Submissions JSON reflects the current registrant
record (current name, current address). Employee counts and HQ are taken from
the 10-K for the fiscal year of the grant, not the current record.

**Coverage.** Public companies and their registered subsidiaries only. Private
and private-equity-owned companies do not appear. Exhibit 21 omits immaterial
subsidiaries, so a project LLC may be absent even when its parent is public.

**Known quirks.** Employee counts in 10-Ks are worldwide, as of fiscal year
end, sometimes "approximately," sometimes full-time only. Recorded as a bucket
with the as-of date and the wording. Two Schedule I rows carry the placeholder
EIN 000000000, which also appears on tens of thousands of EDGAR records; it
is treated as missing. The bulk archive matched 165 recipient EINs. The EIN on an EDGAR record is entered by the filer and is not validated;
24 of the 165 matches carry an unrelated name (Calgon Carbon's EIN appears on
an R.R. Donnelley record; Church & Dwight's on an individual's). Others are
former names or parents (Noveon for Lubrizol). The match is therefore a hint
for research, flagged `edgar_name_match`, never a classification by itself.

**License and attribution.** Public domain. Cite as "SEC EDGAR."

---

## Form 5500 and 5500-SF annual returns (U.S. Department of Labor, EBSA)

**What it is.** Retirement and welfare plan filings by plan sponsors, with
sponsor name, sponsor EIN, plan year, and participant counts at the beginning
and end of the year.

**Where it comes from.** DOL bulk CSV datasets by filing year at
`https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/public-disclosure/foia/form-5500-datasets`.

**Coverage.** Sponsors with a plan. Plans under 100 participants file the
short form (5500-SF). A company with no plan is absent, which by itself points
toward small. Participant counts include former employees with balances and
exclude ineligible employees, so they are a size band, not a headcount.

**Known quirks.** Filed at the sponsor (usually parent or payroll entity)
level; the recipient EIN on Schedule I may belong to a subsidiary that does
not sponsor its own plan, or to a subsidiary with its own plan (JSW Steel USA
Ohio: 345 participants; parent JSW Steel: tens of thousands). Used as a size
signal for the entity, graded B; parent resolution still comes first. Large
employers' counts include retirees (General Electric: 490,975 in 2015). We
use plan years 2015, 2019 and 2023 and the largest plan per sponsor EIN,
beginning-of-year participants. 834 of 1,515 recipient EINs (FY2014 to
FY2024) have a filing in at least one of those years.

**License and attribution.** Public record. Cite as "U.S. Department of Labor,
Form 5500 datasets."

---

## Ohio Secretary of State business search (Ohio SOS)

**What it is.** Registration records for every entity doing business in Ohio:
entity type, domestic or foreign, formation or registration date, status,
registered agent.

**Where it comes from.** `https://businesssearch.ohiosos.gov`. The site was
showing a maintenance page on September 18, 2026; access method to confirm.

**Coverage.** All Ohio-registered entities. "Domestic" means formed under Ohio
law, which is not the same as headquartered in Ohio and is recorded only as a
secondary column.

**Known quirks.** Formation date of a project LLC close to the grant date
identifies it as a project vehicle. Name search is exact-prefix on the site.

**License and attribution.** Public record.

---

## Good Jobs First Subsidy Tracker (Good Jobs First)

**What it is.** A database of economic development awards with recipient names
matched to about 2,600 ultimate parent companies, including JobsOhio awards.

**Where it comes from.** `https://subsidytracker.goodjobsfirst.org`. Free web
search; CSV export requires a subscription, so it is used as a per-parent
spot check, not a bulk source.

**Coverage.** Parent matching covers large corporations only. A recipient with
no parent match is not thereby small.

**License and attribution.** Cite as "Good Jobs First, Subsidy Tracker" where
used.

---

## T-100 Domestic Segment, U.S. carriers (Bureau of Transportation Statistics)

**What it is.** Each U.S. airline's monthly report to the Department of
Transportation of every nonstop segment it flew: departures scheduled and
performed, seats and passengers, by carrier, origin, destination and month.

**Where it comes from.** TranStats download form
(`DL_SelectFields.aspx`, table T-100 Domestic Segment U.S. Carriers), posted
by `scripts/15_fetch_t100.py` with geography Ohio, which keeps segments with
an Ohio origin or destination. One CSV per year, 2019 to 2026, in
`data/raw/t100/` (not committed).

**Coverage.** Through June 2026 at download (September 19, 2026); the data
lags about three months. Carrier-reported, not sampled. A month with one
departure on a route can be a charter or a repositioning flight rather than
scheduled service, so a route's life is read from sustained months, not a
single flight.

**Known quirks.** Breeze is carrier code MX. Cincinnati (CVG) is in Kentucky,
so its routes are not in the Ohio pull. International routes are in a
separate table (T-100 International Segment).

**License and attribution.** Public domain. Cite as "U.S. Department of
Transportation, Bureau of Transportation Statistics, T-100 Domestic Segment."

---

## JobsOhio published program guidelines (JobsOhio)

**What it is.** The guideline document JobsOhio publishes for each incentive
program, read for four things: how the grant is paid, what the company must do,
what it must report, and what happens if it falls short. Twelve programs cover
every payment on Schedule I that can be tied to a program at all. Transcribed
to `data/program_terms.json`, one object per program, each with the exact
quote it rests on and the URL it came from.

**Where it comes from.** PDFs and pages under `jobsohio.com`, found through the
site's 1,363-URL sitemap and its incentives pages. One program (Aerospace and
Defense Opportunity) publishes a Word document instead. Fetched with the
User-Agent `Data 4 The People research`.

**How a payment gets a label.** `scripts/19_grant_conditions.py` joins each
Schedule I payment to a program through the program family recorded for that
recipient in JobsOhio's monthly project reports (`program_family` in
`scripts/names.py`), then takes the program's published terms. A recipient
credited with several programs takes the **weakest** published terms of those
programs, because the payment cannot be tied to one of them. Four labels:
`Conditional` (a written clawback or repayment trigger), `Partly conditional`
(reimbursement or stated job metrics, no clawback published), `Unknown`
(nothing published either way), and `Program unknown` (the payment cannot be
tied to a program).

**Coverage and its limits, which belong in the post.**

- 22.5% of paid dollars are `Program unknown`. About a quarter of recipients
  never appear in the monthly reports, and the air service grants appear in
  none of them, so those are labelled from the payee where it is an airline
  and left unknown otherwise.
- These are the **published** terms, not the terms in force. The individual
  grant agreement is not public, and at least one case shows terms exist that
  the guidelines do not print: JobsOhio sued Olive AI in Ohio state court over
  unmet job commitments, and Olive AI's payments match no published program.
  So the finding is about disclosure, and the post must say so.
- The Growth Fund Loan guidelines no longer exist anywhere. The old PDF 404s
  on the live site and the Wayback Machine holds only 404 responses for it, so
  the text was never archived and the program's terms are unrecoverable.
- Guideline documents are undated in the file and dated only inside the PDF,
  and they are revised without a version history. The dates in
  `program_terms.json` are the dates printed in the document read in 2026, so
  a 2016 payment may have been made under terms we cannot see.
- `Conditional` does not mean the money was clawed back, and `Unknown` does not
  mean it was not. The columns describe documents, not outcomes.

**License and attribution.** Cite as "JobsOhio program guidelines," with the
program name and the document date.

---

## Google News RSS, used as a distress index (Google)

**What it is.** Not a dataset. A search index used to find candidate failures
among grant recipients, because no public dataset lists company failures by
name. `scripts/17_distress_scan.py` queries each recipient's name without its
legal suffix against bankruptcy, receivership, liquidation, closure and layoff
terms, and splits the headlines into hard, soft and weak signals. Output:
`data/distress_candidates.csv`.

**Where it comes from.** `https://news.google.com/rss/search?q=...`, fetched
with `curl -sL` (the redirect is required) at 1.5 seconds between queries. No
key, no blocking at that rate. 1,485 distinct recipients scanned: 20 hard
signals, 64 soft.

**Why not court records as the index.** CourtListener's API now requires an
account, and its public pages start returning empty replies after roughly 25
queries, so the full recipient list cannot be swept there. The FJC Integrated
Database omits debtor names, which makes it unusable for name matching. Court
dockets are therefore used to **confirm** candidates, not to find them.

**The name test, and why it is strict.** A headline counts only if it carries
the first two words of the recipient's name with the legal suffix stripped
("petmin usa", "nostrum laboratories"). For a one-word name the suffix or the
payee's city must also appear, which is what stops a story about "Intel
Markets" counting against Intel Corporation. Headlines that match the article
body rather than the title are kept as weak signals and checked by hand.

**Coverage, and why the published count is a floor.**

- Headline-based, so a company that failed without coverage is missing, as is
  one whose Ohio site closed quietly.
- The payee is treated as the company, so a parent's filing that left the Ohio
  operation running is excluded, and a subsidiary failure under a healthy
  parent can be missed.
- Google News coverage thins out before about 2010 and for small local
  outlets, which biases against early years and small recipients.

**License and attribution.** Headlines are used as pointers to sources, not
quoted as findings. Cite the originating outlet, never Google News.

---

## Failure verification (court dockets, SEC filings, local news)

**What it is.** The step that turns a distress candidate into a finding or
throws it out. 84 candidates checked one at a time against the court docket
where one exists, the company's SEC filings where it is public, and the local
story where neither is available. Written to `data/research3/*.json` by the
procedure in `docs/FAILURE_VERIFY_PROMPT.md` and consolidated by
`scripts/21_failures.py` into `data/failures.csv`.

**What `failures.csv` holds.** Every candidate and every verdict, including the
rejects and the reason each was rejected, so the published count can be
audited. Verdicts: `Confirmed failure` (29, $86,537,093 paid), `Not a failure`
(49), `Different company` (4), `Before the grant` (1), `Unresolved` (1).
Confirmed rows carry a `category`, because "failure" covers five different
outcomes and the post should not add a sale to a bankruptcy: Bankruptcy or
receivership, Funded site closed, Mass layoff at the funded site, Sold or
absorbed, Subsidized service ended. The categories are assigned from an
explicit company-name map in `21_failures.py`, not from keywords, because
keyword rules misread "sold" in a closure notice and "closed" in a sale notice.

**The dominant failure mode, and it is worth stating in the post.** 49 of 84
candidates were the company appearing in somebody else's case: JPMorgan and
Morgan Stanley as creditors or fund sponsors, BDO as the author of bankruptcy
reports, British Airways as a customer of a liquidated Scottish contractor,
Rocky Brands as a creditor. A bank named in a bankruptcy court is not a bank
going bankrupt. Three more were a different company sharing a name, found by
checking city, industry and officers against the payee address.

**What is not settled, and must be caveated where used.**

- Columbus Steel Castings: the filing court and case number were not
  retrievable, and whether its $500,000 was paid before or after the May 16,
  2016 filing is unknown, because Schedule I carries fiscal years only.
- Multi-Color: the lead debtor's case number was not retrievable, though nine
  same-day affiliate petitions in Bankr. D.N.J. were seen.
- Goodlevel Enterprises: unresolved.
- CourtListener began returning empty pages partway through, and
  `archive.org` returned 429 and 504 throughout, so several paywalled local
  stories could not be read in full. Rows say in `notes` exactly what could
  not be obtained.

**License and attribution.** Court dockets and SEC filings are public records;
cite the court, case number and filing date. News stories are cited to the
originating outlet with its date.

---

## Franklin County Court of Common Pleas, JobsOhio party-name search (Ohio)

**What it is.** Every matter JobsOhio is named in, in the court where it is
headquartered and where its agreements are litigated. 89 matters from 2011 to
2026: 63 suits JobsOhio filed, 23 collection proceedings on judgments it won,
and 3 brought against it. This is the only public record of JobsOhio enforcing
repayment, and the complaints quote the agreements, which are otherwise not
public.

**Where it comes from.** The clerk's Case Information Online at
`https://fcdcfcjs.co.franklin.oh.us/CaseInformationOnline/`, by party-name
search for JOBSOHIO. The same system serves scanned images of the filings once
its disclaimer is accepted, so the complaints and judgment entries are
readable, not just the docket lines. Fetched with the User-Agent
`Data 4 The People research`. Raw list in
`data/research3/jobsohio_franklin_cases.csv`; per-case readings in
`data/research3/lawsuit_*.json` and `olive_ai_suit.json`; joined to the grant
data by `scripts/22_lawsuits.py` into `data/jobsohio_lawsuits.csv`.

**How a defendant is matched to a grant.** By normalized company name first,
then by distinctive-word overlap with legal suffixes and generic industry
words removed, and only when exactly one recipient matches. A match needs at
least two distinctive words of two or more letters on both sides: without that
floor, "JOSEPH H JAMES" matched "H&H INDUSTRIES INC," because both reduce to
the single token "h". 51 of the 63 defendants tie to a Schedule I recipient.
The 12 that do not were either paid under another name, paid $5,000 or less
(below the Schedule I threshold), given something other than a reportable
grant, or are individuals rather than companies.

**The sum pleaded is not the grant, and usually differs from it.** 31 of the 47
suits where both figures exist agree exactly; the other 16 differ for
structural reasons, not errors. A company can hold a grant agreement, a Talent
Acquisition Services agreement and a loan at once and be sued on one of them. A
suit can cover one of several grants (Keno Kozie took $40,000 in FY2019 and
$600,000 in FY2021 and was sued on the $40,000). The Schedule I figure is the
parent's total across years and payees, while a complaint pleads what was
disbursed under one agreement. And JobsOhio sometimes demands less than the
whole. `data/jobsohio_lawsuits.csv` carries an `amount_matches_990` column
marking every row where the two differ, so a pleaded sum is never mistaken for
a grant.

**Three instruments, and the attachment practice splits by instrument.** Grant
Agreements (the majority) attach the signed contract as an exhibit every time.
Talent Acquisition Services Agreements refuse every time, with the same
sentence about "confidential and/or competitive and/or trade secret
information." One case is a Loan Agreement with a Cognovit Promissory Note and
personal guarantees, where JobsOhio filed the complaint and a confession of
judgment the same day. So the text of a JobsOhio grant agreement is public and
the text of its services agreements is not.

**Coverage, and the limits that belong in the post.**

- **One county only.** JobsOhio is headquartered in Franklin County and sues
  there, but a suit filed in another Ohio county, in federal court or in
  another state would not appear. The count is a floor.
- A collection proceeding (case type CJ, or a case number containing JG) is a
  garnishment or certificate of judgment on an earlier suit, not a new suit.
  These are counted separately so the suit count is not doubled.
- **A satisfaction of judgment records that a judgment was paid. It does not
  state the sum actually paid,** and settlement agreements are generally not
  filed. The correct phrasing is "the judgment of $X was recorded as fully
  satisfied," never "JobsOhio recovered $X."
- Complaints quote the agreement but do not attach it. In the Olive AI case
  the complaint says why, twice: the agreement "contains confidential and/or
  competitive and/or trade secret information." Some material is sealed.
- Case status on the clerk's system (ACTIVE, CLOSED, INACTIVE) lags and is not
  a reliable guide to the merits. A judgment matter can read ACTIVE years
  after the judgment was satisfied.
- **The agreements sued on are not always grant agreements.** The Olive AI
  agreement was a Talent Acquisition Services Agreement under which JobsOhio
  paid subcontractors rather than the company. Each case records what the
  complaint itself calls the agreement, and the post must not upgrade a
  services agreement to a grant agreement.
- Complaints routinely say "one of its incentive offerings" without naming any
  of the 12 published programs, so these cases usually cannot be mapped onto
  the program taxonomy used elsewhere in this project.

**What the page shows, and why it changed.** The table column was originally
"Conditions" and reported what JobsOhio publishes. That was the wrong question.
A reader wants to know whether Ohio can get the money back, and the published
guidelines are nearly silent on it while the signed agreements are not. The
column is now **"Can Ohio get it back?"**, computed in
`scripts/19_grant_conditions.py` as a `recourse` grade on the evidence:

| Grade | Means | Paid dollars |
|---|---|---|
| `agreement seen` | this recipient's own signed agreement is in a court file and carries Section 9(b)(ii) | 0.9% |
| `standard form` | paid under a program whose agreements were obtained from court files, all carrying the identical clause | 69.2% |
| `published clawback` | no agreement obtained, but the program's guidelines publish a repayment trigger | 6.2% |
| `loan` | repayable as debt, which is not a performance clawback | 1.3% |
| `service not cash` | a services agreement: JobsOhio paid subcontractors and can bill the service value as liquidated damages | 0.1% |
| `none found` | nothing published and no agreement ever obtained | 0.9% |
| `program unknown` | the payment cannot be tied to a program at all | 21.4% |

So recourse is established for **76.4% of paid dollars**, nearly all of it on
the strength of the form agreement rather than on anything JobsOhio publishes.
A parent paid under several programs takes the weakest grade of those programs.

`none found` is the finding worth naming: it is almost entirely the Commercial
Air Service Restoration grants, $10,073,711 including $5,681,149 to British
Airways. Those guidelines describe a disbursement process and then say nothing
about what happens if a route ends, and **no airline appears among the 63
companies JobsOhio has sued**. That contradicts the common assumption, which
this project also started from, that the airline grants were paid only while
the route flew.

Reimbursement is deliberately **not** a recourse grade. It is how the money
goes out: the company spends first and JobsOhio repays documented costs, so a
company that never spends never collects. That limits what is at risk; it is
not a way to recover money already paid.

**Effect on `data/program_terms.json`.** The Talent Acquisition entry had
inferred that because the benefit is delivered as a service, there is "no
disbursement to reverse." The Olive AI docket disproves that: the company owes
the value of the services performed if it misses its metrics, and JobsOhio
took a $598,420.17 judgment on exactly that clause. The entry is corrected and
its confidence lowered to Medium. Its `conditional` label stays **Unknown**,
because that field records what JobsOhio publishes, not what is in force, and
the published fact sheet still carries no repayment language. The dollar
shares in `grant_conditions.csv` are therefore unchanged.

**License and attribution.** Court filings are public records. Cite the court,
case number, document and filing date.

---

## Method decisions changed on November 3, 2026

Recorded here because each one moves a published number, and the rule is that a
method change is documented in the commit that makes it.

**Placeholder parents are no longer parents.** A research pass that could not
find an owner wrote the word "unknown" or "unresolved" in the parent cell
instead of leaving it empty, and the analysis keyed on that word, merging 12
unrelated project LLCs into two companies. A recipient whose owner was not
found is now its own parent.

**A conflict between two payees of one parent is resolved against the finding,
not by read order.** Where two researched recipients of the same parent
disagree, the analysis takes the smaller size band, Ohio for home state, and
the non-`business` class, and still prints the conflict. Read order used to
decide. The class rule moved Nationwide Children's Hospital ($13,500,000) out
of the business denominator, which is why Ohio's share of business dollars fell
from 36.8% to 35.8%.

**The worst case sweeps on the weakest grade under a parent.** It used to sweep
on the grade inherited from whichever payee was read first, which let 6 parents
carrying $16.4 million escape although they had a C-graded payee. The published
floor is now 61.3% of dollars to large, down from 62.4%, which is the correct
direction: the old figure was less unfavorable than its own wording promised.

**`data/reversals.csv` is deleted.** Its `paid_before` column matched on exact
company name, so it missed offsetting positive rows filed under a different
spelling of the same EIN (BrewDog USA / BREWDOG COLUMBUS; Barclays Services
Ohio / BARCLAYS SERVICES LLC; THERMA-TRU CORP / THERMA-TRU CORP CLAWBACK; iSqFt
/ ConstructConnect; Unverferth three ways) and reported 21 net-zero recipients
for -$1,657,252 instead of 16 for -$757,252. Nothing in the pipeline read it.
`09_analyze.py` computes the figure correctly from the EIN-keyed join, and
`TIEOUT.md` carries it.

**`TIEOUT.md` now carries a Sensitivities section,** computed rather than
asserted. The two that matter:

**The class boundary was re-checked, and it holds.** All 122 parents classed
`site_development` were read again against one test: whose business is
building? A developer who builds and leases to others stays
`site_development`; an operating company that received money to build, expand
or clean up **its own** facility is that operating company, whatever the payee
vehicle is called. Decisions, one line of reasoning and a source each, are in
`data/site_dev_review.csv`; `scripts/25_apply_site_dev.py` folds them in.

**10 of 122 changed, all to `business`, carrying $11,139,868.** The small
share of business dollars moved 18.1% to 19.0%. That is the number that
matters here: the wholesale-reversal counterfactual below implies 8.1 points,
and the errors actually in the batch are worth about a tenth of that. The
counterfactual is an upper bound, not a live risk, and the post should say so.

The clearest changes: Ohio-West Virginia Excavating ($4,739,868), a general
contractor whose own name and EIN are on the 990; CrossCountry Mortgage
($1,000,000), whose JobsOhio project record names it with 180 jobs created;
GBQ Partners ($100,000), a Columbus accounting firm classed as a developer by
a name rule because "Partners" is in the name, which is the same error as
Tractor Supply.

**21 rows carry a standing caveat.** 12 are marked `OPEN` in the review: left
as `site_development` but never positively identified, the largest being CW
Partners LLC at $500,000, which rests on a name rule and nothing else. 9 are
marked `FLAG`: cases where `site_development` is defensible but a reader could
reasonably dispute it. The one to know is **Seefried Industrial Properties at
$17,205,000**, the largest site payment in the data. Seefried is correctly a
developer, but the beneficiary was Amazon, so a reader may fairly ask why the
biggest site payment sits outside the business denominator rather than
counting as large.

- *The class boundary is the largest exposure in the project.* 101 parents
  carrying $117,746,967 were classed out of `business` by hand after the
  automatic classifier called them businesses, mostly into site_development.
  96 of them, carrying $97,096,967, would have scored small. Recompute the
  headline on the automatic class and the small share of business dollars goes
  from 18.1% to 26.2%. The reclassification is defensible on the merits, since
  these are project vehicles and industrial developers rather than operating
  small businesses, but it is a judgment call worth $97 million that moves the
  headline 8 points toward the thesis, and the published worst case does not
  cover it. The post states the counterfactual.
- *One payment carries the home-state finding.* Intel Corporation alone is
  $124,422,793, 15.2% of business dollars, almost all of it one FY2023 payment.
  Leave Intel out and Ohio's share of business dollars goes from 35.8% to
  42.2%. The post names Intel beside the number.

**Two denominators, stated on purpose.** Size and home-state shares run on
dollars net of the 33 reversed payments ($1,171,884,901). The conditions shares
run on positive payments only ($1,197,924,989), because a reversal has no
program to label. Any sentence using either must say which.

**A guard now stops the analysis** if `review_size` or `review_hq` disagrees
with `emp_bucket` or `parent_hq_state`. The analysis reads the latter;
`18_apply_review.py` merges the former into it. Skipping that merge used to
mean a changed review answer was silently ignored.

---

## Method check: is Schedule I cash paid, or the award?

**Why this was tested.** The Republic Steel docket (23CV008186) shows a grant
agreement authorizing $500,000 and a complaint pleading that JobsOhio
"provided Defendant $300,000.00 in grant funds." The Schedule I row for that
company is a single FY2022 entry of **$500,000**, which equals the authorized
amount, not the pleaded disbursement. If Schedule I rows generally reported
awards rather than cash, the headline dollars in this project would be wrong.

**The test.** 1,119 recipients appear in both JobsOhio's monthly executed
grants reports (which record the award) and Schedule I (which JobsOhio's own
Schedule O says is cash). If Schedule I reported awards, the two would agree
almost always. They do not, and the disagreement is strongly size-dependent:

| Committed | Recipients | Schedule I equals the award | Cash as a share of commitments |
|---|---|---|---|
| $50,000 or less | 337 | 84.6% | 169.2% |
| $50,000 to $250,000 | 359 | 61.8% | 141.4% |
| $250,000 to $1,000,000 | 247 | 50.2% | 119.0% |
| Over $1,000,000 | 176 | **17.0%** | **54.5%** |

The large awards, where a partial draw is likely and where most of the money
is, behave exactly as cash should: only 17% match the award and the group drew
54.5% of what was committed. Small awards match because a $25,000 or $50,000
grant is a single lump that is usually drawn in full. Among the 859 recipients
with exactly one award in the monthly reports, 72.3% match, and the 15.7% that
drew less drew a median of 67% of the award.

The shares above 100% in the small bands are a limit of the commitments file,
not of Schedule I: a recipient with several awards may have only some of them
parsed out of the monthly report PDFs, so its commitment total is understated.

**Conclusion.** Schedule I is cash paid, as the filer states in Schedule O and
as the Part IX reconciliation shows. Republic Steel is a single-case
discrepancy, not a systemic one, and it is **not resolved**: the complaint
pleads $300,000 disbursed, the defendant's answer denies that it received
$300,000, JobsOhio dismissed with prejudice four months later, and no filing
reconciles either figure with the $500,000 on the return. Flagged as an open
item in `docs/STORY_LEADS.md` rather than used.

---

## What a "grant" on Schedule I can actually be

Three of the 63 lawsuits establish that some Schedule I rows are not cash
handed to the named recipient at all.

Under a **Talent Acquisition Services Agreement**, JobsOhio pays subcontractors
to perform services for a company, and the company owes the value of those
services if it misses its metrics. The INEOS complaint (21CV007238) states it
exactly: JobsOhio "commenced performance of the TAS Agreement and **incurred
$54,235 in subcontractor costs** necessary to provide the Deliverables and
Services." That $54,235 is the FY2021 Schedule I figure for INEOS Pigments USA
Inc. So the return reports as a grant to the company money JobsOhio spent with
vendors on the company's behalf. Olive AI, Nexient, Candid Care and Candle-Lite
show the same structure.

This bears directly on the Supply Line International Medical question in
`docs/STORY_LEADS.md` lead 8: a Schedule I row does not establish that the
named company received money.

**Also established:** JobsOhio's own form contemplates a company holding more
than one agreement. Section 9(a)(v) makes it a Breach if "Grantees are in
default of **any other agreement between Grantor and either Grantee**." So a
Schedule I row for a company can span a grant, a services agreement and a loan,
and a lawsuit covers one of them.

---

## JobsOhio Form 990 FY2025, from the filer's own PDF (JobsOhio)

**What it is.** Schedule I Part II for the year ending June 30, 2025: 377 rows,
$173,433,961 in cash grants. The same schedule as every other year, but read
from a PDF rather than e-file XML.

**Why a PDF.** The FY2025 return is in no machine-readable source. The
GivingTuesday data lake returns 404, the IRS S3 bucket (`irs-form-990`) returns
404, and ProPublica's API lists no filing for period 202506 at all. JobsOhio
posts its own return at
`https://www.jobsohio.com/files/tax-returns/b200_jobsohio_990_fed_pdc_ty24.pdf`
("ty24" is tax year 2024, which is the year beginning July 2024, which is this
project's FY2025). 84 pages, prepared by Deloitte Tax LLP.

**How it is read.** `scripts/23_parse_sched_i_pdf.py`, by word position rather
than text order. This matters: the first Schedule I page lays its columns out
in a different reading order from the 42 continuation pages, so
`extract_text()` returns six names, then six EINs, then six amounts, and
pairing those by order would be a guess. The geometry is identical on every
page and is not. Each recipient is one horizontal band holding the city, state
and ZIP at x<200, the EIN at x≈213, the cash at x≈370, the non-cash at x≈468
and the purpose at x≈637, with the name and street on the bands above.

**How it is checked.** The parse must equal the filer's own recipient count on
Schedule I Part I lines 2 and 3. It does: 13 + 364 = 377. **This is the only
year where that reconciles.** FY2023 (386 against 315 rows) and FY2024 (362
against 312) do not, as recorded above. The script exits rather than write a
file that does not foot, and also fails on any row with no recipient name.

**Coverage and limits.**

- A PDF read is a weaker source than XML and the post should say which years
  came from which. Nothing else in the pipeline treats FY2025 differently.
- The PDF carries no IRS object ID, so the `object_id` column is empty for
  these rows and the filing cannot be pinned the way the other eleven are. If
  the XML appears later, re-run `23_parse_sched_i_pdf.py` against it and the
  row counts should match exactly.
- Merged by `scripts/26_add_fy2025.py`, which replaces rather than appends the
  year's rows, validates every classification value the analysis reads, and
  refuses to write while any FY2025 recipient is still unresearched.

**The 274 new recipients** were classified by the same method and prompt as the
original 1,452 (`docs/RESEARCH_PROMPT.md`), in seven batches in
`data/research2025/`, with the site-developer test from the re-check applied
from the start.

**One known conflict this year creates.** Avery Dennison appears twice under
different EINs: Avery Dennison Retail Information Services (26-3306955, FY2022,
headquarters coded CA) and Avery Dennison Corporation (95-1492269, FY2025,
coded OH). Both are right at their own time, because the company moved its
headquarters from Glendale, California to Mentor, Ohio. They resolve to one
parent, so the home-state conflict rule fires and takes Ohio, which is the
conservative call against the finding that most dollars leave the state. The
conflict is printed in `TIEOUT.md` rather than hidden. $300,000 and $250,000
are the amounts involved.

---

## Company links on the page (various)

**What it is.** One link per company, so a reader can check the company rather
than take our word for it. `data/parent_links.csv`, built by
`scripts/27_resolve_links.py`.

**Why it was rebuilt.** The page used to link a company name to the first entry
in its research `sources`. Those fields record *how* a call was made, not
*where* a reader can go, so most of them were never URLs at all: "Form 5500
2023: 86 participants, largest plan, sponsor JAFE DECORATING, INC." A sample of
60 found **16 that resolved**. Of the 44 failures, 34 were prose rather than a
URL, four were Google News search queries, and four were SEC filings that
failed only because they were fetched without the contact User-Agent the SEC
requires.

**The order, which is the reader's order:**

1. **The company's own 10-K**, where it has an SEC CIK on file. Pulled from the
   SEC submissions API (`data.sec.gov/submissions/CIK##########.json`) so the
   link is the actual most recent annual report, not a search page.
2. **A press release or news report** of the announcement, from the URLs the
   research already cited.
3. **The company's own website.**

**Every link was fetched before it was written, and a link that did not resolve
was not written.** The page shows that company's name as plain text instead. A
dead link sends a reader nowhere and makes them doubt the rest of the row.

**Coverage.** 860 of 1,719 companies, carrying **$1,137,318,627 of
$1,346,076,114, or 84.5% of the dollars**: 87 to a 10-K, 78 to another SEC
filing, 221 to a press release, 224 to a news report, 250 to a company site.

The 859 unlinked companies carry $208,757,487 and are mostly small Inclusion
and Small Business Grant recipients whose only public record is JobsOhio's own
project report and a Form 5500 participant count. Leaving them unlinked is a
deliberate choice: no link is honest, an invented one is not.

**Re-checked independently.** A random 70 of the written links, fetched again
in a separate pass: **69 returned 200**. The one failure is a local news site
that serves 403 to automated fetches but loads in a browser.

**Known limits.** A link can rot after it is written, and the file records the
date nothing. The 10-K is the company's most recent, not the one covering the
grant year, so it shows the company as it is now rather than when it was paid.
Both belong in the methodology note.

---

## SBA small-business size standards (13 CFR 121.201)

**What it is.** The legal definition of a small business in the United States:
a table of every six-digit NAICS industry with the threshold below which a firm
in that industry counts as small. Pulled by
`scripts/28_sba_size_standards.py` into `data/sba_size_standards.csv`.

**Where it comes from.** The eCFR renderer,
`https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-13?part=121&section=121.201`,
rather than SBA's own PDF, because the eCFR is the authoritative current text
and is machine readable. SBA's PDF link moves with each revision and was 404 at
the time of writing.

**The finding that matters: there is no single SBA employee number.**

- 978 industries. **500 of them define small by average annual receipts, not by
  headcount at all** (soybean farming is $2.25 million of receipts).
- Of the 478 that do count employees, the threshold runs from **100 to 1,500**.
- The most used value is 1,000 employees (15.1%), then 750 (13.2%), then 1,250
  (11.1%). **500 employees is the standard for 47 industries, 9.8% of those
  that count employees and 4.8% of all industries.**
- For manufacturing (NAICS 31-33), which is most of what JobsOhio funds, all
  346 industries use an employee test and the **median threshold is 1,000**.
  500 covers 12.4% of them.

**What this project does with it, and why.** The cutoff stays at 500 by
default, and the page now says on its face why. Three reasons:

1. No single number can honestly be labelled "the SBA definition," so
   presenting one as official would be wrong.
2. The employee bands in this analysis are `<100`, `100-499`, `500-4999` and
   `5000+`. **A 1,000-employee line falls inside the 500-4999 band**, which
   holds 272 companies and $158,310,559, so it cannot be drawn from the data
   without headcounts finer than the bands, which many C and D graded
   recipients do not have.
3. 500 is the conservative choice. Because the SBA's manufacturing median is
   1,000, a 500 line counts **fewer** companies as small than the SBA would,
   which understates this project's own small-business share rather than
   flattering it.

Drawing an SBA-faithful line would mean a per-company NAICS code and an exact
headcount. JobsOhio's own reports give only coarse sector labels (Advanced
Manufacturing, Automotive, Logistics and Distribution) for 64% of recipients,
and those do not map to six-digit NAICS. That is the honest reason it is not
done, and it belongs in the methodology.

**License and attribution.** Public domain. Cite as "SBA size standards, 13 CFR
121.201," with the date retrieved.

---

## Known limit: a headquarters is recorded as of the grant, and can drift

The method says the home state is the ultimate parent's headquarters **at the
time of the grant**. Two error classes come out of that, and both have been
found in this data.

**Ownership drift**, now swept. 211 parents had been classified by the
automatic rules R1 to R4, which read a signal about the payee and never asked
who owned it. All 211 were re-checked (`data/research_owner/`,
`scripts/29_apply_ownership.py`): **44 had a parent other than themselves at
the time of the grant**, 10 were acquired only afterwards and were correctly
left alone, 8 could not be settled, the rest were independent. Net effect
**$1,520,000 moved out of the Ohio column and $300,000 into it**, on a
$1.35 billion base. The error was real and its consequence is small.

**Headquarters drift**, not swept, and named here as a limitation. A company
that moved after its grant can be recorded at the address it has now. One
confirmed case: **P.H. Glatfelter**, $500,000, FY2019, had been recorded in
North Carolina, which is where the registrant sits today as Magnera Corp of
Charlotte. Its 10-K for the year ended December 31, 2019 gives a
principal-executive-offices phone number in the 717 area code, which is York,
Pennsylvania; the move to Charlotte came in 2022. Corrected. Neither state is
Ohio, so no published Ohio figure moved.

A cheap scan for more of these — parents whose EDGAR current state differs from
the recorded state — returns 31 rows carrying $48,719,349, but nearly all are
the design working rather than failing: `edgar_hq_state` is the *payee's*
current registrant address while `parent_hq_state` is the *parent's* address at
the grant. General Electric is recorded Massachusetts for its 2018-2021 grants
and shows Ohio in EDGAR today because GE Aerospace is now in Evendale. That is
correct, not wrong.

Three of the 31 are recorded as Ohio and would be worth one look before a
second edition, because an error there would move a published figure:
**Milacron** ($1,500,000, FY2016), **Sterigenics US** ($500,000, FY2018) and
**CBTS Technology Solutions** ($450,023, FY2023). They are listed here rather
than chased because the signal is mostly noise and the expected yield is low.
