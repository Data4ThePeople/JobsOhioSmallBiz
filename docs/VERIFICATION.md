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

### Result of the ownership check

All 427 rows were checked. 27 turned out to belong to a larger group
($7.3 million of grants) and were reclassified to the parent: among them
Adalet (Berkshire Hathaway), Wayne Trail (Lincoln Electric), IMCO Carbide
(Berkshire Hathaway), Aer Lingus (IAG), Imperial Electric (Nidec), Daido
Metal USA (Daido Metal), Miba Energy (Miba AG), FacilitySource (CBRE) and
Forsee Power (France). Another 16 kept their size but moved home state,
because their owner was a smaller company outside Ohio (Dewesoft, Slovenia;
ASHTA Chemicals, Mexico; SentriLock, National Association of Realtors,
Illinois) or because the company itself was based elsewhere. 328 were
confirmed or presumed independent, and 65 could not be settled either way;
those keep the rule's classification. In the later, smaller batches a "no"
usually means nothing contrary was found, not that independence was proven.

Private-equity ownership was handled one way throughout: the fund is never
the parent. A company owned by a fund is classified under the operating group
the fund built, and is small if that group had fewer than 500 employees in
the grant years (Thaler Machine, n2y, PUI Audio).

### Effect on the headline (businesses, 500-employee cutoff)

| | Before the check | After |
|---|---|---|
| Small share of recipients | 63.9% | 61.1% |
| Small share of dollars | 19.6% | 18.4% |
| Worst case, dollars to large | at least 61.5% | at least 62.1% |

(These are the figures after the first check only; the final figures are below.)

### Second ownership check: researched small businesses

The random re-check also found 3 errors in 67 researched rows (4.5%), all of
the same kind: a subsidiary of a larger group counted as small. So the same
ownership check was run on every researched small business outside the hand
review and the random sample: 221 recipients, $37.0 million. 12 (5.4%, $2.5
million) belonged to a larger group and were reclassified, among them Grady
McCauley (LSI Industries), JR Manufacturing (Nippon Steel Trading), Hamilton
Safe (Gunnebo, Sweden), 20/20 Custom Molded Plastics (Inteplast) and deSter
(gategroup, Switzerland). Several more moved home state to a smaller
out-of-state parent.

### Headline after both checks (businesses, 500-employee cutoff)

| | Before the checks | After |
|---|---|---|
| Small share of recipients | 63.9% | 60.1% |
| Small share of dollars | 19.6% | 18.1% |
| Worst case, dollars to large | at least 61.5% | at least 62.3% |

## A second rule assumption: Ohio headquarters

Rule R1 also recorded every Inclusion Grant recipient as Ohio-headquartered,
since the program funds Ohio businesses. The ownership check found
independent R1 recipients based elsewhere (Walkenhorst's, Sparks, NV; Tiger
Pistol, Austin, TX), and four more R1 rows carry a non-Ohio address on
Schedule I. Those six were moved to their own state. An R1 recipient with an
Ohio address and no contrary evidence stays Ohio-headquartered.

## Limits

The two passes are not fully independent: both used the same written method,
the same signals, and the same model family, and both worked without a web
search engine. Agreement between them shows the method gives the same answer
twice; it does not prove the answer is right. The hand review of the largest
recipients and the source links in the published table are the check on that.

---

# Verification of the FY2025 classifications

## What was checked

A random sample of **60** of the 274 recipients that first appear on the FY2025
return, drawn with a fixed seed (20261112). A second pass classified each one
from the same signals, with no access to the first pass's answers, following
the same written method (`docs/RESEARCH_PROMPT.md`). Output:
`data/research2025/verify25.json`.

The second pass was told explicitly not to open `data/parents.csv`, the
first-pass batch files, `dist/data.json`, `TIEOUT.md` or `docs/STORY_LEADS.md`,
and reported two honest leaks: it grepped `DATASETS.md` for two method sections
(that file was not on the exclusion list), and the session's git context
displayed a commit subject carrying a first-pass aggregate. Neither conveys a
per-company answer, so the pass stands, but it is recorded here rather than
left out.

## Raw disagreement, before anyone judged which pass was right

| Field | Disagreements | Rate |
|---|---|---|
| Size band | 2 of 60 | 3.3% |
| Home state | 1 of 60 | 1.7% |
| Recipient class | **0 of 60** | **0.0%** |
| Small/large at the 500 line | 1 of 60 | 1.7% |
| Ohio / not Ohio | 1 of 60 | 1.7% |

For comparison, the original pass over the FY2014-2024 recipients disagreed on
**6.7%** of size calls. The FY2025 work is about half that rate, and the class
call — which decides the headline denominator and is the largest sensitivity in
the project — agreed on every one of the 60.

## None of the three disagreements moves a published headline figure

Each was adjudicated on the evidence, and each sits outside the business
denominator or is the same call either way.

1. **NP DWBA LLC, $800,000.** First pass: NorthPoint Development, 500-4999.
   Second: the payee itself, under 100. **Kept as NorthPoint.** "DWBA" is the
   Dayton-Wright Brothers Airport; WDTN reported NorthPoint beginning the $146
   million First Flight Commerce Center at that site in April 2024; and
   NorthPoint's two other Ohio project vehicles in this file carry the same
   "NP" prefix. The grade stays D, because that is a naming and location
   pattern rather than a document naming this LLC. Classed `site_development`
   by both passes, so the band never enters the business headline.
2. **Progressive Automations USA, $50,000.** First pass: under 100. Second:
   100-499. Both grade D, no published headcount exists. **Both are "small" at
   the 500 line**, so the call is identical where it matters and the
   disagreement is cosmetic.
3. **Spring & Main LLC, $60,000.** First pass: Ohio. Second: California.
   **Kept as Ohio.** The California address on Schedule I is Silicon Valley
   Bank's Santa Clara office, a lender or escrow address, while the LLC is
   named for a street corner in Lima and the project is a downtown Lima
   redevelopment. Classed `site_development` by both passes, so the business
   home-state figure is unaffected; it does sit in the all-recipients view.

## What the second pass flagged that the first did not

Seven rows it judged unsettlable by any public source, all graded D by both
passes: NP DWBA, TCG Corrina Owner I, Spring & Main, JT and Sons, Persys
Engineering, Universal Design and Fabrication, Progressive Automations USA.
Three near-boundary calls worth knowing: Taikisha Ltd sits at 5,525 employees,
barely over the 5,000 line, on a figure dated a year after the grant; Pallet
Distributors is under 100 on 89 Form 5500 participants; Ark Transportation is
under 100 on 36 retained jobs but committed to 103.

One shared-source warning: JobsOhio's own June 2023 report line reads
"Universal Design and Fabrication LLC Wika", which looks like two table rows
run together by the PDF parser. If so, the county tag may belong to the other
company, and the defect is in `commitments_norm.csv` rather than in either
research pass.
