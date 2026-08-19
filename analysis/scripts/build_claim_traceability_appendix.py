"""Build a publication supplement joining claims to the approved matrix."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "evidence"
RESULTS = ROOT / "results"


def main() -> None:
    with (EVIDENCE / "CLAIM_REGISTRY_MASTER.csv").open(encoding="utf-8-sig", newline="") as handle:
        claims = list(csv.DictReader(handle))
    with (RESULTS / "normalized" / "master_matrix.csv").open(encoding="utf-8-sig", newline="") as handle:
        matrix = {row["case_id"]: row for row in csv.DictReader(handle)}
    rows = []
    for claim in claims:
        fields = [field for field in claim["matrix_field"].split(";") if field]
        statuses = ";".join(f"{field}={matrix[claim['case_id']][field]}" for field in fields)
        references = [item.strip() for item in claim["raw_evidence"].split(";") if item.strip()]
        rows.append({
            "claim_id": claim["claim_id"], "case_id": claim["case_id"],
            "label": claim["label"], "claim": claim["claim"],
            "evidence_references": claim["raw_evidence"],
            "all_references_exist": all((ROOT / ref).exists() for ref in references),
            "transformation": claim["transformation"],
            "normalized_evidence": claim["normalized_evidence"],
            "matrix_status": statuses, "claim_status": claim["status"],
            "supporting_claim_ids": claim["supporting_claim_ids"],
        })
    destination = RESULTS / "tables" / "claim_traceability_appendix.csv"
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    print(f"Generated {len(rows)} traceability rows")


if __name__ == "__main__":
    main()
