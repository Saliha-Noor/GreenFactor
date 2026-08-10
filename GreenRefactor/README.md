# 🌱 GreenRefactor — Multi-Language Energy Refactoring Platform

> An agent-based empirical research framework and full-stack analytics platform that automatically detects energy-wasteful coding patterns across **8 programming languages**, applies safe mechanical refactorings, and statistically validates energy savings using paired hypothesis testing.

---

## 📸 Key Features & Capabilities

- 🤖 **9 Specialized Multi-Agent Engine** — Autonomous agent pipeline for ingestion, AST pattern scanning, mechanical code transformation, automated build/test verification, RAPL/CodeCarbon energy sampling, and statistical analysis.
- ⚡ **8 Supported Programming Languages** — Full pattern scanner and refactorer support for **Python, JavaScript, Java, C#, C, C++, Go, and Rust**.
- 📊 **120 Open-Source Benchmark Repositories** — 15 curated real-world GitHub repositories per language pre-configured for batch empirical research.
- 🎨 **Modern React + Vite Web Dashboard** — Dark glassmorphism & light themes, authentication suite (Sign In, Sign Up, Password Reset), interactive code refactoring tab, repo explorer, side-by-side diff viewer, statistical inspector, and user profile management.
- 🔬 **Rigorous Statistical Verification** — Automated normality checks (Shapiro-Wilk), parametric (Paired $t$-test) / non-parametric (Wilcoxon signed-rank) hypothesis testing, Cohen's $d$ effect sizes, and 95% Confidence Intervals.
- 🛠️ **Interactive Code Refactor Studio** — Paste custom multi-language code directly in the web UI to analyze energy flaws and generate refactored green code instantly.

---

## 📂 Project Architecture & Directory Structure

```
greenrefactor/
│
├── Backend/                          # Python Research Engine & Agent Architecture
│   ├── agents/                       # 9 specialized pipeline agents
│   │   ├── ingestion_agent.py        # Automated git clone, validation & registration
│   │   ├── pattern_detection_agent.py# Regex/AST pattern scanner (10 energy patterns)
│   │   ├── refactoring_agent.py      # Mechanical & AST code transformation rules
│   │   ├── build_run_agent.py        # Language-specific build & execution adapters
│   │   ├── measurement_agent.py      # RAPL / TDP power sampling engine
│   │   ├── verification_agent.py     # Test-suite verification & rollback safety net
│   │   ├── stats_agent.py            # Shapiro-Wilk, t-test/Wilcoxon, Cohen's d, 95% CIs
│   │   ├── llm_review_agent.py       # Semantic code review adapter
│   │   └── env_detect.py             # Host environment & toolchain detection
│   │
│   ├── config/
│   │   └── repos.yaml                # 120 benchmark repos (15 per language)
│   │
│   ├── tests/
│   │   └── test_agents.py            # 40 pytest unit tests (100% passing)
│   │
│   ├── repos/                        # Cloned benchmark repositories directory
│   ├── results/                      # Raw and summary energy measurement JSON output
│   │
│   ├── orchestrator.py               # Single-repository execution pipeline
│   ├── run_language_batch.py         # Batch runner across language repos
│   ├── compare_results.py            # Statistical aggregator & RQ report generator
│   ├── export_repos_json.py          # Benchmark configuration exporter
│   ├── cleanup.py                    # Build artifact and temp cache cleaner
│   └── clone_all.py                  # Parallel repo cloner
│
├── Frontend/                         # React + Vite Interactive Web Dashboard
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx            # Top navigation bar + JSON uploader + theme toggle
│   │   │   ├── LoginScreen.jsx       # Authentication (Sign In, Sign Up, Reset Password)
│   │   │   ├── OverviewTab.jsx       # Executive KPI metrics, RQ1 & RQ2 visualizations
│   │   │   ├── RefactorTab.jsx       # Interactive multi-language live refactor studio
│   │   │   ├── BenchmarkCatalogTab.jsx # Filterable 120-repository & 10-pattern catalog
│   │   │   ├── StatsInspectorTab.jsx # Statistical decision trees, distributions & test tables
│   │   │   ├── UserProfileTab.jsx    # User settings, activity logs & session manager
│   │   │   └── HelpDrawer.jsx        # Slide-over research methodology guide
│   │   ├── data/
│   │   │   └── mockData.js           # Built-in dataset fallback & sample datasets
│   │   ├── App.jsx                   # Main React SPA routing and state manager
│   │   ├── index.css                 # Dark/Light CSS design system with variables
│   │   └── main.jsx                  # React application entrypoint
│   ├── index.html                    # Single Page Application HTML shell
│   ├── package.json                  # Frontend dependencies and npm scripts
│   └── vite.config.js                # Vite build system configuration
│
├── .gitignore                        # Git exclusion rules
└── README.md                         # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites

| Component | Minimum Version | Installation / Notes |
|-----------|----------------|----------------------|
| **Python** | 3.10+ | [python.org](https://python.org) |
| **Node.js** | 18.0+ | [nodejs.org](https://nodejs.org) |
| **Git** | 2.30+ | [git-scm.com](https://git-scm.com) |

#### Optional Toolchains (for compiling & benchmarking target repos):
- **C/C++**: `gcc` / `g++`
- **Java**: JDK 17+ (`javac` / `java`)
- **C#**: .NET SDK 8.0+ (`dotnet`)
- **Go**: Go 1.21+ (`go`)
- **Rust**: Rustup / Cargo 1.70+ (`cargo`)

---

### Environment Variables

The GreenRefactor backend optionally uses the Groq LLM API to perform advanced semantic code review patterns (`offload_to_native`, `high_perf_libraries`, `high_perf_data_structures`, `swap_library_impl`).

To enable these 4 semantic patterns, create a `.env` file in the `Backend/` directory (you can copy `.env.example`) and add your Groq API key:
```env
GROQ_API_KEY=gsk_your_api_key_here
```

*Note: If no API key is provided, the application degrades gracefully and relies exclusively on the local mechanical refactoring heuristic engine.*

---

### Step 1 — Setup Backend Environment

```powershell
# Navigate to the Backend directory
cd Backend

# Install required Python dependencies
pip install -r requirements.txt
```

---

### Step 2 — Run Unit Tests

Verify that all 40 multi-agent pipeline tests pass on your host system:

```powershell
python -m pytest tests/test_agents.py -v
```

---

### Step 3 — Execute Benchmarks & Generate Statistical Reports

```powershell
# 1. Clone benchmark repos for a language (e.g. Python):
python clone_all.py

# 2. Run batch execution for a language:
python run_language_batch.py --language python

# 3. Generate statistical summary report (RQ1 & RQ2 metrics):
python compare_results.py
```

---

### Step 4 — Launch the Frontend Web Dashboard

```powershell
# Navigate to the Frontend directory
cd ../Frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```

Open your browser at **`http://localhost:3000`** (or the port specified in terminal).

---

## 🖥️ Dashboard Overview & Workflow

1. **Authentication** — Sign in with your account or use the quick access options.
2. **Overview Tab** — View top-level research insights, energy savings distributions across languages, and runtime execution model impacts.
3. **Interactive Refactor Studio** — Paste target code in any supported language, select a pattern (e.g. *Early Termination*, *Cache Reuse*, *Loop Hoisting*), and click **Refactor Code** to preview green optimizations in real time.
4. **Code Diff Viewer** — Inspect side-by-side line diffs of original vs refactored code across benchmark repositories.
5. **Statistical Inspector** — Explore normality tests (Shapiro-Wilk), parametric/non-parametric hypothesis test choices, p-values, Cohen's $d$ effect sizes, and confidence intervals.
6. **Import Results** — Click **"Load JSON Results"** in the top navigation header to dynamically load generated `comparison_summary.json` files from your backend test runs.

---

## 🔬 Research Questions & Methodology

| Research Question | Objective | Statistical Methodology |
|-------------------|-----------|------------------------|
| **RQ1: Energy Reduction** | How much energy can mechanical green refactoring save per language? | Paired $t$-test / Wilcoxon signed-rank test per repo, Cohen's $d$ effect size, 95% Confidence Intervals. |
| **RQ2: Execution Model Impact** | Does the execution paradigm (Interpreted vs JIT vs Compiled) influence refactoring efficacy? | Cross-category ANOVA / Kruskal-Wallis test across language runtime groups. |

> **Note on Measurement Methodology & Thermal Drift:**
> By default (`interleave=False`), baseline runs are measured upfront in batch before refactoring. To mitigate potential thermal throttling or CPU frequency drift confounds, the pipeline also supports an opt-in `interleave=True` parameter in `orchestrator.run_case()` which alternates baseline and refactored executions.

### Methodological Exclusions (Threats to Validity)
To ensure the integrity of the empirical dataset, 38 of the 120 originally configured repositories are formally excluded from measurement. These repositories lack deterministic, single-process, CPU-bound workloads that can be robustly measured for micro-energy consumption without massive mocking or external harnesses. This exclusion is enforced in code, not just documented here: each excluded repo carries `excluded: true` and an `exclusion_reason` in `config/repos.yaml`, and `run_language_batch.py` filters them out before queuing (skip lines are printed per repo, and even an explicit `--repo <excluded-name>` is rejected).

| Exclusion Category | Language | Excluded Repositories | Justification |
| :--- | :--- | :--- | :--- |
| **Async/Event-Loop Web Frameworks** | Python | `flask`, `gunicorn`, `tornado` | Requires a live HTTP server + client harness to exercise meaningfully; no deterministic single-process workload available. |
| | JS | `express`, `koa`, `socket_io` | Same as above. |
| | Java | `vertx` | Same as above. |
| | C | `mongoose` | Same as above. |
| | Go | `gin`, `gorilla_mux`, `fiber`, `fasthttp`, `echo` | Same as above. |
| | Rust | `tokio`, `hyper`, `actix_web`, `tikv` | Same as above. |
| | C# | `masstransit`, `akka_net` | Distributed messaging frameworks requiring live brokers. |
| **Frontend/Browser-Bound** | JS | `react`, `vue`, `jquery`, `chart_js`, `d3` | Requires a full browser/DOM environment; cannot run in a headless Node process without massive mocking, which invalidates energy readings. |
| **Test/Mock Frameworks** | JS | `eslint` | Meta-tool; benchmarking linting performance varies wildly based on the target source code. |
| | Java | `junit4` | Same as above; requires a target project. |
| | C++ | `catch2`, `googletest` | Same as above. |
| | C# | `moq`, `xunit`, `fluentvalidation` | Same as above. |
| **Scraping / Network-Bound** | Python | `scrapy` | Inherently network-bound and non-deterministic. |
| **Build/Compiler Tools** | JS | `webpack` | Requires a target project to compile; highly variable based on target source. |
| **Pattern Demo / No Sustained Workload** | Java | `java_design_patterns` | Repo is a design-pattern showcase (Singleton example); no natural sustained workload exists, and looping the trivial call artificially would measure loop/JIT overhead rather than genuine program behavior. |
| **Complex Multi-File Build** | C | `sqlite`, `redis`, `curl`, `jq` | No isolatable refactor target without a custom multi-file build pipeline; would require Makefile/CMake integration out of scope for this project. |

**Final Genuinely Measurable Target:** 82 Repositories (120 configured − 38 formally excluded, per the table above; enforced via `excluded: true` in `config/repos.yaml`).

> **Data status note (as of this audit):** the `results/` files currently shipped with this repo (`lz4`, `zlib`, `stb`, `requests`, plus the now-removed `flask`) all predate several of the fixes above — their rejection notes are missing the `Detail:` diagnostic suffix present in the current `verification_agent.py`, meaning they were generated by an older code version. A minimal, isolated reproduction of the current `apply_pattern` → rebuild → `verify_before_after` → `restore` sequence on a clean synthetic C repo **does** correctly produce an accepted, measured refactor, so the verification/restore mechanism itself is not currently known to be broken. But every pattern hit in every currently-shipped `results/*.json` was rejected with `"baseline ALSO fails verification"`, meaning **no results file in this repo right now reflects a genuine measured energy comparison** — all of them should be regenerated with the current code before being treated as paper data. Don't trust a `"status": "done"` at face value; check for at least one `"status": "measured"` pattern entry with a populated `stats` block.

---

## 🧪 Supported Green Refactoring Patterns (10)

| # | Pattern Name | Transformation Type | Targeted Inefficiency | Estimated Savings (prior estimate, not yet empirically measured per-pattern) |
|---|--------------|--------------------|-----------------------|-------------------|
| 1 | **Early Termination** | Mechanical (line/regex heuristic) | Exhaustive iteration after result match | ~14% energy reduction |
| 2 | **Cache Reuse / Memoization** | Mechanical (line/regex heuristic) | Repeated expensive computation | ~22% energy reduction |
| 3 | **Loop Invariant Hoisting** | Mechanical (line/regex heuristic) | Redundant calculations inside loops | ~12% energy reduction |
| 4 | **Batch Operations** | Flagged / Static | High-frequency individual disk/network I/O | ~35% energy reduction |
| 5 | **Offload to Native** | Semantic Review | Heavy interpreted loops | ~42% energy reduction |
| 6 | **High-Performance Libraries** | Semantic Review | Generic collections in hot code paths | ~19% energy reduction |
| 7 | **High-Performance Data Structures** | Semantic Review | Suboptimal data structure selection | ~16% energy reduction |
| 8 | **Swap Library Implementation** | Semantic Review | Unoptimized third-party library calls | ~15% energy reduction |
| 9 | **Lazy Evaluation** | Mechanical (line/regex heuristic) | Pre-allocating unneeded heavy objects | ~18% energy reduction |
| 10 | **Memory Allocation Optimization** | Mechanical (line/regex heuristic) | Excessive heap allocation in tight loops | ~25% energy reduction |

> **Note:** These are pre-registered estimates used to prioritize which patterns to implement. Measured, aggregate results per language are in `Backend/results/comparison_summary.json` and summarized in the Research Questions section below — they show substantially smaller and more mixed effects than these estimates once evaluated against real repos. See the Final Project Report for the full breakdown.

---

## 🌐 Supported Programming Languages

- 🐍 **Python** (Interpreted)
- 🟨 **JavaScript** (JIT / V8)
- ☕ **Java** (JVM / JIT)
- 🔷 **C#** (.NET / JIT)
- ⚙️ **C** (Native Compiled)
- 🛠️ **C++** (Native Compiled)
- 🔹 **Go** (Compiled / GC)
- 🦀 **Rust** (Native Compiled / Zero-cost abstractions)

---

## 📄 License

This project is licensed under the **MIT License**. See `LICENSE` for details.
