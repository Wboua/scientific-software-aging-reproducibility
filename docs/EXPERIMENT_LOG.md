# Experiment Log — Consolidated From This Study

This log contains only observations explicitly recovered from the working discussion/evidence. Missing details are marked rather than reconstructed.

## PS001 — DLinear / LTSF-Linear
- Candidate previously studied with Electricity and MSE/MAE comparison around DLinear/FEDformer.
- Raw historical run folder/logs are currently unavailable in this workspace.
- Official repository itself warns that after script updates some DLinear results are slightly different.
- Status: preserve as TRACE-INCOMPLETE until logs are recovered or experiment is deliberately rerun under a preregistered protocol.

## PS002 — Hidet
- Git commit observed: `f2e9767bb2464bd0592a8ec0b276f97481f13df2`, dated 2023-04-25.
- Tag observed: `v1.0`.
- TVM submodule initially uninitialized (`-c07a...`).
- Authors' platform: i9-12900K, RTX 3090, 64 GiB, Linux, NVIDIA driver; README reports CUDA 11.6 and NVIDIA driver 510.73.08.
- Host probe: `nvidia-smi` unavailable; Windows reports Intel Iris Xe Graphics only.
- Classification: HW-CONSTRAINED. Scientific execution not attempted because required NVIDIA GPU is absent.

## PS003 — SciJava Ops
- Reinforced protocol: Temurin JDK 17, 21, 25; same machine/OS/code/classes/dependencies; 5×5s warmup; 10×5s measurement; 3 forks; 3 independent repetitions.
- Mean framework ratio statistic recovered: JDK17 139.057× (CV 13.57%), JDK21 79.470× (CV 50.53%), JDK25 61.060× (CV 34.46%).
- Mean sjOps μs/op: 266.138, 411.615, 311.190 for JDK17/21/25.
- Mean ijOps μs/op: 35467.494, 24732.629, 20240.559.
- Interpretation: execution survives, quantitative performance relationship is runtime-sensitive.

## PS004 — TimeX++ / FreqShape
- Dataset/code path investigation recovered multiple author-machine absolute paths, e.g. `/TimeX/datasets/...` and `/n/data1/.../TimeSeriesCBM/datasets/FreqShape`.
- `process_Synth` and FreqShape generator are present, but scripts embed environment-specific filesystem assumptions.
- Classification: environment coupling / hard-coded experimental context; partial/repaired execution history should be supplemented with raw run log if recovered.

## PS005 — ADSketch
- Candidate: ADSketch / Yahoo public anomaly dataset via Code Ocean-style artifact.
- Historical reconstruction previously produced an exploitable run; an F1 around 0.556 was discussed, but raw evidence is not currently embedded here.
- Do not publish that exact number until its raw log is recovered.
- Classification: repaired/environment-sensitive.

## PS006 — RQuBE / BBFS
- Author build command: `g++ -O3 src/RQuBE_(node/edge).cpp -o out`.
- BBFS has a separate build/run path and generates ground-truth files required by later parameter experiments.
- We reached buildability, but practical experiment completion was blocked during BBFS/RQuBE workflow; discussion recorded `input 0 0 / size less than 3` behavior and very high initialization cost.
- Classification: BUILD-PASS / EXPERIMENT-CONSTRAINED.

## PS007 — Sound Static Data Race Verification for C
- Downloaded both source artifact and 4.5GB VM artifact.
- OVA imported successfully into VirtualBox 7.2.14.
- VM start failed with `VERR_UNRESOLVED_ERROR` / `E_FAIL (0x80004005)`.
- Authors specify 8 CPUs, 26GB RAM for full evaluation; reduced evaluation 8 CPUs, 16GB RAM, ~2h.
- Classification: INFRA-CONSTRAINED, not algorithm failure.

## PS008 — RAJAPerf
Historical checkout:
- tag `v2024.07.0`, commit `6e81aa58`.
Current checkout:
- commit `338cfeb7`.
- Current submodules observed: BLT `e783e30f...`, RAJA `4302ac72...`, Kokkos `f5723022...`.
- Initial historical build required submodule and CMake/toolchain repair; eventual build reached 100%.
- Selected kernels: `Basic_DAXPY`, `Stream_TRIAD`, `Algorithm_REDUCE_SUM`.
- Current mean runtimes (Base_Seq): 0.675188s, 1.662521s, 0.100516s.
- Historical mean runtimes (Base_Seq): 2.010450s, 5.633594s, 0.268251s.
- Current checksum report: selected variants PASSED; relative differences zero or near machine precision.
- Classification: numerical fidelity PASS after repair; performance drift observed. Do not infer cause solely from timing difference because code/environment also differ.

## PS009 — NPB-CPP
- Repository commit observed: `d31c997580ef1a58c13c69fe02dadcb3e0e95105` (2021-07-29).
- README warns tests were made with GCC-5.
- Initial generated `npbparams.hpp` contained broken quoted macros and compilation failed with `missing terminating " character`.
- Copying to a clean Linux location and normalizing CRLF in `config/make.def` allowed EP, CG, MG Class S builds.
- Observed validation:
  - EP: 1.00 s, 33.52 Mop/s, Verification SUCCESSFUL
  - CG: 0.03 s, 2354.52 Mop/s, Verification SUCCESSFUL
  - MG: 0.00 s, 7091.58 Mop/s, Verification SUCCESSFUL
- Classification: OOTB build failure -> minimal packaging/environment repair -> scientific verification PASS.

## PS010 — mgm / R
Modern environment:
- Rocker R 4.6.1.
- Initial `mgm` installation failed because `fs` could not find libuv; dependency cascade propagated through sass/bslib/rmarkdown/Hmisc/qgraph/mgm.
- After installing libuv development package, `mgm` 1.2-15 installed.
- `examples_mgm.R` initially failed because `figures/` was absent.
- After `mkdir -p figures`, script generated at least `Fig_mgm_p4_example.pdf` and `Fig_mgm_p4_resampling.pdf`, then failed in `mgmsampler()` with `the condition has length > 1`.
Historical runtime probe:
- R 3.6.3 launched successfully.
- Matrix class probe returned `"matrix"`, condition TRUE, `accepted`.
- Attempted historical `mgm 1.2-9` reconstruction. `stringr 1.4.0` was eventually installed after historical glue/stringi, but Hmisc/qgraph triggered a large dependency cascade; reconstruction deliberately stopped.
- Classification: modern dependency decay + runtime/API semantic drift; historical runtime availability does not imply historical ecosystem reconstructability.

## 2026-08-15 — Q1 manuscript audit revision (non-experimental)

- Scope: manuscript structure, evidentiary wording, reviewer cautions, venue planning, and submission metadata.
- Scientific data changes: none. `results/normalized/master_matrix.csv` and raw evidence were not modified.
- Applied: PS001 trace-decay result framing; denominator cautions; human-coding limitation; targeted-review scope; title/abstract revision; Table 5 relocation; TRACE_DECAY definition; traceability supplement statement; data-availability and submission checklists.
- Deferred: independent human recoding/κ, LIT013/LIT014 verification, current venue-rule verification, Zenodo deposit, and truncated R6/R7/R9/R10 instructions.

## 2026-08-15 — Scientific positioning update (non-experimental)

- Modified manuscript files: `manuscript/02_related_work.md`, `manuscript/references.bib`, `manuscript/SCIENTIFIC_POSITIONING_UPDATE.md`, `manuscript/SUBMISSION_CHECKLIST.md`, and `manuscript/Q1_REVISION_REPORT.md`.
- Modified literature metadata: `analysis/literature/literature_matrix.csv`.
- Added and verified: Muttakin et al. ICSE 2026 and Guilloteau et al. ACM REP 2024.
- Resolved: LIT013 as R4R (DOI `10.1145/3736731.3746156`) and LIT014 as the ACM REP 2025 HPC/distributed paper (DOI `10.1145/3736731.3746141`), both `VERIFIED-PRIMARY`.
- Scientific data changes: none. Raw evidence and `results/normalized/master_matrix.csv` were not modified.

## 2026-08-15 — Reviewer-oriented figure expansion (non-experimental)

- Generated 5 new manuscript figures from normalized data. No scientific data modified. Source: `analysis/scripts/generate_new_figures.py`.
- Outputs: timeline, aggregate capability-chain profile, UNKNOWN sensitivity bounds, analytical preservation-scope matrix, and corpus-size/measurement-resolution comparison; each exported as 300-DPI PNG and vector PDF.
- Manuscript integration: Figures 5--16 were renumbered consistently across Sections 4--6; analytical graphics are explicitly distinguished from experimental outcomes and causal estimates.
- Protected artifacts: raw evidence, `MASTER_MATRIX.md`, and `results/normalized/master_matrix.csv` were not modified.

## 2026-08-15 — LaTeX portability correction (non-experimental)

- Modified `manuscript/07_threats_to_validity.md`: replaced the literal Unicode kappa with the equivalent LaTeX math expression `$\kappa$`.
- Rationale: MiKTeX `pdflatex` reported U+03BA as unsupported and stopped compilation.
- Scientific meaning and data: unchanged.

## 2026-08-15 — Full argumentation reinforcement (non-experimental)

- Manuscript files modified: `00_abstract.md`, `01_introduction.md`, `02_related_work.md`, `03_methodology.md`, `04_experimental_setup.md`, `05_results.md`, `06_discussion.md`, `07_threats_to_validity.md`, `references.bib`, `Q1_REVISION_REPORT.md`, and new `FULL_REVISION_REPORT.md`.
- Generator/audit files modified: `analysis/scripts/build_latex_manuscript.py` and `analysis/scripts/assemble_and_audit_manuscript.mjs`.
- Nature: strengthened differential positioning, defended the n=10 depth/breadth trade-off, formalized TRACE_DECAY, added a corpus-resolution comparison table, reinforced N/P discussion, normalized selected typography, and renumbered manuscript tables 3--7.
- References: added Runeson and the verified R4R/HPC ACM REP 2025 records; Muttakin and Guilloteau integrations retained.
- Figure audit: eleven PNGs declare 200--220 DPI; print-ready 300-DPI/vector regeneration remains incomplete and is reported as PARTIAL.
- Human/external actions not simulated: independent recoding/κ, final venue decision, and Zenodo DOI deposit.
- Scientific data changes: none. Raw evidence and `results/normalized/master_matrix.csv` were not modified.
