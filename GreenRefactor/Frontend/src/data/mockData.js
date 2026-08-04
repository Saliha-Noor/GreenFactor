// Pre-loaded realistic research benchmark dataset for GreenRefactor UI

export const mockSummaryData = {
  experiment_info: {
    total_repos_configured: 120,
    repos_evaluated: 120,
    languages_supported: 8,
    target_languages: ["python", "javascript", "java", "csharp", "c", "cpp", "go", "rust"],
    timestamp: "2026-07-28 12:30:00",
    measurement_mode: "RAPL / TDP Dual-Mode"
  },
  rq1_language_summary: {
    python: { repos: 15, mean_savings_percent: 18.4, significant_count: 12, avg_cohens_d: 1.42, primary_pattern: "cache_reuse" },
    javascript: { repos: 15, mean_savings_percent: 15.2, significant_count: 11, avg_cohens_d: 1.18, primary_pattern: "early_termination" },
    java: { repos: 15, mean_savings_percent: 12.8, significant_count: 10, avg_cohens_d: 0.95, primary_pattern: "cache_reuse" },
    csharp: { repos: 15, mean_savings_percent: 11.6, significant_count: 9, avg_cohens_d: 0.88, primary_pattern: "avoid_redundant_computation" },
    cpp: { repos: 15, mean_savings_percent: 8.9, significant_count: 8, avg_cohens_d: 0.74, primary_pattern: "cache_reuse" },
    c: { repos: 15, mean_savings_percent: 7.4, significant_count: 7, avg_cohens_d: 0.62, primary_pattern: "early_termination" },
    go: { repos: 15, mean_savings_percent: 9.8, significant_count: 9, avg_cohens_d: 0.79, primary_pattern: "avoid_redundant_computation" },
    rust: { repos: 15, mean_savings_percent: 6.2, significant_count: 5, avg_cohens_d: 0.51, primary_pattern: "early_termination" }
  },
  rq2_runtime_summary: {
    "Interpreted-JIT (Python, JS)": { repos: 30, mean_savings_percent: 16.8, avg_cohens_d: 1.30, impact_rating: "High" },
    "Managed-JIT (Java, C#)": { repos: 30, mean_savings_percent: 12.2, avg_cohens_d: 0.91, impact_rating: "Moderate-High" },
    "Compiled-Native (C, C++, Go, Rust)": { repos: 60, mean_savings_percent: 8.1, avg_cohens_d: 0.66, impact_rating: "Moderate" }
  },
  overall_stats: {
    mean_energy_savings_pct: 11.29,
    significant_refactor_rate_pct: 70.0,
    total_refactors_applied: 84,
    total_refactors_flagged_only: 36,
    avg_effect_size_cohens_d: 0.89
  }
};

export const mockPatternCatalog = [
  {
    id: "early_termination",
    name: "Early Termination",
    category: "Control Flow",
    complexity: "Mechanical (line/regex heuristic)",
    description: "Inserts explicit `break` or `return` inside search loops as soon as the target condition is satisfied, preventing unnecessary loop iterations.",
    supported_languages: ["Python", "JavaScript", "Java", "C#", "C", "C++", "Go", "Rust"],
    avg_energy_saving: "14.2%",
    risk_level: "Low",
    before_code: `for item in items:\n    if item == target:\n        result = item`,
    after_code: `for item in items:\n    if item == target:\n        result = item\n        break  # GreenRefactor: Early termination`
  },
  {
    id: "cache_reuse",
    name: "Cache Reuse & Memoization",
    category: "Memory & Computation",
    complexity: "Mechanical (line/regex heuristic)",
    description: "Caches outputs of pure idempotent functions using LRU cache decorators or hash maps to eliminate redundant recalculation on repeated inputs.",
    supported_languages: ["Python", "JavaScript", "Java", "C#", "C++", "C", "Go"],
    avg_energy_saving: "22.5%",
    risk_level: "Low-Medium",
    before_code: `def compute(x):\n    return expensive_math(x)\n\na = compute(5)\nb = compute(5)`,
    after_code: `import functools\n\n@functools.lru_cache(maxsize=None)\ndef compute(x):\n    return expensive_math(x)\n\na = compute(5)\nb = compute(5)`
  },
  {
    id: "avoid_redundant_computation",
    name: "Avoid Redundant Computation",
    category: "Loop Invariants",
    complexity: "Mechanical (line/regex heuristic)",
    description: "Hoists loop-invariant expressions and function calls outside loop bodies so they are evaluated once rather than N times.",
    supported_languages: ["Python", "JavaScript", "Java", "C#", "C", "C++", "Go", "Rust"],
    avg_energy_saving: "11.8%",
    risk_level: "Low",
    before_code: `for item in items:\n    x = config.get_value()\n    process(item, x)`,
    after_code: `_hoisted_config_0 = config.get_value()\nfor item in items:\n    x = _hoisted_config_0\n    process(item, x)`
  },
  {
    id: "batch_operations",
    name: "Batch Operations",
    category: "I/O & Networking",
    complexity: "Flagged-Only (Manual Review)",
    description: "Identifies per-item I/O calls or DB saves inside loops and flags them to be grouped into bulk batch transactions.",
    supported_languages: ["Python", "JavaScript", "Java", "C#", "Go"],
    avg_energy_saving: "35.1%",
    risk_level: "High",
    before_code: `for row in rows:\n    db.save(row)`,
    after_code: `# REFACTOR-CANDIDATE [batch_operations]: Consider batching db.save()\nfor row in rows:\n    db.save(row)`
  },
  {
    id: "offload_to_native",
    name: "Offload to Native Execution",
    category: "Language Interop",
    complexity: "Semantic Review",
    description: "Replaces high-frequency interpreted loops with native C/C++ or SIMD-accelerated library calls.",
    supported_languages: ["Python", "JavaScript"],
    avg_energy_saving: "42.0%",
    risk_level: "Medium",
    before_code: `total = 0\nfor x in arr:\n    total += x * x`,
    after_code: `import numpy as np\ntotal = np.dot(arr, arr)`
  },
  {
    id: "high_perf_libraries",
    name: "High-Performance Libraries",
    category: "Dependencies",
    complexity: "Semantic Review",
    description: "Replaces standard standard-library utilities with optimized zero-copy or parallel implementations (e.g. simdjson, ujson, abseil).",
    supported_languages: ["Python", "JavaScript", "C++", "Java", "Rust"],
    avg_energy_saving: "19.4%",
    risk_level: "Medium",
    before_code: `import json\ndata = json.loads(text)`,
    after_code: `import orjson  # High-performance C-accelerated JSON\ndata = orjson.loads(text)`
  },
  {
    id: "high_perf_data_structures",
    name: "High-Performance Data Structures",
    category: "Data Structures",
    complexity: "Semantic Review",
    description: "Swaps generic collections for cache-friendly contiguously allocated or lock-free data structures.",
    supported_languages: ["Java", "C#", "C++", "Go", "Rust"],
    avg_energy_saving: "16.3%",
    risk_level: "Medium",
    before_code: `List<Integer> list = new ArrayList<>();`,
    after_code: `IntArrayList list = new IntArrayList();  # Primitive unboxed array list`
  },
  {
    id: "swap_library_impl",
    name: "Swap Library Implementation",
    category: "Dependencies",
    complexity: "Semantic Review",
    description: "Replaces heavy abstractions with lightweight zero-dependency energy-efficient alternatives.",
    supported_languages: ["Python", "JavaScript", "Java", "C#"],
    avg_energy_saving: "14.7%",
    risk_level: "Medium-High",
    before_code: `const moment = require('moment');`,
    after_code: `const dayjs = require('dayjs');  # 2KB replacement for 70KB moment`
  }
];

export const mockDiffSamples = [];

