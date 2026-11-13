# What Eric needs to do personally before publishing

**Scope changed 2026-11-13: the post is an announcement of the tool, not a
story about what is in it.** The leads go to local reporters to work. That
removes several items from this list and it raises the bar on one thing, so
read the next paragraph before the list.

**A tool is held to a higher standard than a story, not a lower one.** In a
story a sentence can carry its own hedge. In a table a row either says a
company had a mass layoff or it does not, and the reader who acts on it is a
reporter who will ring that company. Every caveat therefore has to live in
the row, on hover, where someone filtering the table will meet it. That is
already how the tool is built, and it is why the validation work continues
rather than stopping here.

**The count is 43 companies and $97,009,323.**

Sections are in priority order.

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

## 2. Give JobsOhio notice, and ask four questions

**Time: 30 minutes to send. It should go before the tool is public.**

You are not making an argument about JobsOhio, but the tool asserts that 43
companies it paid $97,009,323 failed afterwards, and it names every one. That
is worth putting to them first, and whatever they say belongs in the
announcement. Four questions, each tied to a number the tool will show:

1. JobsOhio paid $1.37 billion in grants over twelve years. The returns record
   $26.0 million coming back, 1.9%. Is that the complete figure for repayments
   and clawbacks, and if not, what is?
2. On our reading of Schedule I, 43 companies that were paid $97.0 million
   failed after the money went out: the funded site closed, there was a mass
   layoff there, the company went bankrupt, or it was sold. We will publish
   the list. Is any of it wrong?
3. It has filed 63 suits in Franklin County since 2018, pleading $13.5 million
   and recovering $3.2 million in judgments recorded as satisfied. Three of
   the 43 were sued. What determines whether JobsOhio sues?
4. Its transparency page says that once a project is complete it "publicly
   shares all its executed grant agreements and loans". Several completed
   projects in this data have no published agreement. What is the rule?

**Offer them the data before it is public.** If a row is wrong, you would
rather hear it from them this week than from a reporter next month. Record the
date you asked.

## 3. Decide whether the Dayton records request is yours or a reporter's

**Time: 5 minutes to decide, 20 to send if you keep it.**

JobsOhio announced the Avelo Dayton route itself, the route flew nine months,
and the announcement is no longer on its site. **No public document states the
$200,000**; it comes off the tax return. The City of Dayton owns the airport
and is subject to public records law where JobsOhio is not, so a request to
the city should produce the agreement and the figure.

Under the old plan this was yours. Under the new one it is the single best
thing to hand a Dayton reporter: it is local, it is concrete, and the request
writes itself. Lead 17 has the addresses and the exact records to ask for.

**My recommendation: give it away, and say so in the handoff.** A Dayton
newsroom will get a faster answer from its own city than you will, and it is a
better story with a local byline on it.

## 4. Two minutes in a browser — the FY2012 and FY2013 returns

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

## 5. Judgment calls that are yours, not mine

Most of what was here was about how hard to push a story, and the scope change
retires those. Three remain, because they are about what the tool asserts.

**a. Ultium Cells: decided, nothing needed.** It stays Michigan, because
recoding it on plant location would force the same on Honda ($47.4m, plants
all in Ohio, counted to Japan) and Fuyao ($10.6m, Moraine, counted to China).
Schedule I also shows $20,000,000 of the $50,000,000 remitted to GM's head
office in Detroit. The page names it next to Intel and states the cost of the
call: count Ultium as Ohio and the home-state dollar share goes 36.2% to
41.4%. Only act if you disagree.

**b. Does the tool state a cut-off date?** The count moved three times today,
31 to 28 to 43. It should now be stable, because the WARN join is exhaustive
over 2020 to 2026 and the earlier years have no register to search. But a
reporter who cites "43" in March should be able to tell whether that was still
the number. **My recommendation: put the date the data was last verified on
the page**, next to the count. It costs a line and it makes the figure
quotable.

**c. What the announcement says about the pandemic.** 46% of Ohio's entire
WARN register is 2020, and March to June alone is 28% of it. The tool holds
those candidates to a higher bar and excludes most of them. A reporter working
from the tool needs to know that or they will re-derive a different number and
think we are wrong. **My recommendation: one sentence in the announcement and
the full account in the method note**, which is where it already is.

Retired by the scope change: how hard to lead on Republic Steel, whether
Sherwin-Williams gets named as a concentration risk, and whether the three
"failed elsewhere" companies get a paragraph. All three are now the tool's
job, and the tool already shows them.

---

## 6. Before you hit publish

- [ ] `python3 scripts/30_audit_summary.py` — must print 28 of 28 checks pass
- [ ] `python3 scripts/31_audit_failures.py --fetch` — must print no problems;
      the `--fetch` confirms all 43 source links still resolve
- [ ] `python3 scripts/39_audit_commitments.py` — expect 24 truncated names and
      the November 2016 gap. These are known, documented, and do not touch a
      published share. If the numbers have grown, something regressed.
- [ ] Open the tool, filter to each of the five outcome tiles, and hover three
      rows at random in each. Every one should name the site the money paid
      for, the site that failed, and either Ohio's own notice or why there is
      none. **This is the check that matters most now**, because it is what a
      reporter will do.
- [ ] Click "show what was rejected, and why" and confirm 71 rows appear. That
      view silently rendered nothing for a while.
- [ ] Read `docs/TIEOUT_INDEPENDENT_3.md` when it lands and act on anything in
      it before publishing.

---

## 7. Smaller things the independent tie-out raised, if there is time

`docs/TIEOUT_INDEPENDENT_2.md` reproduces every headline share to seven
decimal places, which is the main thing. It also found these, none of which
moves a headline:

- **DATASETS.md states a class rule the code does not implement.** The doc says
  a mixed-class parent takes the non-business class; the code behaves as
  "largest payee's class". Only Tractor Supply discriminates, and applying the
  written rule moves the small share 18.90% to 18.94%. Either fix the doc or
  fix the code; they should not disagree.
- ~~The confidence A/B/C/D panel does not reproduce~~ **Fixed.** It was
  showing whichever payee's grade was read first, while the worst-case bounds
  swept on the weakest, so the page really was displaying one grading and
  computing its bounds on another. Evidence now takes the weakest grade among
  a parent's payees and reproduces 1,700 of 1,700. Ten rows moved, mostly B to
  C.
- **The recourse block divides by net dollars** where DATASETS.md says the
  conditions shares use positive payments. "70.7%" is 71.09% on the stated
  rule.
- **Roughly a dozen prose figures in DATASETS.md are a fiscal year out of
  date**, listed in section 3.8 of the tie-out.
- **10.2% of the small-business dollars rest on no headcount source** — 79
  business recipients whose `emp_source` is a search URL or nothing, 48 of them
  counted small.

---

## 8. The FirstEnergy question, which is now a reporter's and not yours

**The largest payment in the data has no project behind it.** $12,408,019 to
FirstEnergy Corp in FY2017. Its commitment row does exist, in a November 2016
report our parser silently dropped, and it is a **$14,000,000 Revitalization
*Loan* to FirstEnergy Generation, LLC**.

One part of this is yours and one is not.

**Yours, and small:** if that money is a loan draw rather than a grant, the
repayment column for the row is wrong and the dollar base needs a sentence.
Worth half an hour before publishing, because the tool shows that row. Read
the November 2016 report directly and check the Schedule I purpose text.

**Not yours:** FirstEnergy Generation is the subsidiary that became
FirstEnergy Solutions and went bankrupt in 2018, and FirstEnergy is the
company at the centre of the HB6 prosecution. Lead 16 says, and I still think,
that the finding here is a $12.4 million payment with no public project
record, and that reaching for HB6 needs reporting this project has not done.
Under the new plan that is exactly the kind of thing to hand over. Give it to
a reporter who covers that beat.

**The parser defect behind it needs nothing from you.** 24 truncated company
names, November 2016 missing, a row shift in June 2023.
`scripts/39_audit_commitments.py` reports them and `DATASETS.md` describes
them. **None touches a published share.** I deliberately did not fix them: the
obvious fix cut the file by 516 rows when I tried it. Post-publication work.

---

## 9. The handoff itself, which is now the point

The process has an outreach step (4a, a list of at least twelve reporters and
advocates for you to confirm; 4b, a tailored email to each, saved as Gmail
drafts and never sent). Under the old plan that was a step after the story.
Under the new one it **is** the deliverable, and it should probably be built
before the announcement rather than after it, so the announcement can say the
leads are already with people.

Two things I would want from you before drafting that list:

- **Which beats.** The seventeen leads split roughly into economic
  development and state accountability (Columbus), aviation (Dayton), steel
  and manufacturing (Youngstown, Lorain, Canton), and bankruptcy or courts.
  Say which of those you want covered and I will build the list against it.
- **How much to give each one.** A tailored email naming the one lead that
  fits that reporter's patch pulls harder than a link to seventeen. It also
  takes longer. Say which you want.

`docs/STORY_LEADS.md` now opens with a front door written for that audience
rather than for you, so it can go out as-is.

---

## Still open, no action from you yet

- The last research pass came back. Republic Steel, AK Steel, Goodlevel,
  Multi-Color and Avelo are resolved and applied. Nostrum is partly resolved:
  the Bryan plant's last recorded production is 3 March 2025 and its equipment
  was auctioned on 14 April, but **no Bryan headcount exists on the reachable
  record** and the monthly operating reports that would settle it are on
  PACER at about a dollar each.
- The Olive AI state-court file was already complete in
  `data/research3/olive_ai_suit.json`; that item is closed.
- Eight companies filed a mass-layoff notice **before** Ohio paid them. Most
  are the 2020 shutdown and unremarkable. One is not: **Mobis**, a 210-job
  permanent cut in Toledo in November 2024 and a $700,000 grant in FY2025. The
  catch is that the notice is filed by Mobis North America and the grant went
  to Mobis US Electrified Powertrain, a different entity at a different Toledo
  plant with the same Hyundai Mobis parent. The accurate sentence is "Ohio paid
  one Hyundai Mobis company while another cut 210 jobs across town", and
  JobsOhio could settle it by giving the payment date.

---
