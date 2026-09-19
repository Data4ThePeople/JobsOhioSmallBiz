# Tie-out

Every number below is recomputed from `data/grants_raw.csv` and `data/parents.csv` by `scripts/09_analyze.py`.

- Schedule I rows: 2,038; distinct recipients: 1,515; parents: 1,487; FY2014 to FY2024; cash $1,171,884,901
- Parents with a researched classification: 1,008 carrying $1,108,576,277 (94.6% of dollars)

## By recipient class (all parents)

- business: 1,315 parents, $839,470,847 (71.6%)
- site_development: 87 parents, $104,764,083 (8.9%)
- university: 11 parents, $95,233,751 (8.1%)
- hospital: 6 parents, $64,135,725 (5.5%)
- nonprofit: 33 parents, $39,978,482 (3.4%)
- government: 35 parents, $28,302,013 (2.4%)

## Businesses only

- Cutoff 100 employees: parents small 29.8%, large 34.1%, unknown 36.1%; dollars small 7.0%, large 85.5%, unknown 7.5%
- Cutoff 500 employees: parents small 43.3%, large 20.5%, unknown 36.1%; dollars small 16.2%, large 76.3%, unknown 7.5%
- Cutoff 5000 employees: parents small 53.3%, large 10.6%, unknown 36.1%; dollars small 29.7%, large 62.8%, unknown 7.5%
- Home state: parents Ohio 46.5%, other 17.4%, unknown 36.1%; dollars Ohio 34.6%, other 57.9%, unknown 7.5%
- Worst case: dollars to large at least 67.4%; parents small at least 40.4%
- Two-by-two (dollars): large|ohio 20.3%, large|other 56.0%, small|ohio 14.3%, small|other 1.9%, unknown|unknown 7.5%

## All recipients

- Cutoff 100 employees: parents small 30.6%, large 32.5%, unknown 36.9%; dollars small 14.9%, large 78.2%, unknown 6.9%
- Cutoff 500 employees: parents small 43.6%, large 19.5%, unknown 36.9%; dollars small 23.8%, large 69.3%, unknown 6.9%
- Cutoff 5000 employees: parents small 53.0%, large 10.1%, unknown 36.9%; dollars small 35.8%, large 57.3%, unknown 6.9%
- Home state: parents Ohio 51.3%, other 16.5%, unknown 32.2%; dollars Ohio 49.9%, other 44.7%, unknown 5.4%
- Worst case: dollars to large at least 60.3%; parents small at least 37.0%
- Two-by-two (dollars): large|ohio 28.6%, large|other 40.7%, small|ohio 19.8%, small|other 4.0%, unknown|ohio 1.5%, unknown|unknown 5.4%

## Conflicts between recipients of one parent

- bucket: 100-499 vs 500-4999 (SFG GEIS SHALERSVILLE LLC)
- bucket: 500-4999 vs 100-499 (NP FTC LLC)
- bucket: <100 vs 100-499 (CMG STRATEGY CO LLC)
- hq: OH vs CA (COOKE BUILDING LLC)
- hq: OH vs CO (CMG STRATEGY CO LLC)
- hq: OH vs NJ (SR 29 WEST JEFF LLC)
- hq: OH vs NY (RUDOLPH DEVELOPMENT LLC)
