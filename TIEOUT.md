# Tie-out

Every number below is recomputed from `data/grants_raw.csv` and `data/parents.csv` by `scripts/09_analyze.py`.

- Schedule I rows: 2,415; distinct recipients: 1,789; parents: 1,719; FY2014 to FY2025; cash $1,345,318,862
- Reversed payments (negative Schedule I rows): 33 rows, $-26,040,088; parents netting to zero or less, not counted as recipients: 16 (net $-757,252)
- Parents counted (net payment above zero): 1,719; with a classification: 1,719, carrying $1,346,076,114 of the $1,346,076,114 they were paid on net (100.0%)

## By recipient class (all parents)

- business: 1,487 parents, $956,764,828 (71.1%)
- site_development: 131 parents, $109,515,340 (8.1%)
- university: 12 parents, $104,248,751 (7.7%)
- hospital: 7 parents, $100,785,000 (7.5%)
- nonprofit: 39 parents, $42,885,073 (3.2%)
- government: 43 parents, $31,877,122 (2.4%)

## Businesses only

- Cutoff 100 employees: parents small 43.8%, large 56.2%, unknown 0.0%; dollars small 7.8%, large 92.2%, unknown 0.0%
- Cutoff 500 employees: parents small 64.0%, large 36.0%, unknown 0.0%; dollars small 18.9%, large 81.1%, unknown 0.0%
- Cutoff 5000 employees: parents small 82.2%, large 17.8%, unknown 0.0%; dollars small 35.4%, large 64.6%, unknown 0.0%
- Home state: parents Ohio 65.6%, other 34.4%, unknown 0.0%; dollars Ohio 36.3%, other 63.7%, unknown 0.0%
- Worst case: dollars to large at least 58.2%; parents small at least 47.3%
- Two-by-two (dollars): large|ohio 20.3%, large|other 60.8%, small|ohio 16.0%, small|other 2.9%

## All recipients

- Cutoff 100 employees: parents small 45.1%, large 51.1%, unknown 3.7%; dollars small 15.3%, large 83.4%, unknown 1.4%
- Cutoff 500 employees: parents small 63.9%, large 32.4%, unknown 3.7%; dollars small 25.2%, large 73.5%, unknown 1.4%
- Cutoff 5000 employees: parents small 80.3%, large 15.9%, unknown 3.7%; dollars small 39.0%, large 59.6%, unknown 1.4%
- Home state: parents Ohio 68.5%, other 31.5%, unknown 0.0%; dollars Ohio 51.7%, other 48.3%, unknown 0.0%
- Worst case: dollars to large at least 53.7%; parents small at least 42.9%
- Two-by-two (dollars): large|ohio 30.0%, large|other 43.4%, small|ohio 20.3%, small|other 4.9%, unknown|ohio 1.4%

## Conflicts between recipients of one parent

Resolved against the finding, not by read order: the smaller size band, Ohio, and out of the `business` denominator.

- bucket: 100-499 vs 500-4999 (SFG GEIS SHALERSVILLE LLC)
- bucket: 500-4999 vs 100-499 (NP FTC LLC)
- class: business vs hospital (THE RESEARCH INSTITUTE AT NATIONWIDE CHILDREN'S HOSPITAL)
- class: site_development vs business (TRACTOR SUPPLY COMPANY)
- hq: CA vs OH (AVERY DENNISION CORPORATION)

## Sensitivities

These are not errors. They are the places the headline is most exposed, computed so the post can state them before a reader finds them.

**The class boundary, and it is the largest one.** 93 parents carrying $108,342,324 were classed out of `business` by hand after the automatic classifier called them businesses, mostly into site_development: project LLCs and industrial developers rather than operating companies. 90 of them, carrying $91,042,324, would have scored small. Recompute the headline on the automatic class instead and the business universe goes 1,487 parents / $956,764,828 to 1,573 / $1,062,867,177, and the small share of business dollars goes **18.9% to 25.5%**. The published worst case does not cover this: it reassigns size inside the business set and never reconsiders the class boundary. The post should state this figure itself rather than wait to be asked why a company that builds and leases industrial buildings is not a small business.

**One payment carries the home-state finding.** Intel Corporation alone is $125,415,416, 13.1% of all business dollars. The top three (Intel Corporation, Honda Motor Co., Ltd., Ultium Cells LLC (50/50 join) are 23.8%. Leave Intel Corporation out and Ohio's share of business dollars goes **36.3% to 41.8%**, and the large share goes 81.1% to 78.3%. Its classification is not in doubt, so this is leverage rather than error. Name it beside the number.

**The small share leans on a few weakly-graded size bands.** Ohio-West Virginia Excavating Co. (Dennis Hend ($4,739,868, grade D); American Nitrile LLC ($3,327,345, grade C); ALTIVIA Corporation ($3,100,000, grade C). Together the C and D graded small parents carry $64,171,332 of the $180,802,311 in the small column. The worst case already reassigns all of them, but the largest deserves a sentence of its own in the post.

**The small side is not outlier-driven,** which is the reassuring half: the largest small parent is Ohio-West Virginia Excavating Co. (Dennis Hendershot and Roger Lewis) at $4,739,868, 2.6% of small dollars.

**Two denominators, on purpose.** The size and home-state shares run on dollars net of the 33 reversed payments ($1,345,318,862). The conditions shares in `data/grant_conditions.csv` run on positive payments only ($1,371,358,950), because a reversal has no program to label. The post must say which denominator each number uses.

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
- King's Command Foods LLC [500-4999, WI, business, $250,000] | King's Command Foods, LLC [500-4999, WA, business, $425,000]
- NorthPoint Development [100-499, MO, site_development, $1,900,000] | NorthPoint Development LLC [500-4999, MO, site_development, $800,000]
- TEAM, Inc. [5000+, TX, business, $300,000] | THE AKA TEAM INC [<100, OH, business, $50,000]
