# Failure and Drift Taxonomy

Mechanisms describe **why** a capability was impeded or changed. They are non-exclusive and are stored separately from outcome states and repair level.

| Code | Class | Definition | Cases observed |
|---|---|---|---|
| D1 | Dependency decay | Required packages or system libraries are unavailable, incompatible, or no longer reconstructable as originally specified. | PS005, PS010 |
| D2 | Toolchain/build drift | Compiler, build-system, submodule, CMake/Make, or generated-build assumptions obstruct the original path. | PS008, PS009 |
| D3a | Runtime version sensitivity | A retained benchmark remains executable but its measured performance changes materially across runtime versions under an otherwise controlled protocol. This label does **not** imply an API break. | PS003 |
| D3b | Runtime semantic drift | The program installs or starts, but changed runtime semantics alter or terminate execution. | PS010 |
| D4 | Environment coupling | The workflow depends on author- or host-specific filesystem, device, configuration, or locale/encoding assumptions. | PS004 |
| D4a | Encoding environment | Execution is blocked by host text-encoding behavior rather than a scientific or API-level failure. | PS004 |
| D5 | Infrastructure/virtualization constraint | A preserved VM/container path cannot be meaningfully evaluated because the required infrastructure is not satisfiable on the retained host. | PS007 |
| D6 | Hardware constraint | The artifact requires an unavailable accelerator or hardware class. | PS002 |
| D7 | Performance drift | Correctness or execution evidence survives while performance measurements are not preserved or remain only partially comparable. | PS003, PS008 |
| D8 | Evidence/trace decay | A historical claim or intervention path cannot be audited at the same resolution because its raw evidentiary trace is incomplete. | PS001, PS009 |
| D9 | Workflow/data-orchestration barrier | Build or startup succeeds, but an external data-generation, ground-truth, or orchestration condition blocks the end-to-end experiment. | PS006 |

## Coding discipline

- `RUNTIME_API_DRIFT` is no longer used as a broad catch-all category.
- API removal/renaming should be coded only when the retained evidence shows a concrete API incompatibility.
- Locale/encoding failures are coded as environment coupling rather than runtime/API drift.
- Mechanism counts are descriptive, non-exclusive, and do not represent prevalence outside the corpus.
