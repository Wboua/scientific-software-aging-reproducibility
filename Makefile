.PHONY: validate hashes analysis manuscript all docker-build docker-run

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


docker-build:
	docker build -t scientific-software-aging-analysis .

docker-run:
	docker run --rm scientific-software-aging-analysis
