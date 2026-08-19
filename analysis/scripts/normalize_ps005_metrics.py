"""Normalize retained PS005 per-series precision/recall/F1 logs."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "evidence" / "PS005"
PATTERN = re.compile(r"precision: ([0-9.]+), recall: ([0-9.]+), f1: ([0-9.]+)")


def main() -> None:
    rows = []
    for environment in ("env01", "env02"):
        source = CASE / "outputs" / f"ps005_series_metrics_{environment}.txt"
        raw = source.read_bytes()
        text = raw.decode("utf-16") if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else raw.decode("utf-8-sig")
        matches = PATTERN.findall(text)
        if len(matches) != 67:
            raise ValueError(f"Expected 67 series in {source.name}, found {len(matches)}")
        for index, (precision, recall, f1) in enumerate(matches):
            rows.append({
                "case_id": "PS005",
                "execution_id": f"PS005-{environment.upper()}",
                "series_index": index,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "source_file": f"evidence/PS005/outputs/{source.name}",
                "source_locator": f"metric row {index + 1}",
                "label": "OUR-OBSERVED",
                "status": "READY-FOR-REVIEW",
            })
    destination = CASE / "normalized" / "yahoo_metrics.csv"
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
