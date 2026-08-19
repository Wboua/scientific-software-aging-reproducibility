# Sound Static Data Race Verification for C: Is the Race Lost?
## Artifact


## Introduction

This artifact contains the benchmarks, tools and scripts for reproduction, along with our reference results used for the paper.

### Claims
The artifact provides support for each of the following three pairs of Research Questions and Findings from the paper.

**RQ 1.** How do data race freedom verifiers that compete in SV-COMP perform on
real-world programs?

**Finding 1.** The 7 verifiers with the best results in the SV-COMP NoDataRace category successfully verify 3 (2 unique) real-world programs out of 18. The two most prominent obstacles are unsupported standard library functions or syntax.

**RQ 2.** What are the concrete multi-threaded implementation idioms preventing existing tools from verifying data race freedom in real-world programs, and how well do the selected set of SV-COMP verifiers handle each of these idioms?

**Finding 2.** Leading SV-COMP automated data race freedom verifiers are unable to reason about most thread-joining and per-thread data distribution implementation idioms from real-world programs, even when such idioms are isolated and simplified, succeeding on 8 of the 20 idioms.

**RQ 3.** How prevalent are the challenging coding idioms in real-world programs?

**Finding 3.** We find that per-thread-data idioms and thread-joining schemes occur
frequently in real-world programs. Features indicating the use of constructs that cause
verifiers to fail are under-represented in SV-COMP tasks, with five features entirely
absent.

There are no unsupported claims.


### Contents
The reproduction package contains materials for reproducing Tables 2, 5 and 6 in the paper which contain the data for answering the research questions.

We provide two versions of the artifact:

1. The source version includes benchmarks, scripts and reference results such that they can easily be accessed and reused outside of the virtual machine.
2. The virtual machine version additionally includes tools and their dependencies such that the results can be reproduced by execution.

The **source version** contains:

* `README.md`/`README.pdf` — this file.
* `concrat-benchmarks/` — Concrat benchmarks and execution scripts (RQ 1, RQ 3).
   * `results-paper/` — reference results used for Table 2 (Finding 1).
* `extracted-micro-benchmarks/` — Extracted micro-benchmarks (with their racy variations) and execution scripts (RQ 2).
   * `results-paper/` — reference results used for Table 5 (Finding 2).
* `concrat-benchmarks-excluded/` — Excluded Concrat benchmarks (RQ 3).
* `sv-benchmarks/` — SV-COMP 2023 NoDataRace-Main category benchmarks (Finding 3).
* `joern/` — Joern scripts for Table 6 (RQ 3).
   * `concrat-benchmarks-paper/` — reference results for Concrat benchmarks used for Table 6 (Finding 3).
   * `concrat-benchmarks-excluded-paper/` — reference results for excluded Concrat benchmarks used for Table 6 (Finding 3).
   * `sv-benchmarks-paper/` — reference results for SV-COMP benchmarks used for Table 6 (Finding 3).
* `sv-benchmarks.sh` — script to download SV-COMP 2023 NoDataRace-Main category benchmarks.
* `tools/download.sh` — script to download SV-COMP 2023 tools from their reproduction packages.
* `properties/no-data-race.prp` — property file for executing SV-COMP tools.

The **virtual machine version** contains all of the above in `/home/vagrant`, but also:

* `concrat-benchmarks/`
   * `results-test/` — results from kick-the-tires (initially empty).
   * `results/` — full evaluation results (initially empty) (Finding 1).
   * `results-reduced/` — reduced evaluation results (initially empty) (Finding 1).
* `extracted-micro-benchmarks/`
   * `results-test/` — results from kick-the-tires (initially empty).
   * `results/` — full evaluation results (initially empty)  (Finding 2).
   * `results-reduced/` — reduced evaluation results (initially empty)  (Finding 2).
* `joern/`
   * `concrat-benchmarks/` — results for Concrat benchmarks (initially empty) (Finding 3).
   * `concrat-benchmarks-excluded/` — results for excluded Concrat benchmarks (initially empty) (Finding 3).
   * `sv-benchmarks/` — results for SV-COMP benchmarks (initially empty) (Finding 3).
* `tools/` (subdirectories) — downloaded SV-COMP 2023 tools from their reproduction packages.


## Hardware Dependencies

The executable artifact is a [VirtualBox](https://www.virtualbox.org/) virtual machine, because [BenchExec](https://github.com/sosy-lab/benchexec) does not run in Docker.
**Full evaluation** requires:

* 8 CPU cores,
* 26 GB RAM,
* 7 GB disk space,
* ~2 days and 15 hours.

Considering the significant runtime, we also provide a reduced evaluation.
**Reduced evaluation** requires:

* 8 CPU cores,
* 16 GB RAM,
* 7 GB disk space,
* ~2 hours.


## Getting Started Guide

### Setup
1. Import the virtual machine into VirtualBox.
2. Start the virtual machine and log in with username "vagrant" (not "Ubuntu"!) and password "vagrant".
3. Right click on the desktop and open Applications → Accessories → Terminal Emulator.
   If prompted, choose GNOME Terminal.

### Concrat benchmarks kick-the-tires
1. Run `./concrat-benchmarks/run-test.sh` in the terminal emulator. This takes ~3 minutes.
2. Run `firefox concrat-benchmarks/results-test/table-generator.table.html` to view the results.
3. Switch to the Table tab in the website.
4. Check the results:

   1. Goblint should have two "true" statuses.
   2. Deagle should have one "unknown" status.
   3. Locksmith should have one "true" status.
   4. Most statuses will be "TIMEOUT" due to the very small time limit used for kick-the-tires testing.

### Extracted micro-benchmarks kick-the-tires
1. Run `./extracted-micro-benchmarks/run-test.sh` in the terminal emulator. This takes ~4 minutes.
2. Run `firefox extracted-micro-benchmarks/results-test/table-generator.table.html` to view the results.
3. Switch to the Table tab in the website.
4. Check the results:

   1. Goblint should have three correct (green) "true" statuses and four incorrect (red) "true" statuses.
   2. Deagle should have many correct (green) and incorrect (red) "true" and "false(unreach-call)" statuses.
   3. Locksmith should have three correct (green) "true" statuses and two incorrect (red) "true" statuses.
   4. Some statuses will be "TIMEOUT" due to the very small time limit used for kick-the-tires testing.


## Step-by-step Instructions

The following commands are to be executed after opening the terminal as instructed in the Setup part of the Getting Started Guide above.
It is not necessary to run the kick-the-tires steps to perform full or reduced evaluation.

### Finding 1

This experiment consists of 2 parts:

1. Running the tools on the Concrat benchmarks using BenchExec, which generates an HTML table with raw results (automated).
2. Translating the tools' raw output from the HTML table into the table included in the paper (manual).

The two parts can be done sequentially by translating the results from the automated execution,
or independently by translating the provided reference results and comparing them with the results from the automated execution.

#### Part 1

##### Full evaluation
1. Run `./concrat-benchmarks/run.sh` in the terminal emulator. This takes ~2 days and 3 hours.
2. Run `firefox concrat-benchmarks/results/table-generator.table.html` to view the results.
3. Switch to the Table tab in the website.
4. Interpret the results according to part 2 below.

##### Reduced evaluation
1. Run `./concrat-benchmarks/run-reduced.sh` in the terminal emulator. This takes ~1 hour.
2. Run `firefox concrat-benchmarks/results-reduced/table-generator.table.html` to view the results.
3. Switch to the Table tab in the website.
4. Interpret the results according to part 2 below.
   The reduced evaluation is sufficient to reproduce all "True" results in Table 2.
   Other statuses may be timeout or out-of-memory instead of "Unknown" due to the reduced resource limits used for the reduced evaluation.

#### Part 2
Raw execution results must be manually interpreted to yield Table 2 in the paper.
This can be done using full/reduced evaluation results from part 1, or based on the reference raw results provided in `concrat-benchmarks/results-paper/table-generator.table.html`.

The "Table" tab in the website shows results for all tools on all Concrat benchmarks in the respective status columns.
Tool output logs can be accessed by clicking on the status cell.
Instructions for interpreting the statuses and logs can be found in `concrat-benchmarks/README-results.md`.


### Finding 2

This experiment consists of 2 parts:

1. Running the tools on the extracted micro-benchmarks using BenchExec, which generates an HTML table with raw results (automated).
2. Translating the tools' raw output from the HTML table into the table included in the paper (manual).

The two parts can be done sequentially by translating the results from the automated execution,
or independently by translating the provided reference results and comparing them with the results from automated execution.

#### Part 1

##### Full evaluation
1. Run `./extracted-micro-benchmarks/run.sh` in the terminal emulator. This takes ~12 hours.
2. Run `firefox extracted-micro-benchmarks/results/table-generator.table.html` to view the results.
3. Switch to the Table tab in the website.
4. Interpret the results according to part 2 below.

##### Reduced evaluation
1. Run `./extracted-micro-benchmarks/run-reduced.sh` in the terminal emulator. This takes ~1 hour.
2. Run `firefox extracted-micro-benchmarks/results-reduced/table-generator.table.html` to view the results.
3. Switch to the Table tab in the website.
4. Interpret the results according to part 2 below.
   The reduced evaluation is sufficient to reproduce all "Correct" and "Unsound" results in Table 5.
   Other statuses may be timeout or out-of-memory instead of "Inconcl" due to the reduced resource limits used for the reduced evaluation.

#### Part 2
Raw execution results must be manually interpreted to yield Table 5 in the paper.
This can be done using full/reduced evaluation results from part 1, or based on the reference raw results provided in `extracted-micro-benchmarks/results-paper/table-generator.table.html`.

The "Table" tab in the website shows results for all tools on all Concrat benchmarks in the respective status columns.
Tool output logs can be accessed by clicking on the status cell.
Instructions for interpreting the statuses and logs can be found in `extracted-micro-benchmarks/README-results.md`.


### Finding 3

This experiment consists of 2 parts:

1. Running prevalence measurement script on the Concrat benchmarks (also excluded) and SV-COMP 2023 NoDataRace-Main category benchmarks using Joern, which generates detailed Markdown results for every benchmark and a CSV summary (automated).
2. Translating the CSV summary into the table included in the paper (manual).

The two parts can be done sequentially by translating the summary from the automated execution,
or independently by translating the provided reference summary and comparing them with the summary from automated execution.

#### Part 1

##### Full evaluation
1. Run `./joern/run.sh` in the terminal emulator. This takes ~5 hours.
2. Interpret the following summaries according to part 2 below:
   * `joern/concrat-benchmarks/results.csv`,
   * `joern/concrat-benchmarks-excluded/results.csv`,
   * `joern/sv-benchmarks/results.csv`.

##### Reduced evaluation
1. Run `./joern/run-reduced.sh` in the terminal emulator. This takes ~16 minutes.
2. Interpret the following summaries according to part 2 below:
   * `joern/concrat-benchmarks/results.csv`,
   * `joern/concrat-benchmarks-excluded/results.csv`.

#### Part 2
Raw summaries must be manually interpreted to yield Table 6 in the paper.
This can be done using full/reduced evaluation results from part 1, or based on the reference raw results provided in

   * `joern/concrat-benchmarks-paper/results.csv`,
   * `joern/concrat-benchmarks-excluded-paper/results.csv`,
   * `joern/sv-benchmarks-paper/results.csv`.

The CSV files contain tables with one row per benchmark and the columns correspond to the idioms in Table 6 (in the same order).
Values indicate how many instances of the idiom were found in the benchmark.

To get values for Table 6, count the benchmarks (Concrat or SV-COMP) where the corresponding idiom count is non-zero.
This is best done using a spreadsheet editor (e.g. Excel, LibreOffice Calc) by importing the reference CSV file from the source artifact.


## Reusability Guide

There are two reusable core pieces:

1. The Extracted Micro-benchmarks
2. The (Fixed) Concrat Benchmarks

### 1. The Extracted Micro-benchmarks

The first reusable core of the artifact is the extracted micro-benchmarks in `extracted-micro-benchmarks/`. They are in standard BenchExec and SV-COMP format, each consisting of three files:

1. An unpreprocessed `.c` file with the C source code.
2. A preprocessed `.i` file which many SV-COMP tools require (to bypass various preprocessing issues).
3. A BenchExec task definition `.yml` file with the expected verdict for the no-data-race property.

We submitted them to sv-benchmarks where they were accepted for inclusion in SV-COMP 2024. Thus, the micro-benchmarks have already been successfully reused at SV-COMP 2024 using 12 tools, including new ones.


### 2. The (Fixed) Concrat Benchmarks

The second reusable piece are the fixed Concrat benchmarks in `concrat-benchmarks/` and `concrat-benchmarks-excluded/`. The fixes are explained in `concrat-benchmarks/README.md` and in the paper.
The fixed benchmarks are also enriched by BenchExec task definition `.yml` files, which makes it trivial to evaluate any SV-COMP tool also on these real-world programs.

To evaluate new tools on either benchmarks, the tool must be integrated into BenchExec just like they are for SV-COMP. For this, we simply refer to [Tool Integration in BenchExec documentation](https://github.com/sosy-lab/benchexec/blob/main/doc/tool-integration.md).
To include new tools in our scripts, additionally do the following:

1. Create `mytool.xml` for BenchExec benchmark definition for the tool. This would be a copy of any one provided in this artifact but with tool name and options changed.
2. Add a line to `table-generator.xml` for the tool. This would be a copy of any one provided in `table-generator.xml` but with tool name changed.
3. Add a call to BenchExec to `run.sh` for the tool. This would be a copy of any one provided in `run.sh` but with tool name and path changed.
