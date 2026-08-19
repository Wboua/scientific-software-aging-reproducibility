# Provenance Policy

Use three labels in notes and manuscript source comments:
- `[AUTHOR-REPORTED]`: from candidate paper/repository.
- `[OUR-OBSERVED]`: from our terminal/log/evidence.
- `[INFERENCE]`: interpretation based on one or more observations.

Every table cell in final Results should be traceable to a case file and ideally a raw evidence filename.

Never place a published value into `results/raw/` as if our program produced it. Store author references under `papers/` or case metadata.
