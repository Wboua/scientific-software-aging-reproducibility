"""Sensitivity and robustness analyses for the approved ten-case matrix."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "results" / "normalized" / "master_matrix.csv"
TABLES = ROOT / "results" / "tables"
DIMS = ("A", "I", "B", "E", "N", "P")


def write(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    with MATRIX.open(encoding="utf-8-sig", newline="") as handle:
        matrix = list(csv.DictReader(handle))

    sensitivity = []
    for dim in DIMS:
        applicable = [row[dim] for row in matrix if row[dim] != "N/A"]
        observed = [state for state in applicable if state != "UNKNOWN"]
        passed = observed.count("PASS")
        partial = observed.count("PARTIAL")
        unknown = applicable.count("UNKNOWN")
        denominator = len(observed)
        sensitivity.append({
            "dimension": dim,
            "observed_denominator": denominator,
            "strict_pass_n": passed,
            "strict_pass_percent": round(100 * passed / denominator, 1) if denominator else "NA",
            "inclusive_pass_or_partial_n": passed + partial,
            "inclusive_percent": round(100 * (passed + partial) / denominator, 1) if denominator else "NA",
            "unknown_applicable_n": unknown,
            "worst_case_percent_unknown_as_failure": round(100 * passed / len(applicable), 1) if applicable else "NA",
            "best_case_percent_unknown_as_success": round(100 * (passed + unknown) / len(applicable), 1) if applicable else "NA",
        })
    write(TABLES / "classification_sensitivity.csv", sensitivity)

    ordinal = {"FAIL": 0, "PARTIAL": 1, "PASS": 2}
    transitions = []
    for left, right in zip(DIMS, DIMS[1:]):
        eligible = [row for row in matrix if row[left] in ordinal and row[right] in ordinal]
        degraded = [row for row in eligible if ordinal[row[right]] < ordinal[row[left]]]
        transitions.append({
            "transition": f"{left}->{right}",
            "eligible_cases": len(eligible),
            "degraded_cases": len(degraded),
            "degraded_case_ids": ";".join(row["case_id"] for row in degraded),
            "degradation_percent": round(100 * len(degraded) / len(eligible), 1) if eligible else "NA",
        })
    write(TABLES / "chain_transition_robustness.csv", transitions)

    case_rows = []
    for row in matrix:
        comparable = [(left, right) for left, right in zip(DIMS, DIMS[1:]) if row[left] in ordinal and row[right] in ordinal]
        degradations = [f"{left}->{right}" for left, right in comparable if ordinal[row[right]] < ordinal[row[left]]]
        case_rows.append({
            "case_id": row["case_id"],
            "comparable_adjacent_transitions": len(comparable),
            "degradation_count": len(degradations),
            "degradations": ";".join(degradations),
            "supports_independently_degradable_chain": "YES" if degradations else "NO_OBSERVED_DEGRADATION",
        })
    write(TABLES / "case_chain_degradations.csv", case_rows)
    print("Generated classification sensitivity and chain robustness tables")


if __name__ == "__main__":
    main()
