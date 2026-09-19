# Tie-out

Every number below is recomputed from `data/grants_raw.csv` and `data/parents.csv` by `scripts/09_analyze.py`.

- Schedule I rows: 2,038; distinct recipients: 1,515; parents: 1,460; FY2014 to FY2024; cash $1,171,884,901
- Reversed payments (negative Schedule I rows): 33 rows, $-26,040,088; parents netting to zero or less, not counted as recipients: 17 (net $-807,252)
- Parents counted (net payment above zero): 1,460; with a classification: 1,460, carrying $1,172,692,153 of the $1,172,692,153 they were paid on net (100.0%)

## By recipient class (all parents)

- business: 1,255 parents, $833,000,511 (71.1%)
- site_development: 113 parents, $110,243,175 (9.4%)
- university: 11 parents, $95,233,751 (8.1%)
- hospital: 6 parents, $64,135,725 (5.5%)
- nonprofit: 35 parents, $41,120,782 (3.5%)
- government: 40 parents, $28,958,209 (2.5%)

## Businesses only

- Cutoff 100 employees: parents small 41.4%, large 58.6%, unknown 0.0%; dollars small 8.7%, large 91.3%, unknown 0.0%
- Cutoff 500 employees: parents small 63.9%, large 36.1%, unknown 0.0%; dollars small 19.6%, large 80.4%, unknown 0.0%
- Cutoff 5000 employees: parents small 81.9%, large 18.1%, unknown 0.0%; dollars small 34.9%, large 65.1%, unknown 0.0%
- Home state: parents Ohio 66.5%, other 33.5%, unknown 0.0%; dollars Ohio 38.2%, other 61.8%, unknown 0.0%
- Worst case: dollars to large at least 61.5%; parents small at least 49.2%
- Two-by-two (dollars): large|ohio 21.3%, large|other 59.1%, small|ohio 16.9%, small|other 2.7%

## All recipients

- Cutoff 100 employees: parents small 42.0%, large 53.3%, unknown 4.7%; dollars small 16.5%, large 81.9%, unknown 1.5%
- Cutoff 500 employees: parents small 62.9%, large 32.4%, unknown 4.7%; dollars small 26.7%, large 71.7%, unknown 1.5%
- Cutoff 5000 employees: parents small 79.0%, large 16.3%, unknown 4.7%; dollars small 39.9%, large 58.6%, unknown 1.5%
- Home state: parents Ohio 69.8%, other 30.2%, unknown 0.0%; dollars Ohio 52.9%, other 47.1%, unknown 0.0%
- Worst case: dollars to large at least 55.5%; parents small at least 43.8%
- Two-by-two (dollars): large|ohio 29.2%, large|other 42.5%, small|ohio 22.1%, small|other 4.7%, unknown|ohio 1.5%

## Conflicts between recipients of one parent

- bucket: 100-499 vs 500-4999 (SFG GEIS SHALERSVILLE LLC)
- bucket: 500-4999 vs 100-499 (NP FTC LLC)
- bucket: <100 vs 100-499 (CMG STRATEGY CO LLC)
- hq: OH vs CA (COOKE BUILDING LLC)
- hq: OH vs CO (CMG STRATEGY CO LLC)
- hq: OH vs NJ (SR 29 WEST JEFF LLC)
- hq: OH vs NY (RUDOLPH DEVELOPMENT LLC)
