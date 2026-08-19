"""Generate the complete descriptive PS003 table from the validated summary."""

from pathlib import Path
import csv
import math


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "evidence" / "PS003" / "normalized" / "validated_jdk_summary.csv"
TARGET = ROOT / "results" / "tables" / "ps003_jdk_analysis.csv"
T_CRITICAL_DF2 = 4.3026527299


def main() -> None:
    source_rows = list(csv.DictReader(SOURCE.open(encoding="utf-8-sig", newline="")))
    rows = []
    for row in source_rows:
        values = list(row.values())
        n = int(values[1])
        mean = float(values[2])
        sd = float(values[4])
        margin = T_CRITICAL_DF2 * sd / math.sqrt(n)
        rows.append({
            "jdk": row["JDK"], "n": n, "mean_ratio_x": mean,
            "median_ratio_x": float(values[3]), "sd_ratio_x": sd,
            "cv_percent": float(values[5]), "min_ratio_x": float(values[6]),
            "max_ratio_x": float(values[7]), "ci95_low": mean - margin,
            "ci95_high": mean + margin, "ci_method": "two-sided t interval, df=2",
            "source_file": "evidence/PS003/normalized/validated_jdk_summary.csv",
        })
    with TARGET.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} validated descriptive rows to {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
