# Parent-resolution research prompt

This is the instruction given to each research agent, one batch of recipients
at a time. It is kept here so the method is reproducible and can be quoted in
the post's methodology.

---

You are classifying recipients of JobsOhio grants (from JobsOhio's IRS Form
990 Schedule I). For each recipient in the JSON list below, determine the
ultimate parent company at the time of the grant, that parent's headquarters
state, the parent's worldwide employee count bucket at the time of the grant,
and whether the recipient is an operating business at all. Return one JSON
object per recipient.

## Definitions

- **Ultimate parent**: the top of the ownership chain at the time of the
  grant years listed in `years` (fiscal years ending June 30). A subsidiary,
  project LLC, or plant entity resolves to the company that controls it. A
  private-equity-owned company resolves to the operating company, not the PE
  fund, but note the PE owner in `notes`. If the recipient was acquired
  after the grant years, use the owner during the grant years.
- **parent_hq_state**: two-letter US state of the parent's headquarters at
  the time of the grant, or the country name if outside the US (e.g.
  "Japan", "Germany"). The recipient's own Ohio plant address does not count.
- **emp_bucket**: the parent's total worldwide employees at the time of the
  grant, one of `<100`, `100-499`, `500-4999`, `5000+`. When the exact number
  is unknown, pick the bucket the evidence supports and lower `confidence`.
- **recipient_class**: `business` (operating for-profit company),
  `site_development` (real-estate or single-project LLC receiving a site,
  spec-building or revitalization grant; name the developer as parent),
  `government`, `university`, `hospital` (nonprofit health system),
  `nonprofit` (chambers, economic development corporations, foundations,
  JobsOhio network partners, event committees).
- **founded_in_ohio**: `yes`, `no`, or `unknown`. Whether the parent was
  founded in Ohio. Only fill when a source says so.
- **confidence**: `A` the size and parent come from an SEC filing, an IRS
  record, or the company's own audited report for the grant year; `B` from a
  JobsOhio or regional partner press release, a Form 5500 participant count,
  or a reputable news story naming the size and owner; `C` from a company
  website, LinkedIn, Wikipedia, or a business directory; `D` unresolved,
  best guess. General knowledge is not a source: every grade above D needs a
  URL you actually fetched.

## Signals already gathered (use them, cite them where they decide the call)

- `edgar_name`, `edgar_state_inc`, `edgar_hq_state`: the recipient's EIN is
  an SEC registrant. Public company or filing subsidiary. Cite the 10-K.
  If `edgar_name_match` says DIFFERENT NAME, the EIN on file at the SEC
  belongs to another filer (EINs are self-reported and sometimes reused) or
  to a former name or parent; confirm the link before relying on it.
- `f5500_participants_YYYY`: Form 5500 plan participants for the recipient's
  EIN (largest plan, beginning of year). Includes former employees with
  balances. Under 250 means very likely under 500 employees at that entity;
  over 1,500 means very likely over 500. The entity may still be a
  subsidiary of something larger, so check the name.
- `metrics_programs`, `metrics_jobs_retained_max`, `metrics_industry`,
  `metrics_commit_total`: JobsOhio's own project report for this company.
  An **Inclusion Grant** (also called Small Business Grant) is restricted to
  small businesses and capped at $50,000; a recipient with only that program
  is small unless something contradicts it. `jobs_retained` is existing
  employment at the Ohio site, a floor on company size.

## Method

1. Start from the signals. If the name is a well-known public company, cite
   its 10-K for the grant year (sec.gov) for employees and HQ.
2. Otherwise search for the company with its city: JobsOhio and regional
   partner releases (jobsohio.com, teamneo.org, columbusregion.com,
   redicincinnati.com, daytonregion.com, rgp.org, ohiose.com), the state's
   Tax Credit Authority approvals, local business press (Columbus Business
   First, Crain's Cleveland, Dayton Business Journal, Cincinnati Business
   Courier, Toledo Blade), then the company site and LinkedIn.
3. For an LLC that looks like a project vehicle, find the JobsOhio release
   for the project in that county and month; it names the operating company.
4. Do not guess a size from revenue or from the grant amount. If you cannot
   find a source, set `confidence` to `D`, pick the bucket that the signals
   most support, and say in `notes` what you looked for.
5. Every row must carry at least one URL in `hq_source` or `emp_source`.
6. **Search budget.** You have about 200 web searches for the whole batch.
   Plan on at most 6 per recipient, fewer for the easy ones. Prefer direct
   fetches of known endpoints over searches: EDGAR full-text search
   (`https://efts.sec.gov/LATEST/search-index?q=%22COMPANY%22&forms=10-K`),
   a company's own site, `https://www.jobsohio.com/news?search=COMPANY`.
   When the signals already settle the call (an Inclusion Grant with a small
   jobs-retained figure, or a Form 5500 count under 100), one search to
   confirm the parent and headquarters city is enough. If the budget runs out,
   finish the remaining rows from the signals at confidence `D` and say so in
   `notes`; never leave a row out.

## When web search is unavailable

The session's search budget may already be spent. Then work from direct
fetches, which earlier batches found reliable:

- EDGAR full-text search JSON: `https://efts.sec.gov/LATEST/search-index?q=%22COMPANY%20NAME%22&forms=10-K`
  and company lookup `https://www.sec.gov/cgi-bin/browse-edgar?company=NAME&type=10-K&output=atom`
  (use curl; for sec.gov only, the User-Agent is
  "Data 4 The People research connect@data4thepeople.com", which SEC requires;
  every other site gets "Data 4 The People research"; never use any other
  email address; the fetch tool is blocked by sec.gov). Read the 10-K "Human Capital" or "Employees" section.
- JobsOhio releases: fetch `https://www.jobsohio.com/sitemap.xml`, grep for
  the company or county, then fetch the release.
- Google News RSS: `https://news.google.com/rss/search?q=%22COMPANY%22+Ohio`
  (article URLs are encoded; the title and source are usually enough).
- Wikipedia REST summary for well-known companies:
  `https://en.wikipedia.org/api/rest_v1/page/summary/TITLE`.
- ProPublica Nonprofit Explorer for nonprofits and governments:
  `https://projects.propublica.org/nonprofits/organizations/EIN`.
- The company's own site guessed from its name (`https://www.NAME.com/about`).
- Team NEO, One Columbus, REDI Cincinnati, Dayton Development Coalition,
  RGP Toledo and OhioSE news pages.
If none of these settle a row, grade it `D`, pick the bucket the signals
support, and say what you tried.

## Saving progress

Work can be cut off by a usage limit at any time. Before starting, check
whether the output file already exists; if it does, keep its rows and
research only the recipients it is missing. Rewrite the whole output file
(valid JSON, all rows done so far) after every five recipients, not only at
the end.

## Output

Write a JSON list to the file path given, one object per input recipient,
with exactly these keys:

```
recipient_id, recipient_class, parent, parent_hq_state, hq_source,
emp_bucket, emp_source, emp_asof, confidence, founded_in_ohio, notes
```

`emp_asof` is the year the employee figure refers to (e.g. "2022"). Keep
`notes` to one or two sentences: the employee figure found, the ownership
chain if any, and anything a skeptical reader would ask about.
