# Study Protocol

## Objective
Evaluate how scientific software artifacts age and which layers of reproducibility fail independently over time.

## Unit of analysis
A published scientific software artifact linked to a research paper and an executable experimental claim.

## Closed corpus
PS001–PS010 only.

## Experimental ladder
For every case, attempt the following where applicable:

- E0 — Artifact identity and availability.
- E1 — Contemporary out-of-the-box installation/build/run.
- E2 — Author-provided preservation mechanism (container/VM/lockfile) where available.
- E3 — Minimal environment/dependency repair.
- E4 — Historical/runtime reconstruction where justified.
- E5 — Scientific/numerical validation against author-provided or benchmark reference criteria.
- E6 — Performance fidelity when the artifact/paper makes performance claims.

A later step is attempted only if meaningful and feasible. Hardware-constrained cases are not forced into software failure categories.

## Controlled principles
- Preserve original code before modification.
- Record commit/tag/date where possible.
- Record host OS, runtime, compiler, package manager, hardware, container/VM versions.
- Record exact commands.
- Capture stdout/stderr.
- Prefer benchmark-internal validation checks (checksums, `Verification SUCCESSFUL`, tolerances) over visual inspection.
- Distinguish correctness from performance.

## Primary outcomes
- OOTB status.
- Highest reproducibility layer reached.
- Repair level required.
- Failure/drift classes observed.
- Numerical/scientific fidelity.
- Performance fidelity.
- Infrastructure/hardware feasibility.

## Cross-case caution
This is a heterogeneous multiple-case empirical study, not a statistically representative random sample of all scientific software. Percentages describe the corpus, not the population of scientific software.
