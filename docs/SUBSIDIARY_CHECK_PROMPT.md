# Subsidiary check prompt

Used for recipients first classified by rule R1 (Inclusion Grant) or R2 (own
Form 5500 plan under 250 participants). The random re-check found these rules
miss US subsidiaries of larger or foreign companies (Egelhof, Test-Fuchs,
Modula, Chalfant/OBO Bettermann, ISS America/Daido Metal, WIKA). This pass
asks one narrow question per recipient.

---

For each recipient in the input JSON list, answer: **during the grant years
(`years`, fiscal years ending June 30), was this company owned or controlled
by a larger company, a foreign company, or a private-equity-backed platform
with 500 or more employees in total?**

How to check, in order, stopping as soon as it is settled:

1. Read the name for markers: "USA", "America", "North America", "Inc." after
   a foreign-sounding brand, "LP", a brand you recognize as a larger group.
2. Fetch the company's own site (`https://www.NAME.com`, `/about`,
   `/about-us`, `/locations`) and look for "a member of", "a subsidiary of",
   "part of the ___ Group", "headquartered in", a list of plants in several
   countries, or a parent logo.
3. Google News RSS: `https://news.google.com/rss/search?q=%22NAME%22+acquired`
   and `...q=%22NAME%22+subsidiary`.
4. The JobsOhio release for the project (sitemap grep at
   `https://www.jobsohio.com/sitemap.xml`), which often names the parent.

Use curl with `--max-time 30` on every request; web search is not available.
Save the output file after every recipient.

Also report a parent that is **not** larger. If the company was owned by
any other company during the grant years (a smaller domestic or foreign
group, a family holding company elsewhere), fill `parent` and
`parent_hq_state` even when `owned_by_larger` is `no`, and give its size in
`emp_bucket` if known. Headquarters is judged at the parent, so a small
Ohio plant of a 300-person French company is small but not Ohio-headquartered.
A private-equity fund is never the parent: report the operating group or
platform the fund owns, and that group's headquarters and size.

Output: a JSON list, one object per input recipient, with exactly these keys:

```
recipient_id, owned_by_larger (yes / no / unknown), parent, parent_hq_state,
emp_bucket, source, notes
```

- If `owned_by_larger` is `yes`: `parent` is the ultimate parent,
  `parent_hq_state` its two-letter state or country name, `emp_bucket` the
  parent's worldwide size (`500-4999` or `5000+`), `source` the URL that shows
  the ownership.
- If `no` and independent: leave `parent`, `parent_hq_state`, `emp_bucket` empty; `source` is
  the page that shows it is independent (an "about" page naming the founders
  or family owners, a "family-owned since" line), or empty if you only found
  nothing contrary.
- If `unknown`: nothing either way; leave the fields empty.

Keep `notes` to one sentence.
