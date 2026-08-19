# Reproduction workflow

## 1. Validate repository structure

```bash
python scripts/validate_repository.py
```

## 2. Verify retained evidence

```bash
python scripts/verify_evidence_hashes.py
```

## 3. Regenerate cross-case analysis

```bash
python analysis/scripts/run_analysis.py
python analysis/scripts/robustness_analysis.py
```

These commands rebuild the master matrix, dimension-specific denominators, recovery summaries, failure-mechanism counts, PS003 statistics, PS008 comparison table, sensitivity analysis, transition analysis, and primary analysis figures.

## 4. Optional case-specific normalization

```bash
python analysis/scripts/normalize_ps003_jmh.py
python analysis/scripts/normalize_ps005_metrics.py
python analysis/scripts/expand_ps003_statistics.py
python analysis/scripts/build_ps008_presentation_table.py
```

Case-specific scripts expect the retained evidence paths in this repository.

## 5. Rebuild traceability appendix

```bash
python analysis/scripts/build_claim_traceability_appendix.py
```
