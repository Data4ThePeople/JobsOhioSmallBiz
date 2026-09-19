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

- Cutoff 100 employees: parents small 39.4%, large 60.6%, unknown 0.0%; dollars small 8.0%, large 92.0%, unknown 0.0%
- Cutoff 500 employees: parents small 60.1%, large 39.9%, unknown 0.0%; dollars small 18.1%, large 81.9%, unknown 0.0%
- Cutoff 5000 employees: parents small 80.5%, large 19.5%, unknown 0.0%; dollars small 34.3%, large 65.7%, unknown 0.0%
- Home state: parents Ohio 62.7%, other 37.3%, unknown 0.0%; dollars Ohio 36.9%, other 63.1%, unknown 0.0%
- Worst case: dollars to large at least 62.3%; parents small at least 45.0%
- Two-by-two (dollars): large|ohio 21.5%, large|other 60.4%, small|ohio 15.3%, small|other 2.7%

## All recipients

- Cutoff 100 employees: parents small 40.6%, large 54.8%, unknown 4.6%; dollars small 16.1%, large 82.4%, unknown 1.5%
- Cutoff 500 employees: parents small 59.8%, large 35.6%, unknown 4.6%; dollars small 25.7%, large 72.8%, unknown 1.5%
- Cutoff 5000 employees: parents small 78.0%, large 17.4%, unknown 4.6%; dollars small 39.5%, large 59.0%, unknown 1.5%
- Home state: parents Ohio 66.5%, other 33.5%, unknown 0.0%; dollars Ohio 51.9%, other 48.1%, unknown 0.0%
- Worst case: dollars to large at least 56.1%; parents small at least 40.3%
- Two-by-two (dollars): large|ohio 29.4%, large|other 43.4%, small|ohio 21.0%, small|other 4.7%, unknown|ohio 1.5%

## Conflicts between recipients of one parent

- bucket: 100-499 vs 500-4999 (SFG GEIS SHALERSVILLE LLC)
- bucket: 500-4999 vs 100-499 (NP FTC LLC)
- bucket: <100 vs 100-499 (CMG STRATEGY CO LLC)
- hq: OH vs CA (COOKE BUILDING LLC)
- hq: OH vs CO (CMG STRATEGY CO LLC)
- hq: OH vs NJ (SR 29 WEST JEFF LLC)
- hq: OH vs NY (RUDOLPH DEVELOPMENT LLC)
