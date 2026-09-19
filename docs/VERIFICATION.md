# Verification of the recipient classifications

## What was checked

A random sample of 150 recipients, drawn with a fixed seed (20260918) from
the 1,301 classified recipients paid less than $1,000,000 in total
(`scripts/10_verify_sample.py draw`). Recipients paid $1,000,000 or more are
reviewed by hand instead (`data/review_for_eric.csv`).

The sample covered every first-pass method in rough proportion: 67 rows
classified by research, 28 by rule R1 (Inclusion Grant), 31 by rule R2 (own
Form 5500 plan under 250 participants), 13 by rule R3 (own plan of 1,500 or
more participants) and 11 by rule R4 (public or nonprofit entity with an Ohio
address).

A second, independent pass researched each sampled recipient from the same
signals, without access to the first answers, using the same written method
(`docs/RESEARCH_PROMPT.md`). The comparison is `scripts/10_verify_sample.py
compare`; the raw output is `data/verify_summary_raw.txt` and every
disagreement is in `data/verify_report_raw.csv`.

## Raw disagreement (before anyone judged which pass was right)

| Field | Disagreements | Rate |
|---|---|---|
| Small or large at 500 employees | 12 of 150 | 8.0% |
| Employee bucket | 25 of 150 | 16.7% |
| Parent headquarters state | 19 of 150 | 12.7% |
| Recipient class (business, nonprofit, etc.) | 5 of 150 | 3.3% |

Size-call disagreements by first-pass method: rule R1 2 of 28, rule R2 5 of
31, research 5 of 67, rules R3 and R4 none.

## Adjudication

Each size-call disagreement was settled by reading both passes' sources.

- The second pass was right in 10 of the 12: ISS America (Daido Metal,
  Japan), Egelhof Controls (EGELHOF Group, Germany), Test-Fuchs (Austria),
  Modula (Italy), WIKA Sensor Technology (WIKA Group, Germany), Chalfant
  Manufacturing (OBO Bettermann, Germany), Steiner eOptics (Beretta Holding),
  RKDS (Rural King), The Hilsinger Company (Hilco Vision), and Braun
  Industries (Demers Braun, Canada, after its February 2018 merger; 96% of its
  grant dollars came after the merger).
- The first pass was right in 2: WellPet (owned by Berwind during the grant
  year, and the method uses the owner at the time of the grant) and Navarre
  Facility (Tractor Supply's own announcement, against an unconfirmed
  alternative).

**Error rate on the small-or-large call: 10 of 150, 6.7%.** By method: rules
R1 and R2, 7 of 59 (11.9%); research, 3 of 67 (4.5%); rules R3 and R4, 0 of
24. Every one of the 10 errors classified a large company as small. None went
the other way.

Of the other home-state and class disagreements, the second pass was
accepted for 11 (among them two nonprofits the R2 rule had counted as
businesses, and three parents headquartered outside Ohio) and the first pass
kept for 3.

## What the errors showed, and what was done about it

The rule errors share one cause. Rules R1 and R2 read the size of the entity
that received the grant, and a small US subsidiary of a larger or foreign
group looks small on both signals: it can win an Inclusion Grant, and it runs
its own small retirement plan. Because every error ran from large to small,
the rules overstated the small-business share of recipients, the half of the
finding that favors the story. They had almost no effect on dollars.

Rather than publish the error rate alone, every remaining R1 and R2 row (427
recipients, $54.4 million) was put through a narrow ownership check
(`docs/SUBSIDIARY_CHECK_PROMPT.md`, applied by
`scripts/13_apply_subsidiary.py`): was the company owned by a larger, foreign,
or private-equity-backed group during the grant years?

## Limits

The two passes are not fully independent: both used the same written method,
the same signals, and the same model family, and both worked without a web
search engine. Agreement between them shows the method gives the same answer
twice; it does not prove the answer is right. The hand review of the largest
recipients and the source links in the published table are the check on that.
