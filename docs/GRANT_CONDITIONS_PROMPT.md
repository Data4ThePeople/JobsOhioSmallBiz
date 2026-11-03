# What conditions came with each grant

Eric's question: for each grant, is there public evidence that the money was
**conditional** (paid only against documented costs, tied to jobs or
investment, repayable if the company did not deliver) or an **unconditional
check** that could not be clawed back?

Individual grant agreements are not public. JobsOhio is a private nonprofit
and is largely outside Ohio's public records law. So the evidence has to come
from what JobsOhio does publish, at the level of the program.

## What to collect, per program

Programs to cover (the families in `data/commitments_norm.csv`):

- Economic Development Grant
- Workforce Grant (and Workforce Training)
- Revitalization Grant, Revitalization Grant Phase II, Revitalization Loan
- Research & Development Center Grant
- Inclusion Grant / Small Business Grant
- Growth Fund Loan
- Vibrant Community Grant
- Ohio Site Inventory Program (OSIP), grant and loan, "Spec Development"
- Commercial Air Service Restoration
- Aerospace and Defense Opportunity Grant
- Talent Acquisition / Talent Attraction, and any "Other Grant"

For each program, find and quote the terms that answer these:

1. **How is the money paid?** Up front, or as reimbursement of costs the
   company has already incurred and documented?
2. **What must the company do to earn it?** Job creation, payroll, capital
   investment, a facility, a route operated, a completed cleanup.
3. **Can JobsOhio take it back?** Any clawback, repayment, recapture, default
   or "subject to repayment" language, and what triggers it.
4. **Is there a reporting requirement?** Annual reports, certification of
   costs, audits.

## Sources, in order (web search is not available)

- JobsOhio program pages: fetch `https://www.jobsohio.com/sitemap.xml`, then
  each `incentives-programs/...` page. Many carry a "View Program Guidelines"
  link to a PDF on jobsohio.com or a partner site; fetch the PDF and read it.
- JobsOhio's **policies** page and board documents: look in the sitemap for
  `about-us`, `meetings-and-financials`, `policies`, `standards`,
  `code-of-regulations`, and any "Standards of Program Operations" or
  "grant policy" document. These state the general terms for all programs.
- JobsOhio's Form 990, Schedule I, Part IV, already in the repo
  (`data/raw/990/`): JobsOhio's own description of how grants are paid and
  monitored. Quote it exactly.
- Regional partner and county development sites, which often reprint
  JobsOhio's program terms: teamneo.org, columbusregion.com,
  redicincinnati.com, daytonregion.com, ohiose.com, rgp.org, and county
  pages such as chooseclintoncountyoh.org, growgallia.com.
- The Ohio Development Services Agency / Department of Development, for the
  state programs JobsOhio's money sits beside (Ohio Tax Credit Authority
  agreements do have public clawback terms, and are a useful contrast).
- Wayback Machine for anything dead:
  `http://archive.org/wayback/available?url=SITE`.

Use `curl --max-time 30`, User-Agent `Data 4 The People research`.

## Output

Write `/Users/ericpachman/PycharmProjects/JobsOhioSmallBiz/data/program_terms.json`:
a JSON list, one object per program, with exactly these keys:

```
program, paid_how, performance_required, clawback, reporting,
conditional (Conditional / Partly conditional / Unconditional / Unknown),
evidence_quote, source, confidence (High / Medium / Low), notes
```

- `conditional` is the summary call:
  - **Conditional**: reimbursement of documented costs **and** stated
    performance requirements **and** repayment language.
  - **Partly conditional**: reimbursement or performance, but no repayment
    language found.
  - **Unconditional**: evidence that money is paid without conditions.
  - **Unknown**: nothing published either way. Say so plainly; this is a
    finding in itself.
- `evidence_quote` is the sentence that carries the call, quoted exactly.
- Save the file after every program.

Report back: the table of programs and calls, which programs published
guidelines and which did not, and anything that contradicts JobsOhio's
general statement that grants are paid on a reimbursement basis.
