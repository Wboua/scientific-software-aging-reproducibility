# Reproducible analysis environment for the normalized cross-case study.
# This image reproduces repository validation, evidence-integrity checks,
# and the Python analysis pipeline. It intentionally does NOT containerize
# the ten heterogeneous historical third-party artifacts themselves.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg

WORKDIR /workspace

# Install Python dependencies first to maximize Docker layer reuse.
COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# Copy the frozen replication package.
COPY . .

# Default command reproduces the normalized analysis after checking the
# repository structure and retained-evidence hashes.
CMD ["sh", "-c", "python scripts/validate_repository.py && python scripts/verify_evidence_hashes.py && python analysis/scripts/run_analysis.py && python analysis/scripts/robustness_analysis.py"]
