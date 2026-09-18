# Tie-out

Every number below is recomputed from `data/grants_raw.csv` and `data/parents.csv` by `scripts/09_analyze.py`.

- Schedule I rows: 2,038; distinct recipients: 1,515; parents: 1,500; FY2014 to FY2024; cash $1,171,884,901
- Parents with a researched classification: 823 carrying $971,620,927 (82.9% of dollars)

## By recipient class (all parents)

- business: 1,360 parents, $872,569,737 (74.5%)
- university: 11 parents, $95,233,751 (8.1%)
- site_development: 59 parents, $74,075,844 (6.3%)
- hospital: 6 parents, $64,135,725 (5.5%)
- nonprofit: 29 parents, $36,657,831 (3.1%)
- government: 35 parents, $29,212,013 (2.5%)

## Businesses only

- Cutoff 100 employees: parents small 27.1%, large 23.8%, unknown 49.0%; dollars small 5.2%, large 72.4%, unknown 22.4%
- Cutoff 500 employees: parents small 37.7%, large 13.2%, unknown 49.0%; dollars small 11.4%, large 66.2%, unknown 22.4%
- Cutoff 5000 employees: parents small 44.6%, large 6.4%, unknown 49.0%; dollars small 21.7%, large 55.8%, unknown 22.4%
- Home state: parents Ohio 39.9%, other 11.1%, unknown 49.0%; dollars Ohio 28.0%, other 49.6%, unknown 22.4%
- Worst case: dollars to large at least 58.5%; parents small at least 37.0%
- Two-by-two (dollars): large|ohio 17.5%, large|other 48.7%, small|ohio 10.5%, small|other 0.9%, unknown|unknown 22.4%

## All recipients

- Cutoff 100 employees: parents small 26.8%, large 23.1%, unknown 50.1%; dollars small 11.2%, large 69.7%, unknown 19.1%
- Cutoff 500 employees: parents small 36.8%, large 13.1%, unknown 50.1%; dollars small 17.5%, large 63.4%, unknown 19.1%
- Cutoff 5000 employees: parents small 43.5%, large 6.4%, unknown 50.1%; dollars small 27.3%, large 53.6%, unknown 19.1%
- Home state: parents Ohio 44.3%, other 10.5%, unknown 45.1%; dollars Ohio 43.6%, other 39.3%, unknown 17.1%
- Worst case: dollars to large at least 55.1%; parents small at least 34.5%
- Two-by-two (dollars): large|ohio 27.0%, large|other 36.4%, small|ohio 14.6%, small|other 3.0%, unknown|ohio 2.0%, unknown|unknown 17.1%
