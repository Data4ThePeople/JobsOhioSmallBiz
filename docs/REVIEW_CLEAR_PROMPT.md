# Clearing the review list

Eric reviewed 97 of the 215 companies on `data/review_simple.csv` by hand.
This prompt is for agents finishing the rest: confirming or correcting the
size and home-state call for each remaining company, with an employee
estimate and an honest confidence.

---

For each company in the input JSON list, answer three questions.

1. **Size at the time of the grant.** Was the ultimate parent above or below
   **500 employees worldwide** in the grant years (`years`, fiscal years
   ending June 30)? Return `Large` or `Small`.
2. **Home state at the time of the grant.** Was the ultimate parent
   headquartered in Ohio? Return `Yes` or `No`, plus the state or country in
   `hq_where`. The company's Ohio plant does not make it Ohio-headquartered.
3. **How sure are you?** `High` (a filing, a JobsOhio or partner release, or
   a news story states the size or ownership), `Medium` (a company page or
   a credible secondary source), `Low` (inference from the signals only).

Also give `employees_estimate`: the best figure or range you can support
("about 120", "250-400", "over 10,000"), and `employees_asof` (the year it
describes). A range is fine and is preferred over a false precision.

## Sources, in order

Web search is **not available**. Use direct fetches with
`curl --max-time 30`:

- SEC EDGAR. User-Agent must be
  `Data 4 The People research connect@data4thepeople.com` for sec.gov only;
  every other site gets `Data 4 The People research`. Company lookup:
  `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=NAME&type=10-K&output=atom`;
  full-text search `https://efts.sec.gov/LATEST/search-index?q=%22NAME%22&forms=10-K`.
  Read the 10-K "Human Capital" or "Employees" section, and Exhibit 21 for
  subsidiaries.
- The company's own site: `/about`, `/about-us`, `/careers`, `/locations`.
- JobsOhio: fetch `https://www.jobsohio.com/sitemap.xml`, grep the company or
  county, then fetch the release. Releases often give employees and owner.
- Google News RSS: `https://news.google.com/rss/search?q=%22COMPANY%22+Ohio`.
  Headlines alone are often enough to date an acquisition.
- Wayback Machine for dead or blocked pages:
  `http://archive.org/wayback/available?url=SITE` then fetch the snapshot.
- Form 5500 participant counts already in the input (`f5500_participants_*`):
  the sponsor's own retirement plan. Under 250 points to a small employer;
  over 1,500 to a large one. It counts former employees with balances, so it
  is a band, not a headcount.
- `metrics_*` fields: JobsOhio's own project report for this company. An
  Inclusion or Small Business Grant is capped at $50,000 and restricted to
  small businesses. `jobs_retained` is employment at the Ohio site, a floor.

## Rules

- **Judge the parent, not the grantee.** A small Ohio plant of a large or
  foreign group is Large, and its home state is the parent's. Check for
  "a member of", "a subsidiary of", "part of the ___ Group" on the company
  site, and for acquisitions in news RSS.
- **A private-equity fund is never the parent.** Use the operating group the
  fund owns, and that group's size and headquarters.
- **A sister company is not a parent.** Companies under common individual
  owners stay their own parent.
- **Use the grant years.** A company bought or grown after its grant years
  keeps the owner it had then; say so in `notes`.
- Never guess from revenue or from the grant amount alone.
- If nothing can be found, keep the current call, mark `Low`, and say in
  `notes` what you tried. That is a useful answer, not a failure.

## Output

A JSON list, one object per input company, exactly these keys:

```
company, size, ohio_hq, hq_where, employees_estimate, employees_asof,
confidence, parent, source, notes
```

`company` is copied verbatim from the input. `source` is the URL that carries
the most weight; `notes` is one or two sentences. Save the file after every
company so nothing is lost if the run is cut off.
