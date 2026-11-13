# Draft email to the reporter

Paste block below. The link goes where you drop it; I have left `[LINK]`.

---

**Subject:** Embargoed: every JobsOhio grant on the 990s, searchable, with the failures flagged

---

Hi [name],

Here is the thing I mentioned, under embargo and still a work in progress:

[LINK]

**What it is.** Every grant over $5,000 that JobsOhio reported paying on its
IRS Form 990 Schedule I, fiscal years 2014 to 2025. 2,415 payments, $1.35
billion, 1,700 parent companies. Each recipient is traced to its ultimate
parent and sized by worldwide employees, so you can ask what share of the
money went to small businesses and what share went to companies
headquartered in Ohio. Click any tile to filter the table under it.

Everything behind it is in the repo: the method in `DATASETS.md`, the data in
`data/`, and three independent recomputations in `docs/TIEOUT_INDEPENDENT_*.md`
by people who were not allowed to read the analysis code. Every figure can be
re-added from the source files.

**Six things to know before you quote any of it.** I would rather you hear
these from me than find them.

1. **Half the failure findings are softer than the other half.** 44 companies
   that were paid $97,709,323 failed after the money went out. **22 of those
   rest on a court filing or the employer's own notice to the state. The other
   22 rest on reporting I could not tie to an Ohio document.** The page says
   which is which, and every row carries its source on hover. The second group
   is where your phone will be worth more than my spreadsheet.

2. **One company is half the money.** Ultium Cells is $50,000,000, 51% of all
   the failed dollars, and **its plant is open.** Ohio's notice breaks the cut
   into 484 permanent and 850 temporary, and the temporary workers were
   recalled. The median failed grant is $500,000; the mean of $2.2 million is
   almost entirely that one row. If you use a dollar total, say what is in it.

3. **The biggest thing in the data is not in the count at all.** The method
   looks for an event: a bankruptcy, a closure, a layoff. A grant paid towards
   a plant that was then abandoned produces none of those. **$28,599,868 went
   towards a Belmont County petrochemical plant that was never built**, across
   three recipients, and none of them is or could be in the failure count. One
   $20 million reversal from that project is 77% of all the money JobsOhio has
   recorded coming back in twelve years. That is lead 18 in
   `docs/STORY_LEADS.md` and I think it is the best thing here.

4. **Three companies failed somewhere other than the site the grant paid
   for**, and they are shown separately rather than counted: Dana closed Lima
   but was paid for Maumee, New Horizons closed Toledo but was paid for
   Norwalk, FedEx closed Lima but was paid for Columbus. A fourth, Toledo
   Innovation Center Landlord, is marked unresolved on purpose: Bitwise
   collapsed in that building but the building opened and is letting, and 18
   Ohio jobs is not a mass layoff.

5. **Ohio only publishes layoff notices from 2020.** Anything earlier rests on
   court dockets and news. Separately, 46% of that whole register is 2020 and
   March to June alone is 28% of it, which is the shutdown: I hold those
   candidates to a higher bar and drop most of them, so if you re-derive a
   number from the raw register you will get a bigger one than mine.

6. **One data file has known defects and it is not the one the headline uses.**
   `commitments_norm.csv`, JobsOhio's own monthly project reports, has 24
   truncated company names and is missing November 2016 entirely, because the
   space character on those pages renders as a dollar sign. It touches no
   published share. `scripts/39_audit_commitments.py` prints the damage. If you
   work from that file, read that first.

**What I have not done.** I have not put any of this to JobsOhio yet. I am
not publishing a story about these companies: the plan is to publish the tool
and let people who cover these beats work the leads. There are 19 of them in
`docs/STORY_LEADS.md`, each written with what is verified separated from what
is not, and several say in terms how not to write the finding.

**One ask.** If you find something wrong, tell me and I will fix it and say so
in the repo. If you work one of the leads, I would like to know which, so I am
not handing the same one to someone else.

Happy to talk through any of it.

Eric

---

## Notes for Eric, not for the email

- **The repo was already public**, and has been throughout. The embargo is a
  courtesy ask on the page and in this email, not a technical control. Anyone
  who finds the repo can read the data and the leads today.
- **`docs/ERIC_TODO.md` is public and names your strategy**, including the four
  questions you plan to put to JobsOhio and the recommendation to hand the
  Dayton records request to a local newsroom. JobsOhio can read that now. Say
  the word and I will move it out of the repo.
- The page carries "Last verified 13 November 2026" because the failure count
  moved five times in two days. If he quotes 44 in March, that date is how he
  checks whether it is still 44.
