# Tie-out

Every number below is recomputed from `data/grants_raw.csv` and `data/parents.csv` by `scripts/09_analyze.py`.

- Schedule I rows: 2,038; distinct recipients: 1,515; parents: 1,456; FY2014 to FY2024; cash $1,171,884,901
- Reversed payments (negative Schedule I rows): 33 rows, $-26,040,088; parents netting to zero or less, not counted as recipients: 17 (net $-807,252)
- Parents counted (net payment above zero): 1,456; with a classification: 1,456, carrying $1,172,692,153 of the $1,172,692,153 they were paid on net (100.0%)

## By recipient class (all parents)

- business: 1,248 parents, $832,450,416 (71.0%)
- site_development: 114 parents, $110,753,270 (9.5%)
- university: 11 parents, $95,233,751 (8.1%)
- hospital: 6 parents, $64,135,725 (5.5%)
- nonprofit: 37 parents, $41,160,782 (3.5%)
- government: 40 parents, $28,958,209 (2.5%)

## Businesses only

- Cutoff 100 employees: parents small 39.8%, large 60.2%, unknown 0.0%; dollars small 8.1%, large 91.9%, unknown 0.0%
- Cutoff 500 employees: parents small 61.1%, large 38.9%, unknown 0.0%; dollars small 18.4%, large 81.6%, unknown 0.0%
- Cutoff 5000 employees: parents small 80.8%, large 19.2%, unknown 0.0%; dollars small 34.4%, large 65.6%, unknown 0.0%
- Home state: parents Ohio 63.7%, other 36.3%, unknown 0.0%; dollars Ohio 37.2%, other 62.8%, unknown 0.0%
- Worst case: dollars to large at least 62.1%; parents small at least 45.4%
- Two-by-two (dollars): large|ohio 21.4%, large|other 60.2%, small|ohio 15.7%, small|other 2.6%

## All recipients

- Cutoff 100 employees: parents small 40.9%, large 54.5%, unknown 4.6%; dollars small 16.2%, large 82.3%, unknown 1.5%
- Cutoff 500 employees: parents small 60.7%, large 34.7%, unknown 4.6%; dollars small 25.9%, large 72.5%, unknown 1.5%
- Cutoff 5000 employees: parents small 78.2%, large 17.2%, unknown 4.6%; dollars small 39.6%, large 58.9%, unknown 1.5%
- Home state: parents Ohio 67.3%, other 32.7%, unknown 0.0%; dollars Ohio 52.1%, other 47.9%, unknown 0.0%
- Worst case: dollars to large at least 55.9%; parents small at least 40.6%
- Two-by-two (dollars): large|ohio 29.3%, large|other 43.2%, small|ohio 21.3%, small|other 4.6%, unknown|ohio 1.5%

## Conflicts between recipients of one parent

- bucket: 100-499 vs 500-4999 (SFG GEIS SHALERSVILLE LLC)
- bucket: 500-4999 vs 100-499 (NP FTC LLC)
- bucket: <100 vs 100-499 (CMG STRATEGY CO LLC)
- hq: OH vs CA (COOKE BUILDING LLC)
- hq: OH vs CO (CMG STRATEGY CO LLC)
- hq: OH vs NJ (SR 29 WEST JEFF LLC)
- hq: OH vs NY (RUDOLPH DEVELOPMENT LLC)
