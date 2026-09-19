# Tie-out

Every number below is recomputed from `data/grants_raw.csv` and `data/parents.csv` by `scripts/09_analyze.py`.

- Schedule I rows: 2,038; distinct recipients: 1,515; parents: 1,482; FY2014 to FY2024; cash $1,171,884,901
- Parents with a researched classification: 1,199 carrying $1,152,554,929 (98.4% of dollars)

## By recipient class (all parents)

- business: 1,290 parents, $834,510,113 (71.2%)
- site_development: 105 parents, $109,418,084 (9.3%)
- university: 11 parents, $95,233,751 (8.1%)
- hospital: 6 parents, $64,135,725 (5.5%)
- nonprofit: 33 parents, $39,854,482 (3.4%)
- government: 37 parents, $28,732,746 (2.5%)

## Businesses only

- Cutoff 100 employees: parents small 33.3%, large 45.0%, unknown 21.7%; dollars small 8.1%, large 89.6%, unknown 2.3%
- Cutoff 500 employees: parents small 50.5%, large 27.8%, unknown 21.7%; dollars small 18.4%, large 79.3%, unknown 2.3%
- Cutoff 5000 employees: parents small 64.0%, large 14.3%, unknown 21.7%; dollars small 33.2%, large 64.5%, unknown 2.3%
- Home state: parents Ohio 53.8%, other 24.5%, unknown 21.7%; dollars Ohio 37.1%, other 60.6%, unknown 2.3%
- Worst case: dollars to large at least 61.1%; parents small at least 43.9%
- Two-by-two (dollars): large|ohio 21.1%, large|other 58.2%, small|ohio 16.0%, small|other 2.4%, unknown|unknown 2.3%

## All recipients

- Cutoff 100 employees: parents small 34.4%, large 41.8%, unknown 23.8%; dollars small 16.0%, large 80.9%, unknown 3.1%
- Cutoff 500 employees: parents small 50.7%, large 25.5%, unknown 23.8%; dollars small 25.8%, large 71.1%, unknown 3.1%
- Cutoff 5000 employees: parents small 63.0%, large 13.2%, unknown 23.8%; dollars small 38.6%, large 58.3%, unknown 3.1%
- Home state: parents Ohio 58.4%, other 22.5%, unknown 19.1%; dollars Ohio 52.0%, other 46.4%, unknown 1.6%
- Worst case: dollars to large at least 55.3%; parents small at least 39.5%
- Two-by-two (dollars): large|ohio 29.1%, large|other 42.0%, small|ohio 21.4%, small|other 4.4%, unknown|ohio 1.5%, unknown|unknown 1.6%

## Conflicts between recipients of one parent

- bucket: 100-499 vs 500-4999 (SFG GEIS SHALERSVILLE LLC)
- bucket: 500-4999 vs 100-499 (NP FTC LLC)
- bucket: <100 vs 100-499 (CMG STRATEGY CO LLC)
- hq: OH vs CA (COOKE BUILDING LLC)
- hq: OH vs CO (CMG STRATEGY CO LLC)
- hq: OH vs NJ (SR 29 WEST JEFF LLC)
- hq: OH vs NY (RUDOLPH DEVELOPMENT LLC)
