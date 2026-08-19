# Candidate Selection and Justification

The corpus is purposefully heterogeneous rather than statistically random. Selection maximizes variation in ecosystem, scientific workload, preservation strategy, expected output, and aging mechanism.

| Case | Why it belongs in the corpus |
|---|---|
| PS001 DLinear | ML forecasting; published numeric MSE/MAE; official repo acknowledges script updates can slightly change results, making result drift directly relevant. |
| PS002 Hidet | GPU compiler artifact with Docker but hard NVIDIA/CUDA requirements; tests whether container preservation removes hardware dependence (it does not). |
| PS003 SciJava Ops | Scientific imaging framework with reproducible JMH benchmark; ideal controlled runtime/JDK performance-drift case. |
| PS004 TimeX++ | Modern ML/XAI artifact where dataset/path assumptions expose environment coupling beyond dependency lists. |
| PS005 ADSketch | Software-engineering/operations anomaly detection artifact, public+industrial evaluation, Code Ocean-style preservation; tests dependency reconstruction and metric fidelity. |
| PS006 RQuBE | Algorithmic C++ graph-query workload with separate ground-truth generation; demonstrates gap between buildability and end-to-end experimental reproducibility. |
| PS007 Data Race Verification | Formal verification artifact explicitly packaged as source + VM because BenchExec does not run in Docker; strong infrastructure-aging case. |
| PS008 RAJAPerf | HPC benchmark designed for performance portability; enables simultaneous numerical correctness and performance-fidelity analysis. |
| PS009 NPB-CPP | Legacy/benchmark C++ port with internal `Verification SUCCESSFUL`; excellent build-aging and scientific verification case. |
| PS010 mgm | R package with fully reproducible examples; exposes CRAN dependency aging and runtime semantic drift. |

## Coverage achieved
- Languages/ecosystems: Python, Java, C, C++, R, CUDA.
- Domains: time-series forecasting, deep-learning compilers, scientific imaging, explainability, anomaly detection, graph querying, static verification, HPC, benchmark computing, statistical graphical modeling.
- Preservation mechanisms: README/requirements, Git submodules, Docker, VM, Code Ocean-like capsule, CRAN, CMake/Make/Maven.
- Fidelity targets: MSE/MAE, F1, benchmark verification, checksums, runtime/latency, JMH ratios, generated figures, tool verdicts.
