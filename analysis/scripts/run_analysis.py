"""Generate the cross-case analysis, tables, and figures from retained evidence."""

from __future__ import annotations

import csv
import math
import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
NORMALIZED = RESULTS / "normalized"
TABLES = RESULTS / "tables"
FIGURES = RESULTS / "figures"
DIMS = ("A", "I", "B", "E", "N", "P")
STATES = ("PASS", "PARTIAL", "FAIL", "N/A", "UNKNOWN")


def read_metadata(case_id: str) -> dict[str, str]:
    text = (ROOT / "evidence" / case_id / "metadata.yaml").read_text(encoding="utf-8-sig")
    result = {"case_id": case_id}
    for key in ("artifact_name", "repair_level", "evidence_status"):
        match = re.search(rf"^{key}: \"([^\"]*)\"", text, re.MULTILINE)
        if not match:
            raise ValueError(f"Missing {key} in {case_id}")
        result[key] = match.group(1)
    for dim in DIMS:
        match = re.search(rf"^  {dim}: \"([^\"]*)\"", text, re.MULTILINE)
        if not match or match.group(1) not in STATES:
            raise ValueError(f"Invalid {dim} in {case_id}")
        result[dim] = match.group(1)
    if result["repair_level"] not in ({f"RL{i}" for i in range(5)} | {"N/A"}):
        raise ValueError(f"Invalid repair level in {case_id}: {result['repair_level']}")
    return result


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    annotations = {}
    with (ROOT / "analysis" / "case_annotations.csv").open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            annotations[row["case_id"]] = row

    matrix = []
    for number in range(1, 11):
        case_id = f"PS{number:03d}"
        meta = read_metadata(case_id)
        ann = annotations[case_id]
        matrix.append({
            "case_id": case_id,
            "artifact": ann["artifact"],
            "ecosystem": ann["ecosystem"],
            **{dim: meta[dim] for dim in DIMS},
            "H": ann["H"],
            "repair_level": meta["repair_level"],
            "ootb_outcome": ann["ootb_outcome"],
            "mechanisms": ann["mechanisms"],
            "evidence_status": meta["evidence_status"],
        })
    write_csv(NORMALIZED / "master_matrix.csv", matrix)

    denominator_rows = []
    for dim in DIMS:
        counts = Counter(row[dim] for row in matrix)
        denominator = sum(counts[state] for state in ("PASS", "PARTIAL", "FAIL"))
        for state in ("PASS", "PARTIAL", "FAIL"):
            numerator = counts[state]
            denominator_rows.append({
                "dimension": dim,
                "state": state,
                "numerator": numerator,
                "denominator": denominator,
                "percentage": round(numerator / denominator * 100, 1) if denominator else "NA",
                "excluded_na": counts["N/A"],
                "excluded_unknown": counts["UNKNOWN"],
            })
    write_csv(TABLES / "dimension_denominators.csv", denominator_rows)

    repair_counts = Counter(row["repair_level"] for row in matrix)
    repair_rows = [{"repair_level": level, "count": repair_counts[level]} for level in ["RL0","RL1","RL2","RL3","RL4","N/A"]]
    write_csv(TABLES / "repair_level_distribution.csv", repair_rows)

    mechanisms = Counter(
        mechanism
        for row in matrix
        for mechanism in row["mechanisms"].split(";")
        if mechanism
    )
    mechanism_rows = [{"mechanism": key, "case_count": value} for key, value in sorted(mechanisms.items())]
    write_csv(TABLES / "failure_mechanisms.csv", mechanism_rows)

    outcome = Counter()
    for row in matrix:
        if row["H"] == "UNSAT":
            category = "HARDWARE_OR_INFRA_NA"
        elif row["ootb_outcome"] == "PASS":
            category = "OOTB_PASS"
        elif row["ootb_outcome"] == "FAIL" and row["E"] == "PASS":
            category = "RECOVERED_TO_EXECUTION_PASS"
        elif row["E"] == "PARTIAL":
            category = "PARTIAL_EXECUTION"
        else:
            category = "TRACE_UNKNOWN"
        outcome[category] += 1
    outcome_rows = [{"category": key, "case_count": value} for key, value in sorted(outcome.items())]
    write_csv(TABLES / "ootb_vs_recovered.csv", outcome_rows)

    ps003 = list(csv.DictReader((ROOT / "evidence" / "PS003" / "normalized" / "validated_jdk_summary.csv").open(encoding="utf-8-sig", newline="")))
    ps003_rows = []
    for row in ps003:
        values = list(row.values())
        n = int(values[1])
        mean = float(values[2])
        median = float(values[3])
        sd = float(values[4])
        minimum = float(values[6])
        maximum = float(values[7])
        margin = 4.3026527299 * sd / math.sqrt(n)
        ps003_rows.append({
            "jdk": row["JDK"], "n": n, "mean_ratio_x": mean,
            "median_ratio_x": median, "sd_ratio_x": sd,
            "cv_percent": float(values[5]), "min_ratio_x": minimum,
            "max_ratio_x": maximum,
            "ci95_low": mean - margin, "ci95_high": mean + margin,
            "ci_method": "two-sided t interval, df=2",
        })
    write_csv(TABLES / "ps003_jdk_analysis.csv", ps003_rows)

    ps008_source = ROOT / "evidence" / "PS008" / "normalized" / "selected_results.csv"
    ps008_rows = list(csv.DictReader(ps008_source.open(encoding="utf-8-sig", newline="")))
    write_csv(TABLES / "ps008_configuration_comparison.csv", ps008_rows)

    FIGURES.mkdir(parents=True, exist_ok=True)
    make_figures(matrix, repair_rows, mechanism_rows, outcome_rows, ps003_rows, ps008_rows)
    write_markdown_matrix(matrix)
    print(f"Generated matrix={len(matrix)} cases, denominators={len(denominator_rows)} rows, figures=6")


def make_figures(matrix, repair_rows, mechanism_rows, outcome_rows, ps003_rows, ps008_rows) -> None:
    palette = {"PASS": "#2a9d8f", "PARTIAL": "#e9c46a", "FAIL": "#e76f51", "N/A": "#b8b8b8", "UNKNOWN": "#6c757d"}
    values = {state: index for index, state in enumerate(STATES)}
    data = np.array([[values[row[d]] for d in DIMS] for row in matrix])
    cmap = plt.matplotlib.colors.ListedColormap([palette[state] for state in STATES])
    fig, ax = plt.subplots(figsize=(8, 5.5)); ax.imshow(data, cmap=cmap, vmin=-.5, vmax=4.5, aspect="auto")
    ax.set_xticks(range(6), DIMS); ax.set_yticks(range(10), [r["case_id"] for r in matrix])
    for y, row in enumerate(matrix):
        for x, dim in enumerate(DIMS): ax.text(x, y, row[dim], ha="center", va="center", fontsize=7)
    ax.set_title("Reproducibility dimensions by case"); fig.tight_layout(); fig.savefig(FIGURES / "reproducibility_heatmap.png", dpi=200); plt.close(fig)

    bar(FIGURES / "repair_level_distribution.png", [r["repair_level"] for r in repair_rows], [r["count"] for r in repair_rows], "Repair-level distribution", "Cases")
    bar(FIGURES / "failure_mechanisms.png", [r["mechanism"].replace("_", "\n") for r in mechanism_rows], [r["case_count"] for r in mechanism_rows], "Observed mechanism frequency", "Cases", (10, 5))
    bar(FIGURES / "ootb_vs_recovered.png", [r["category"].replace("_", "\n") for r in outcome_rows], [r["case_count"] for r in outcome_rows], "OOTB and recovery outcomes", "Cases", (9, 5))

    fig, ax = plt.subplots(figsize=(7, 4.5)); x = np.arange(len(ps003_rows)); means = [r["mean_ratio_x"] for r in ps003_rows]
    low = [r["mean_ratio_x"] - r["ci95_low"] for r in ps003_rows]; high = [r["ci95_high"] - r["mean_ratio_x"] for r in ps003_rows]
    ax.errorbar(x, means, yerr=[low, high], fmt="o", capsize=5); ax.set_xticks(x, [r["jdk"] for r in ps003_rows]); ax.set_ylabel("Baseline-adjusted ijOps/sjOps ratio (×)"); ax.set_title("PS003 JDK sensitivity (mean and 95% t interval)"); fig.tight_layout(); fig.savefig(FIGURES / "ps003_jdk_analysis.png", dpi=200); plt.close(fig)

    if ps008_rows:
        value_key = next(k for k in ps008_rows[0] if "runtime" in k.lower() or k.lower() == "value")
        kernels = ["DAXPY", "TRIAD", "REDUCE_SUM"]
        current = {next(k for k in kernels if k in r["metric"]): float(r[value_key]) for r in ps008_rows if r["execution_id"] == "PS008-CURRENT"}
        historical = {next(k for k in kernels if k in r["metric"]): float(r[value_key]) for r in ps008_rows if r["execution_id"] == "PS008-HISTORICAL"}
        x = np.arange(len(kernels)); width = 0.36
        fig, ax = plt.subplots(figsize=(8, 4.8))
        b1 = ax.bar(x - width / 2, [current[k] for k in kernels], width, label="Current reconstructed configuration")
        b2 = ax.bar(x + width / 2, [historical[k] for k in kernels], width, label="Historical reconstructed configuration")
        ax.set_xticks(x, kernels); ax.set_ylabel("Mean runtime (s)"); ax.set_title("PS008 retained configuration runtimes")
        ax.legend(); ax.bar_label(b1, fmt="%.3f"); ax.bar_label(b2, fmt="%.3f")
        fig.tight_layout(); fig.savefig(FIGURES / "ps008_configuration_comparison.png", dpi=200); plt.close(fig)


def bar(path: Path, labels, values, title: str, ylabel: str, size=(7, 4.5)) -> None:
    fig, ax = plt.subplots(figsize=size); bars = ax.bar(labels, values, color="#457b9d")
    ax.set_title(title); ax.set_ylabel(ylabel); ax.bar_label(bars); ax.tick_params(axis="x", labelsize=8); fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def write_markdown_matrix(matrix) -> None:
    lines = ["# Final Master Matrix", "", "Generated from retained case metadata by `analysis/scripts/run_analysis.py`.", "", "| ID | Artifact | A | I | B | E | N | P | H | Repair |", "|---|---|---|---|---|---|---|---|---|---|"]
    for row in matrix:
        lines.append("| " + " | ".join([row["case_id"], row["artifact"], *(row[d] for d in DIMS), row["H"], row["repair_level"]]) + " |")
    (ROOT / "MASTER_MATRIX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
