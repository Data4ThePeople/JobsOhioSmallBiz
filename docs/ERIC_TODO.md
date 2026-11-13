# What Eric needs to do personally before publishing

Written 2026-11-13 for a Monday publish. Everything here needs a human: a phone
call, a judgment call, a browser, or a name on a request for comment. Work that
a script or an agent could do is not on this list; that work is being done.

Sections are in priority order. The first two are the ones that can change what
the piece says.

---

## 1. One phone call that could change a finding — Sauder Woodworking

**Time: 15 minutes. Do this one first.**

Sauder Woodworking laid off about 150 people at its Archbold plant in August
2025. We have that from the Bryan Times and two trade outlets. **Ohio has no
WARN notice for it**, and a permanent cut of 150 at one site normally requires
one. The state's register in that same window records notices for a single
person and for 39 part-time workers, so this is unlikely to be an oversight.

The likeliest explanation is that the layoff was expected to last under six
months, which Ohio exempts, and that fits the plant staying open. If that is
right, "mass layoff at the funded site" is the wrong label and the row should
move or come out.

Two calls, either of which settles it:

- **Sauder Woodworking, Archbold.** Ask: was the August 2025 layoff permanent
  or temporary, how many were recalled, and is the plant at full staffing now.
- **Ohio Department of Job and Family Services, Rapid Response**, which takes
  the notices: rapdresp@jfs.ohio.gov. Ask whether Sauder filed a WARN notice in
  2025 and, if not, on what exemption.

Right now the 150 figure rests on press reporting alone, and the piece says so.
A call either removes that caveat or removes the row.

---

## 2. Request for comment from JobsOhio

**Time: 30 minutes to send. Needs to go out well before Monday.**

The piece makes serious claims about a public-money body. It should go to them
first, and their refusal to answer is itself publishable. Suggested questions,
each tied to a number we can defend:

1. JobsOhio paid $1.37 billion in grants over twelve years. The returns record
   $26.0 million coming back, 1.9%. Is that the complete figure for repayments
   and clawbacks, and if not, what is?
2. 28 companies that were paid $86.9 million failed after the money went out:
   the funded site closed, there was a mass layoff there, the company went
   bankrupt, or it was sold. JobsOhio sued two of them. What determines whether
   it sues?
3. It has filed 63 suits in Franklin County since 2018, pleading $13.5 million
   in total, median $125,000. Judgments recorded as satisfied come to $3.2
   million. How much has actually been recovered?
4. Its standard agreement says "Notwithstanding the terms of this Agreement,
   Grantor has the discretion to determine compliance." Who exercises that
   discretion, how many waivers have been granted, and are any published?
5. 71% of dollars went to recipients whose agreement lets JobsOhio demand
   repayment. Ten of twelve programs publish no repayment language at all. Why
   is the clause not in the published guidelines?

**Give them a real deadline and record the date you asked.** If they answer,
several of these become much stronger with their number beside ours.

---

## 3. Two minutes in a browser — the FY2012 and FY2013 returns

JobsOhio filed those two years on paper. ProPublica has the PDFs but its
download sits behind a security check that refuses an automated fetch, so they
have to be clicked:

- FY2012: https://projects.propublica.org/nonprofits/organizations/452798687
- FY2013: same page, the 2014-03 filing

Save them into `data/raw/pdf/` as `jobsohio_fy2012.pdf` and
`jobsohio_fy2013.pdf` and there is a parser ready for them.

**This is optional and I would not hold the piece for it.** FY2013 total
expenses were $7.2 million against $584 million in FY2023, so the two missing
years are about 1% of the organization's spending and cannot move any published
share. The page already discloses that they are excluded.

---

## 4. Judgment calls that are yours, not mine

These are decisions about what the piece claims, and I should not make them
alone.

**a. The headline failure number moved, and may move again.** It is now **28
companies and $86.9 million**, down from 31 and $90.7 million, because three
companies turned out to have failed at a site the grant did not pay for. More
candidates are being verified now and the number may rise. Decide whether you
want the piece built on a number that is still moving, or whether we freeze the
count at a stated cut-off date and say so.

**b. How hard to push the "failed elsewhere" three.** Dana, New Horizons Baking
and FedEx Supply Chain each closed an Ohio operation while the site Ohio paid
for kept running. That is not the claim the count makes, so they are out of it,
but it is interesting on its own: it is the kind of thing a press office would
use to say "we don't count that" if we had counted it. Currently they get their
own view in the tool. Decide whether they get a paragraph in the post.

**c. Whether the piece says anything about the pandemic cluster.** 46% of
Ohio's entire WARN register is 2020, and March to June 2020 alone is 28% of it.
That shapes any claim about layoffs at grant recipients and we hold those
candidates to a higher bar. It is honest and a little technical. Your call
whether it belongs in the post or only in the method note.

---

## 5. Before you hit publish

- [ ] `python3 scripts/30_audit_summary.py` — must print 28 of 28 pass
- [ ] `python3 scripts/31_audit_failures.py --fetch` — must print no problems,
      and the `--fetch` run confirms every source link still resolves
- [ ] Read the "After the grant" column on the page and hover three rows at
      random. Every one should name the site the money paid for, the site that
      failed, and either Ohio's own notice or why there isn't one.
- [ ] Confirm the count on the page matches whatever you decided in 4a.

---

## Still open, being worked on, no action from you yet

Listed so nothing gets lost, not because you need to do them.

- Verification of the new candidates the WARN join turned up, including FCA's
  1,225-job Toledo notice and Pixelle's 780-job Chillicothe mill
- Whether the March-June 2020 candidates were temporary or permanent
- Eight companies that filed a mass-layoff notice **before** Ohio paid them;
  Mobis is the strongest, with a 210-job Toledo notice in November 2024 and a
  grant in 2025
- Republic Steel's Lorain idling date, AK Steel's funded county, Goodlevel
  Enterprises, the Olive AI state-court file, Multi-Color's Batavia plant,
  Nostrum's Bryan plant
- An independent recomputation of the headline shares from the raw filings
