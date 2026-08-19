.PHONY: validate hashes analysis manuscript all

validate:
	python scripts/validate_repository.py

hashes:
	python scripts/verify_evidence_hashes.py

analysis:
	python analysis/scripts/run_analysis.py
	python analysis/scripts/robustness_analysis.py

manuscript:
	cd manuscript && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

all: validate hashes analysis
