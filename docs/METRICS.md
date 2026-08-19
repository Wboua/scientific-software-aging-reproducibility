# Study Metrics

## Layer metrics
For eligible cases only:
- Availability rate: A_PASS / eligible A cases
- OOTB install/build rate
- OOTB execution rate
- Post-repair execution rate
- Numerical/scientific fidelity rate
- Performance fidelity rate

Do not use hardware/infrastructure N/A cases in denominators for software executability.

## Repair metrics
- Maximum Repair Level per case.
- Number of distinct interventions.
- Number of environment-only vs source-code interventions.
- Repair success: highest layer before vs after intervention.

## Fidelity metrics
When comparable numbers exist:
- Absolute difference: |x_repro - x_ref|
- Relative difference: |x_repro - x_ref| / |x_ref|
- Ratio for performance: T_ref / T_variant or historical/current as explicitly defined.
- Coefficient of variation across independent runs.

## Evidence completeness
- EC0: artifact only
- EC1: commands/errors preserved
- EC2: raw quantitative output preserved
- EC3: environment + raw output + normalized result preserved

This enables analysis of trace quality independent of software quality.


## Fidelity decision rules added after reviewer audit

### Numerical/scientific fidelity N
- `PASS`: explicit artifact-specific oracle/reference/tolerance fully satisfied within declared scope.
- `PARTIAL`: a meaningful subset of outputs/criteria is established, but full equivalence to the author target is not.
- `FAIL`: an explicit eligible criterion is evaluated and violated.
- `UNKNOWN`: outputs exist or may have existed, but no defensible oracle/comparison basis is retained.

### Performance fidelity P
- `PASS`: sufficiently comparable protocol/reference and declared performance criterion preserved.
- `PARTIAL`: performance is measured and interpretable, but full fidelity/comparability is not established because of sensitivity, variability, or confounding.
- `FAIL`: a comparable declared performance criterion is evaluated and violated.
- `UNKNOWN`: performance output exists but no defensible comparator/protocol supports fidelity.

### External eligibility H
H uses `SAT`, `UNSAT`, `UNKNOWN`, not software outcome states. An `UNSAT` prerequisite can make downstream dimensions `N/A` without implying artifact failure.
