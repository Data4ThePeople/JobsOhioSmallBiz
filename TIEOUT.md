# Tie-out

Every number below is recomputed from `data/grants_raw.csv` and `data/parents.csv` by `scripts/09_analyze.py`.

- Schedule I rows: 2,038; distinct recipients: 1,515; parents: 1,452; FY2014 to FY2024; cash $1,171,884,901
- Reversed payments (negative Schedule I rows): 33 rows, $-26,040,088; parents netting to zero or less, not counted as recipients: 16 (net $-757,252)
- Parents counted (net payment above zero): 1,452; with a classification: 1,452, carrying $1,172,642,153 of the $1,172,642,153 they were paid on net (100.0%)

## By recipient class (all parents)

- business: 1,245 parents, $832,890,284 (71.1%)
- site_development: 112 parents, $96,763,402 (8.3%)
- university: 11 parents, $95,233,751 (8.1%)
- hospital: 7 parents, $77,635,725 (6.6%)
- nonprofit: 37 parents, $41,160,782 (3.5%)
- government: 40 parents, $28,958,209 (2.5%)

## Businesses only

- Cutoff 100 employees: parents small 38.7%, large 61.3%, unknown 0.0%; dollars small 7.8%, large 92.2%, unknown 0.0%
- Cutoff 500 employees: parents small 60.4%, large 39.6%, unknown 0.0%; dollars small 19.0%, large 81.0%, unknown 0.0%
- Cutoff 5000 employees: parents small 80.8%, large 19.2%, unknown 0.0%; dollars small 35.4%, large 64.6%, unknown 0.0%
- Home state: parents Ohio 63.1%, other 36.9%, unknown 0.0%; dollars Ohio 36.5%, other 63.5%, unknown 0.0%
- Worst case: dollars to large at least 60.7%; parents small at least 45.3%
- Two-by-two (dollars): large|ohio 20.2%, large|other 60.8%, small|ohio 16.3%, small|other 2.7%

## All recipients

- Cutoff 100 employees: parents small 40.5%, large 55.1%, unknown 4.4%; dollars small 15.7%, large 82.8%, unknown 1.5%
- Cutoff 500 employees: parents small 60.4%, large 35.2%, unknown 4.4%; dollars small 25.7%, large 72.9%, unknown 1.5%
- Cutoff 5000 employees: parents small 78.4%, large 17.1%, unknown 4.4%; dollars small 39.5%, large 59.0%, unknown 1.5%
- Home state: parents Ohio 66.6%, other 33.4%, unknown 0.0%; dollars Ohio 51.6%, other 48.4%, unknown 0.0%
- Worst case: dollars to large at least 54.5%; parents small at least 40.4%
- Two-by-two (dollars): large|ohio 29.5%, large|other 43.4%, small|ohio 20.7%, small|other 5.0%, unknown|ohio 1.5%

## Conflicts between recipients of one parent

Resolved against the finding, not by read order: the smaller size band, Ohio, and out of the `business` denominator.

- bucket: 100-499 vs 500-4999 (SFG GEIS SHALERSVILLE LLC)
- bucket: 500-4999 vs 100-499 (NP FTC LLC)
- class: business vs hospital (THE RESEARCH INSTITUTE AT NATIONWIDE CHILDREN'S HOSPITAL)
- class: site_development vs business (TRACTOR SUPPLY COMPANY)

## Sensitivities

These are not errors. They are the places the headline is most exposed, computed so the post can state them before a reader finds them.

**The class boundary, and it is the largest one.** 94 parents carrying $105,107,099 were classed out of `business` by hand after the automatic classifier called them businesses, mostly into site_development: project LLCs and industrial developers rather than operating companies. 91 of them, carrying $87,807,099, would have scored small. Recompute the headline on the automatic class instead and the business universe goes 1,245 parents / $832,890,284 to 1,332 / $935,784,008, and the small share of business dollars goes **19.0% to 26.2%**. The published worst case does not cover this: it reassigns size inside the business set and never reconsiders the class boundary. The post should state this figure itself rather than wait to be asked why a company that builds and leases industrial buildings is not a small business.

**One payment carries the home-state finding.** Intel Corporation alone is $124,422,793, 14.9% of all business dollars. The top three (Intel Corporation, Ultium Cells LLC (50/50 join, The Sherwin-Williams Company) are 26.0%. Leave Intel Corporation out and Ohio's share of business dollars goes **36.5% to 42.9%**, and the large share goes 81.0% to 77.7%. Its classification is not in doubt, so this is leverage rather than error. Name it beside the number.

**The small share leans on a few weakly-graded size bands.** Ohio-West Virginia Excavating Co. (Dennis Hend ($4,739,868, grade D); American Nitrile LLC ($3,303,561, grade C); ALTIVIA Corporation ($3,100,000, grade C). Together the C and D graded small parents carry $55,849,777 of the $158,102,224 in the small column. The worst case already reassigns all of them, but the largest deserves a sentence of its own in the post.

**The small side is not outlier-driven,** which is the reassuring half: the largest small parent is Ohio-West Virginia Excavating Co. (Dennis Hendershot and Roger Lewis) at $4,739,868, 3.0% of small dollars.

**Two denominators, on purpose.** The size and home-state shares run on dollars net of the 33 reversed payments ($1,171,884,901). The conditions shares in `data/grant_conditions.csv` run on positive payments only ($1,197,924,989), because a reversal has no program to label. The post must say which denominator each number uses.

## Parents merged as the same company written two ways

Merged only where the normalized name, size bucket, home state and class all agree, so a real disagreement is never papered over.

- American Trailer World Corp.  <=  AMERICAN TRAILER WORLD CORP
- Charles River Laboratories International, Inc.  <=  CHARLES RIVER LABORATORIES INC
- Conagra Brands, Inc.  <=  CONAGRA BRANDS
- Custom Glass Solutions LLC  <=  Custom Glass Solutions
- Discount Drug Mart, Inc.  <=  DISCOUNT DRUG MART INC
- Faxon Machining, Inc.  <=  FAXON MACHINING INC
- Howmet Aerospace Inc.  <=  HOWMET AEROSPACE INC
- Hynes Industries, Inc.  <=  Hynes Industries Inc.
- Keller Logistics Group, Inc.  <=  Keller Logistics Group
- Lincoln Electric Holdings, Inc.  <=  Lincoln Electric Holdings
- McKesson Corporation  <=  MCKESSON CORPORATION
- Park-Ohio Holdings Corp.  <=  Park-Ohio Holdings Corp
- Phillips Meat Processing LLC  <=  PHILLIPS MEAT PROCESSING LLC
- ProVia, LLC  <=  ProVia
- Total Quality Logistics, LLC  <=  TOTAL QUALITY LOGISTICS LLC

### Same normalized name, left separate because an attribute disagrees

Each of these is worth one look before publishing: either they are genuinely different entities, or one of the two records is wrong.

- Griffon Corporation [5000+, NY, business, $300,000] | Griffon Holdings LLC [<100, OH, business, $166,568]
- TEAM, Inc. [5000+, TX, business, $300,000] | THE AKA TEAM INC [<100, OH, business, $50,000]
