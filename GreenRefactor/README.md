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
│   │   └── test_agents.py            # 39 pytest unit tests (100% passing)
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

### Step 1 — Setup Backend Environment

```powershell
# Navigate to the Backend directory
cd Backend

# Install required Python dependencies
pip install pytest scipy pyyaml psutil
```

---

### Step 2 — Run Unit Tests

Verify that all 35 multi-agent pipeline tests pass on your host system:

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
