# Reading a JobsOhio collection suit

JobsOhio publishes guidelines for 12 incentive programs. Only 2 of them print
any repayment or clawback language, and those 2 cover 6.8% of the money it has
paid. The individual agreements are not public.

But JobsOhio sues. A party-name search of the Franklin County Court of Common
Pleas returns 63 suits it has filed since 2018, and 52 of the defendants are
companies on its own Form 990 grant schedule. **The complaints quote the
agreements.** That is the only public place the terms appear, so these dockets
answer the question the guidelines do not: what does JobsOhio actually require,
and does it get the money back?

## How to read a case

Everything is on the Franklin County Clerk of Courts site,
`https://fcdcfcjs.co.franklin.oh.us/CaseInformationOnline/`. It serves both the
docket and scanned images of the filings once its disclaimer is accepted.
Search by case number. Open the docket, then open the filed PDFs.

Read, in this order:

1. **The complaint.** It is usually short, 5 to 15 pages, and it is where the
   agreement is quoted. Get the exact wording.
2. **Any judgment entry**, default or agreed. It carries the dollar figure.
3. **Any satisfaction of judgment, dismissal or settlement notice.** This is
   how the matter ended.

Use the User-Agent `Data 4 The People research`. Web search is not available;
fetch directly. Do not put any personal email address in a request.

## What to pull out

- **The agreement.** Its name and date. It may be a grant agreement, a loan, a
  Talent Acquisition Services Agreement, or something else. Say which. Do not
  call it a grant agreement unless the complaint does.
- **The program.** Many complaints say only "one of its incentive offerings"
  and never name a program. If so, say that.
- **The repayment provision, verbatim.** Quote the sections the complaint
  block-quotes, exactly as written, with the section numbers. This is the most
  valuable thing in the docket. Note whether the remedy is called a clawback,
  liquidated damages, repayment, or something else.
- **The commitments.** Jobs created, jobs retained, payroll, investment, and
  the metric evaluation and expiration dates.
- **The shortfall.** What the company actually reported or achieved.
- **The amount sought**, and whether it is the full award or a part.
- **Whether the agreement is attached as an exhibit.** Often it is not, and
  the complaint says why. Quote that reason.
- **The outcome.** Default judgment, agreed judgment, dismissal, settlement,
  still pending. The date. Whether a satisfaction of judgment was filed.
- **The amount recovered,** but only if a filing states it. A satisfaction of
  judgment means the judgment was recorded as paid; it does not state the sum
  actually paid, so say "judgment of $X recorded as satisfied," never
  "JobsOhio recovered $X."

## Output

Append to your assigned file a JSON list, one object per case, with exactly
these keys:

```
case, defendant, agreement, agreement_date, program, amount_sought,
job_commitments, shortfall, repayment_quote, remedy_named, agreement_is_exhibit,
outcome, outcome_date, amount_recovered, confidence, source, notes
```

- `confidence`: `High` (the filed PDF read), `Medium` (docket entries only),
  `Low` (case exists but nothing readable).
- `repayment_quote`: the verbatim text, or empty if the complaint does not
  quote the agreement. Empty is a real and useful answer; do not paraphrase
  into this field.
- `source`: the docket URLs you actually opened, with the date.

Save the file after every case, so a case already read is not lost. Report
which cases you could not open and why. A clean "the image would not load" is
more useful than a guess.
