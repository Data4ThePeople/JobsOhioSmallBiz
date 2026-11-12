# Tie-out

Every number below is recomputed from `data/grants_raw.csv` and `data/parents.csv` by `scripts/09_analyze.py`.

- Schedule I rows: 2,038; distinct recipients: 1,515; parents: 1,452; FY2014 to FY2024; cash $1,171,884,901
- Reversed payments (negative Schedule I rows): 33 rows, $-26,040,088; parents netting to zero or less, not counted as recipients: 16 (net $-757,252)
- Parents counted (net payment above zero): 1,452; with a classification: 1,452, carrying $1,172,642,153 of the $1,172,642,153 they were paid on net (100.0%)

## By recipient class (all parents)

- business: 1,235 parents, $821,750,416 (70.1%)
- site_development: 122 parents, $107,903,270 (9.2%)
- university: 11 parents, $95,233,751 (8.1%)
- hospital: 7 parents, $77,635,725 (6.6%)
- nonprofit: 37 parents, $41,160,782 (3.5%)
- government: 40 parents, $28,958,209 (2.5%)

## Businesses only

- Cutoff 100 employees: parents small 38.7%, large 61.3%, unknown 0.0%; dollars small 7.6%, large 92.4%, unknown 0.0%
- Cutoff 500 employees: parents small 60.2%, large 39.8%, unknown 0.0%; dollars small 18.1%, large 81.9%, unknown 0.0%
- Cutoff 5000 employees: parents small 80.7%, large 19.3%, unknown 0.0%; dollars small 34.7%, large 65.3%, unknown 0.0%
- Home state: parents Ohio 62.8%, other 37.2%, unknown 0.0%; dollars Ohio 35.6%, other 64.4%, unknown 0.0%
- Worst case: dollars to large at least 61.4%; parents small at least 45.3%
- Two-by-two (dollars): large|ohio 20.3%, large|other 61.6%, small|ohio 15.3%, small|other 2.7%

## All recipients

- Cutoff 100 employees: parents small 40.4%, large 55.0%, unknown 4.6%; dollars small 15.7%, large 82.8%, unknown 1.5%
- Cutoff 500 employees: parents small 60.3%, large 35.1%, unknown 4.6%; dollars small 25.7%, large 72.8%, unknown 1.5%
- Cutoff 5000 employees: parents small 78.2%, large 17.1%, unknown 4.6%; dollars small 39.5%, large 59.0%, unknown 1.5%
- Home state: parents Ohio 66.6%, other 33.4%, unknown 0.0%; dollars Ohio 51.6%, other 48.4%, unknown 0.0%
- Worst case: dollars to large at least 54.5%; parents small at least 40.2%
- Two-by-two (dollars): large|ohio 29.5%, large|other 43.4%, small|ohio 20.6%, small|other 5.0%, unknown|ohio 1.5%

## Conflicts between recipients of one parent

Resolved against the finding, not by read order: the smaller size band, Ohio, and out of the `business` denominator.

- bucket: 100-499 vs 500-4999 (SFG GEIS SHALERSVILLE LLC)
- bucket: 500-4999 vs 100-499 (NP FTC LLC)
- class: business vs hospital (THE RESEARCH INSTITUTE AT NATIONWIDE CHILDREN'S HOSPITAL)
- class: site_development vs business (TRACTOR SUPPLY COMPANY)

## Sensitivities

These are not errors. They are the places the headline is most exposed, computed so the post can state them before a reader finds them.

**The class boundary, and it is the largest one.** 100 parents carrying $115,396,967 were classed out of `business` by hand after the automatic classifier called them businesses, mostly into site_development: project LLCs and industrial developers rather than operating companies. 96 of them, carrying $97,096,967, would have scored small. Recompute the headline on the automatic class instead and the business universe goes 1,235 parents / $821,750,416 to 1,332 / $935,784,008, and the small share of business dollars goes **18.1% to 26.2%**. The published worst case does not cover this: it reassigns size inside the business set and never reconsiders the class boundary. The post should state this figure itself rather than wait to be asked why a company that builds and leases industrial buildings is not a small business.

**One payment carries the home-state finding.** Intel Corporation alone is $124,422,793, 15.1% of all business dollars. The top three (Intel Corporation, Ultium Cells LLC (50/50 join, The Sherwin-Williams Company) are 26.3%. Leave Intel Corporation out and Ohio's share of business dollars goes **35.6% to 42.0%**, and the large share goes 81.9% to 78.7%. Its classification is not in doubt, so this is leverage rather than error. Name it beside the number.

**The small side is not outlier-driven,** which is the reassuring half: the largest small parent is Novagard Solutions, Inc. at $3,876,963, 2.6% of small dollars.

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
