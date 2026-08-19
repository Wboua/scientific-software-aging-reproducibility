# Repair Taxonomy

## RL0 — No repair
Author instructions work directly, or case is stopped only by external hardware/infrastructure constraint.

## RL1 — Environment/configuration
Examples: create expected output directory; set environment variable; select working directory.

## RL2 — Dependency/toolchain
Examples: install system library (`libuv`); initialize submodules; install compatible CMake/runtime/package version.

## RL3 — Build/packaging/path
Examples: line-ending normalization; repair author-specific path assumption; packaging/build-file compatibility change that does not change the scientific algorithm.

## RL4 — Scientific source modification
Changes algorithm/data processing/model logic. This materially weakens direct reproduction claims and must be analyzed separately.

## RL5 — Unrecovered
Repair attempt stopped, impossible, or evidence insufficient.

### Principle
A project recovered at RL1–RL3 is not equivalent to a project requiring RL4. The article should report repair type and intensity, not only final PASS/FAIL.
