# Data dictionary

## Capability states

- `PASS`: the declared criterion was evaluated and supported by retained evidence.
- `PARTIAL`: a meaningful subset was supported, but the full criterion was not established.
- `FAIL`: an applicable criterion was evaluated and demonstrably failed.
- `N/A`: the dimension is inapplicable or cannot legitimately be evaluated because an external prerequisite is unsatisfied.
- `UNKNOWN`: retained evidence is insufficient for classification.

## Dimensions

- `A`: artifact availability.
- `I`: installability/dependency resolution.
- `B`: buildability.
- `E`: executability.
- `N`: scientific-result/numerical fidelity.
- `P`: performance fidelity.
- `H`: external hardware/infrastructure eligibility (`SAT`, `UNSAT`, `UNKNOWN`).

## Repair depth

- `RL0`: no repair.
- `RL1`: environment/configuration intervention.
- `RL2`: dependency/toolchain intervention.
- `RL3`: build/packaging/path intervention.
- `RL4`: scientific source modification.
- `N/A`: repair depth cannot be established from retained evidence.

Recovery outcome is recorded separately from repair depth.

## Provenance labels

- `AUTHOR-REPORTED`: taken from the original publication/artifact documentation.
- `OUR-OBSERVED`: obtained directly from retained executions or files in this study.
- `INFERENCE`: an interpretation supported by explicitly linked evidence.
