"""Normalize retained PS003 JMH JSON files without modifying raw evidence."""

from __future__ import annotations

import csv
import json
import math
import re
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "evidence" / "PS003"
OUTPUTS = CASE / "outputs"
NORMALIZED = CASE / "normalized"
RUN_PATTERN = re.compile(r"jdk(17|21|25)-run([123])\.json$")


def main() -> None:
    rows: list[dict[str, object]] = []
    selected: dict[tuple[str, int], dict[str, float]] = {}

    for path in sorted(OUTPUTS.glob("jdk*-run*.json")):
        match = RUN_PATTERN.fullmatch(path.name)
        if not match:
            continue
        jdk, repetition_text = match.groups()
        repetition = int(repetition_text)
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        for result in payload:
            observed_protocol = (
                result["jmhVersion"],
                result["threads"],
                result["forks"],
                result["warmupIterations"],
                result["warmupTime"],
                result["measurementIterations"],
                result["measurementTime"],
            )
            expected_protocol = ("1.36", 1, 3, 5, "5 s", 10, "5 s")
            if observed_protocol != expected_protocol:
                raise ValueError(f"Unexpected protocol in {path.name}: {observed_protocol}")
            benchmark = result["benchmark"].rsplit(".", 1)[-1]
            metric = result["primaryMetric"]
            rows.append(
                {
                    "case_id": "PS003",
                    "execution_id": f"PS003-JDK{jdk}-R{repetition}",
                    "jdk": jdk,
                    "independent_repetition": repetition,
                    "benchmark": benchmark,
                    "score": repr(metric["score"]),
                    "score_error": repr(metric["scoreError"]),
                    "unit": metric["scoreUnit"],
                    "forks": result["forks"],
                    "warmup_iterations": result["warmupIterations"],
                    "warmup_time": result["warmupTime"],
                    "measurement_iterations": result["measurementIterations"],
                    "measurement_time": result["measurementTime"],
                    "threads": result["threads"],
                    "jmh_version": result["jmhVersion"],
                    "jdk_version": result["jdkVersion"],
                    "source_file": f"evidence/PS003/outputs/{path.name}",
                    "source_locator": f"benchmark={result['benchmark']}; primaryMetric",
                    "label": "OUR-OBSERVED",
                    "status": "READY-FOR-REVIEW",
                }
            )
            if benchmark in {"noOps", "sjOps", "ijOps"}:
                selected.setdefault((jdk, repetition), {})[benchmark] = float(metric["score"])

    if len(rows) != 90:
        raise ValueError(f"Expected 90 benchmark rows, found {len(rows)}")

    NORMALIZED.mkdir(parents=True, exist_ok=True)
    result_path = NORMALIZED / "jmh_results.csv"
    with result_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary_rows: list[dict[str, object]] = []
    for jdk in ("17", "21", "25"):
        runs = [selected[(jdk, repetition)] for repetition in (1, 2, 3)]
        ratios = [
            (run["ijOps"] - run["noOps"]) / (run["sjOps"] - run["noOps"])
            for run in runs
        ]
        mean_ratio = statistics.mean(ratios)
        sd_ratio = statistics.stdev(ratios)
        summary_rows.append(
            {
                "case_id": "PS003",
                "jdk": f"Temurin {jdk}",
                "n_independent_runs": 3,
                "mean_ratio_x": repr(mean_ratio),
                "median_ratio_x": repr(statistics.median(ratios)),
                "sd_ratio_x": repr(sd_ratio),
                "cv_percent": repr(sd_ratio / mean_ratio * 100),
                "min_ratio_x": repr(min(ratios)),
                "max_ratio_x": repr(max(ratios)),
                "mean_sjops_us_per_op": repr(statistics.mean(run["sjOps"] for run in runs)),
                "mean_ijops_us_per_op": repr(statistics.mean(run["ijOps"] for run in runs)),
                "transformation": "per-run (ijOps-noOps)/(sjOps-noOps) ratio; arithmetic mean; sample SD",
                "source_file": "evidence/PS003/normalized/jmh_results.csv",
                "label": "OUR-OBSERVED",
                "status": "READY-FOR-REVIEW",
            }
        )

    # This file is a verification recalculation, not a replacement for the
    # researcher-validated aggregate retained in provenance/.
    summary_path = NORMALIZED / "raw_recalculation_check.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0]))
        writer.writeheader()
        writer.writerows(summary_rows)

    if any(not math.isfinite(float(row["mean_ratio_x"])) for row in summary_rows):
        raise ValueError("Non-finite summary value")

    print(f"Wrote {len(rows)} rows to {result_path.relative_to(ROOT)}")
    print(f"Wrote {len(summary_rows)} rows to {summary_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
