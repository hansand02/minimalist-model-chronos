"""Print the main metrics per dataset and their unweighted mean: python summary.py <metrics.csv>..."""

import csv
import sys
from pathlib import Path

METRICS = ["crps", "crps_log1p", "mae", "coverage_10_90"]

rows = {Path(f).parent.name: next(csv.DictReader(open(f))) for f in sys.argv[1:]}
print(f"{'':<28}" + "".join(f"{m:>16}" for m in METRICS))
for name, row in rows.items():
    print(f"{name:<28}" + "".join(f"{float(row[m]):>16.3f}" for m in METRICS))
if len(rows) > 1:
    means = [sum(float(row[m]) for row in rows.values()) / len(rows) for m in METRICS]
    print(f"{'mean':<28}" + "".join(f"{v:>16.3f}" for v in means))
