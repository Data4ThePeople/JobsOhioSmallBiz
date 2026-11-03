# Tie-out

Every number below is recomputed from `data/grants_raw.csv` and `data/parents.csv` by `scripts/09_analyze.py`.

- Schedule I rows: 2,038; distinct recipients: 1,515; parents: 1,466; FY2014 to FY2024; cash $1,171,884,901
- Reversed payments (negative Schedule I rows): 33 rows, $-26,040,088; parents netting to zero or less, not counted as recipients: 17 (net $-807,252)
- Parents counted (net payment above zero): 1,466; with a classification: 1,466, carrying $1,172,692,153 of the $1,172,692,153 they were paid on net (100.0%)

## By recipient class (all parents)

- business: 1,249 parents, $832,950,416 (71.1%)
- site_development: 123 parents, $110,253,270 (9.4%)
- university: 11 parents, $95,233,751 (8.1%)
- hospital: 6 parents, $64,135,725 (5.5%)
- nonprofit: 37 parents, $41,160,782 (3.5%)
- government: 40 parents, $28,958,209 (2.5%)

## Businesses only

- Cutoff 100 employees: parents small 38.4%, large 61.6%, unknown 0.0%; dollars small 7.5%, large 92.5%, unknown 0.0%
- Cutoff 500 employees: parents small 59.7%, large 40.3%, unknown 0.0%; dollars small 17.8%, large 82.2%, unknown 0.0%
- Cutoff 5000 employees: parents small 80.4%, large 19.6%, unknown 0.0%; dollars small 34.2%, large 65.8%, unknown 0.0%
- Home state: parents Ohio 62.9%, other 37.1%, unknown 0.0%; dollars Ohio 36.8%, other 63.2%, unknown 0.0%
- Worst case: dollars to large at least 62.4%; parents small at least 44.9%
- Two-by-two (dollars): large|ohio 21.7%, large|other 60.5%, small|ohio 15.1%, small|other 2.7%

## All recipients

- Cutoff 100 employees: parents small 40.0%, large 55.4%, unknown 4.6%; dollars small 15.7%, large 82.8%, unknown 1.5%
- Cutoff 500 employees: parents small 59.8%, large 35.6%, unknown 4.6%; dollars small 25.7%, large 72.8%, unknown 1.5%
- Cutoff 5000 employees: parents small 78.0%, large 17.5%, unknown 4.6%; dollars small 39.5%, large 59.0%, unknown 1.5%
- Home state: parents Ohio 66.6%, other 33.4%, unknown 0.0%; dollars Ohio 51.6%, other 48.4%, unknown 0.0%
- Worst case: dollars to large at least 56.0%; parents small at least 40.0%
- Two-by-two (dollars): large|ohio 29.5%, large|other 43.4%, small|ohio 20.6%, small|other 5.0%, unknown|ohio 1.5%

## Conflicts between recipients of one parent

- bucket: 100-499 vs 500-4999 (SFG GEIS SHALERSVILLE LLC)
- bucket: 500-4999 vs 100-499 (NP FTC LLC)
