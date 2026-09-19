# Tie-out

Every number below is recomputed from `data/grants_raw.csv` and `data/parents.csv` by `scripts/09_analyze.py`.

- Schedule I rows: 2,038; distinct recipients: 1,515; parents: 1,463; FY2014 to FY2024; cash $1,171,884,901
- Reversed payments (negative Schedule I rows): 33 rows, $-26,040,088; parents netting to zero or less, not counted as recipients: 17 (net $-807,252)
- Parents with a researched classification: 1,310 carrying $1,165,391,842 (99.4% of dollars)

## By recipient class (all parents)

- business: 1,264 parents, $833,351,538 (71.1%)
- site_development: 109 parents, $109,980,448 (9.4%)
- university: 11 parents, $95,233,751 (8.1%)
- hospital: 6 parents, $64,135,725 (5.5%)
- nonprofit: 34 parents, $41,054,482 (3.5%)
- government: 39 parents, $28,936,209 (2.5%)

## Businesses only

- Cutoff 100 employees: parents small 35.9%, large 52.1%, unknown 11.9%; dollars small 8.3%, large 90.8%, unknown 0.9%
- Cutoff 500 employees: parents small 55.6%, large 32.4%, unknown 11.9%; dollars small 19.0%, large 80.1%, unknown 0.9%
- Cutoff 5000 employees: parents small 71.5%, large 16.5%, unknown 11.9%; dollars small 34.2%, large 65.0%, unknown 0.9%
- Home state: parents Ohio 58.6%, other 29.4%, unknown 11.9%; dollars Ohio 37.7%, other 61.4%, unknown 0.9%
- Worst case: dollars to large at least 61.5%; parents small at least 46.2%
- Two-by-two (dollars): large|ohio 21.3%, large|other 58.8%, small|ohio 16.4%, small|other 2.6%, unknown|unknown 0.9%

## All recipients

- Cutoff 100 employees: parents small 37.0%, large 47.8%, unknown 15.2%; dollars small 16.3%, large 81.6%, unknown 2.2%
- Cutoff 500 employees: parents small 55.4%, large 29.4%, unknown 15.2%; dollars small 26.3%, large 71.5%, unknown 2.2%
- Cutoff 5000 employees: parents small 69.8%, large 15.0%, unknown 15.2%; dollars small 39.3%, large 58.5%, unknown 2.2%
- Home state: parents Ohio 62.8%, other 26.7%, unknown 10.5%; dollars Ohio 52.5%, other 46.9%, unknown 0.6%
- Worst case: dollars to large at least 55.6%; parents small at least 41.3%
- Two-by-two (dollars): large|ohio 29.2%, large|other 42.3%, small|ohio 21.7%, small|other 4.6%, unknown|ohio 1.5%, unknown|unknown 0.6%

## Conflicts between recipients of one parent

- bucket: 100-499 vs 500-4999 (SFG GEIS SHALERSVILLE LLC)
- bucket: 500-4999 vs 100-499 (NP FTC LLC)
- bucket: <100 vs 100-499 (CMG STRATEGY CO LLC)
- hq: OH vs CA (COOKE BUILDING LLC)
- hq: OH vs CO (CMG STRATEGY CO LLC)
- hq: OH vs NJ (SR 29 WEST JEFF LLC)
- hq: OH vs NY (RUDOLPH DEVELOPMENT LLC)
