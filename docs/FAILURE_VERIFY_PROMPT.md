# Verifying a company failure after a JobsOhio grant

`scripts/17_distress_scan.py` reads Google News headlines for every grant
recipient and flags anything that looks like bankruptcy, receivership,
liquidation or closure. Those flags are candidates. This prompt turns a
candidate into a finding, or throws it out.

Most flags are wrong in one of three ways, and each has to be ruled out:

- **A different company with the same name.** "Ohio Logistics" and "Multi-Color"
  exist in several states.
- **The company appears in someone else's case.** Banks and accounting firms
  turn up constantly as creditors, advisers or authors of bankruptcy reports.
  JPMorgan in a bankruptcy court is not JPMorgan going bankrupt.
- **The event came before the grant.** Only a failure in or after the first
  grant year counts.

## What to establish for each candidate

1. **Is it the same company?** Match on city or state, industry, and the
   officers' names where a story gives them. The payee address is in the
   input. If the match is only the name, say so and mark it unconfirmed.
2. **What happened, exactly?** Chapter 11 (reorganization), Chapter 7
   (liquidation), a state-court receivership, an assignment for the benefit of
   creditors, a plant closure, or layoffs only. These are different outcomes
   and the post will name them precisely.
3. **When?** The filing or announcement date. Compare it to `grant_years`.
4. **Which entity filed?** The grant payee itself, its parent, or a sister
   company. A parent's filing that leaves the Ohio operation running is a
   different story from the payee itself liquidating.
5. **What happened to the Ohio site and the jobs**, if a source says.

## Sources, in order (web search is not available)

- The court docket, which is the primary record. CourtListener's public search
  works at a slow pace: fetch
  `https://www.courtlistener.com/?q=%22NAME%22&type=r&order_by=dateFiled+desc`
  with a browser User-Agent, **wait at least 20 seconds between queries**, and
  stop querying it if replies come back empty, which means it is throttling.
  Read the case name, court ("Bankr. N.D. Ohio"), docket number and date.
- Google News RSS with `curl -sL`:
  `https://news.google.com/rss/search?q=%22COMPANY%22+bankruptcy`.
- The story itself. Many local outlets block direct fetches; use the Wayback
  Machine: `http://archive.org/wayback/available?url=THE_URL`, then fetch the
  snapshot.
- The company's own site and its last archived version.
- SEC filings for public companies (8-K announcing a filing). sec.gov requires
  the User-Agent `Data 4 The People research connect@data4thepeople.com`;
  everything else gets `Data 4 The People research`.

## Output

A JSON list, one object per candidate, exactly these keys:

```
recipient_id, name, verdict, event, event_date, entity_filed, court,
docket, same_company_evidence, ohio_outcome, confidence, source, notes
```

- `verdict`: `Confirmed failure`, `Different company`, `Not a failure`
  (the company appears in someone else's case, or the headline is about a
  report or a fund), `Before the grant`, or `Unresolved`.
- `event`: `Chapter 11`, `Chapter 7`, `Receivership`, `Assignment for benefit
  of creditors`, `Closure`, `Layoffs`, or empty.
- `confidence`: `High` (court docket or SEC filing seen), `Medium` (credible
  news story naming the company and the city), `Low` (name match only).

Save the file after every candidate. Report the confirmed failures with
amounts and dates, and say which ones you could not settle.
