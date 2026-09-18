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
`USAddress/CityNm`, `USAddress/StateAbbreviationCd`) are stable across all 11.
Pre-2013 schemas used different names; none of our XML files predate 2013.

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
- *Recipients include project vehicles.* Rows like "101 WEST FIFTH LLC" and
  "300 CLINTON LLC" are real-estate or single-project entities. Each must be
  resolved to the operating company that benefited before size or home state
  can be judged.
- *Multi-year payments.* One commitment is often paid across several fiscal
  years (reimbursement basis, per Schedule I Part IV), so one company appears
  in several years. Counting rows overstates "grants" for large multi-year
  awards; the headline count uses unique parents.
- *Case and punctuation vary* across years for the same recipient
  ("Company, Inc." vs "COMPANY INC"). Dedupe by EIN first, then normalized name.

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
is treated as missing. The bulk archive matched 165 recipient EINs.

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
