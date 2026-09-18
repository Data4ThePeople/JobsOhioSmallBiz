# Tie-out

Every number below is recomputed from `data/grants_raw.csv` and `data/parents.csv` by `scripts/09_analyze.py`.

- Schedule I rows: 2,038; distinct recipients: 1,515; parents: 1,505; FY2014 to FY2024; cash $1,171,884,901
- Parents with a researched classification: 40 carrying $505,640,471 (43.1% of dollars)

## By recipient class (all parents)

- business: 1,383 parents, $913,411,996 (77.9%)
- university: 11 parents, $95,233,751 (8.1%)
- hospital: 7 parents, $72,635,725 (6.2%)
- site_development: 43 parents, $37,423,365 (3.2%)
- government: 36 parents, $32,196,187 (2.7%)
- nonprofit: 25 parents, $20,983,877 (1.8%)

## Businesses only

- Cutoff 100 employees: parents small 0.2%, large 1.8%, unknown 98.0%; dollars small 0.2%, large 37.6%, unknown 62.2%
- Cutoff 500 employees: parents small 0.6%, large 1.4%, unknown 98.0%; dollars small 0.6%, large 37.2%, unknown 62.2%
- Cutoff 5000 employees: parents small 0.9%, large 1.1%, unknown 98.0%; dollars small 2.0%, large 35.8%, unknown 62.2%
- Home state: parents Ohio 1.0%, other 1.0%, unknown 98.0%; dollars Ohio 8.3%, other 29.5%, unknown 62.2%
- Worst case: dollars to large at least 32.5%; parents small at least 0.4%
- Two-by-two (dollars): large|ohio 7.7%, large|other 29.5%, small|ohio 0.6%, unknown|unknown 62.2%

## All recipients

- Cutoff 100 employees: parents small 0.5%, large 2.2%, unknown 97.3%; dollars small 1.5%, large 41.6%, unknown 56.9%
- Cutoff 500 employees: parents small 0.8%, large 1.9%, unknown 97.3%; dollars small 1.8%, large 41.3%, unknown 56.9%
- Cutoff 5000 employees: parents small 1.3%, large 1.4%, unknown 97.3%; dollars small 4.2%, large 38.9%, unknown 56.9%
- Home state: parents Ohio 1.5%, other 1.1%, unknown 97.3%; dollars Ohio 18.8%, other 24.3%, unknown 56.9%
- Worst case: dollars to large at least 36.4%; parents small at least 0.5%
- Two-by-two (dollars): large|ohio 18.3%, large|other 23.0%, small|ohio 0.5%, small|other 1.3%, unknown|unknown 56.9%
