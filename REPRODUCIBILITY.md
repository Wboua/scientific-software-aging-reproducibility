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

## 6. Rebuild manuscript

```bash
cd manuscript
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## 7. Reproduce the normalized analysis with Docker

The repository root contains a Dockerfile for the analysis pipeline only. This keeps the analysis environment reproducible without pretending that the ten heterogeneous aged artifacts share a single containerizable execution environment.

```bash
docker build -t scientific-software-aging-analysis .
docker run --rm scientific-software-aging-analysis
```

To write regenerated files back into the checked-out repository:

```bash
docker run --rm -v "$PWD:/workspace" scientific-software-aging-analysis
```

The default container command runs:

```text
validate_repository.py
verify_evidence_hashes.py
run_analysis.py
robustness_analysis.py
```

The manuscript build remains separate because it requires a TeX distribution; the Docker image is intentionally limited to the auditable Python analysis path.
