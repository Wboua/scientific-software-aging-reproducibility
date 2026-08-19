"""Build the confounder-aware PS008 presentation table from normalized rows."""

from pathlib import Path
import csv


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "evidence" / "PS008" / "normalized" / "selected_results.csv"
TARGET = ROOT / "results" / "tables" / "ps008_configuration_comparison.csv"
LABELS = {
    "PS008-CURRENT": "Current reconstructed configuration",
    "PS008-HISTORICAL": "Historical reconstructed configuration",
}


def main() -> None:
    rows = list(csv.DictReader(SOURCE.open(encoding="utf-8-sig", newline="")))
    output = []
    for row in rows:
        output.append({
            "case_id": row["case_id"],
            "execution_id": row["execution_id"],
            "configuration_label": LABELS[row["execution_id"]],
            "metric": row["metric"], "value": row["value"], "unit": row["unit"],
            "aggregation": row["aggregation"], "n": row["n"],
            "source_file": row["source_file"], "source_locator": row["source_locator"],
            "label": row["label"], "status": row["status"],
            "confounding_note": "Do not attribute differences causally: code revision, submodules, hardware, compiler, OS, dependencies, build configuration, tuning, repetitions, and background conditions are not jointly controlled.",
        })
    with TARGET.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    print(f"Wrote {len(output)} rows to {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
