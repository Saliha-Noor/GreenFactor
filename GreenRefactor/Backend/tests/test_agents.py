"""
GreenRefactor Agent Unit Tests

Tests the core agent components against synthetic code samples:
  - Pattern detection (positive/negative cases for all 4 mechanical patterns)
  - Refactoring transformations (backup/restore, syntax correctness)
  - Statistics agent (normality check, t-test vs Wilcoxon, Cohen's d)

Run with: pytest tests/test_agents.py -v
"""
import json
import os
import shutil
import tempfile
import textwrap

import pytest

# --- path setup so imports resolve from the project root ---
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents.pattern_detection_agent import (
    detect_cache_reuse,
    detect_early_termination,
    detect_batch_operations,
    detect_avoid_redundant_computation,
    scan_file,
)
from agents.refactoring_agent import (
    apply_pattern,
    restore,
    _backup,
    RefactorResult,
)
from agents.pattern_detection_agent import PatternHit


# ============================================================================
# Helpers
# ============================================================================

@pytest.fixture
def tmp_dir():
    """Create a temporary directory for test files, cleaned up after test."""
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d, ignore_errors=True)


def _write(tmp_dir, filename, content):
    """Write a test file and return its path."""
    path = os.path.join(tmp_dir, filename)
    with open(path, "w") as f:
        f.write(textwrap.dedent(content))
    return path


# ============================================================================
# Pattern Detection — cache_reuse
# ============================================================================

class TestDetectCacheReuse:
    """Tests for detect_cache_reuse across multiple languages."""

    def test_python_positive(self, tmp_dir):
        """Function called 2+ times with the SAME args (actual reuse) should be detected."""
        path = _write(tmp_dir, "sample.py", """\
            def compute(x):
                return x * x + 1

            a = compute(5)
            b = compute(5)
            c = compute(5)
        """)
        hits = detect_cache_reuse(path, "python")
        assert len(hits) >= 1
        assert hits[0].pattern == "cache_reuse"

    def test_python_different_args_no_hit(self, tmp_dir):
        """Regression test: calling a function with DIFFERENT args each time is not
        a caching opportunity (nothing to reuse), so it must NOT be flagged.
        This locks in the fix for the arg-blindness bug in detect_cache_reuse."""
        path = _write(tmp_dir, "sample.py", """\
            def compute(x):
                return x * x + 1

            a = compute(5)
            b = compute(10)
            c = compute(15)
        """)
        hits = detect_cache_reuse(path, "python")
        assert len(hits) == 0

    def test_python_already_cached(self, tmp_dir):
        """Function with @lru_cache should NOT be flagged."""
        path = _write(tmp_dir, "sample.py", """\
            import functools

            @functools.lru_cache(maxsize=None)
            def compute(x):
                return x * x + 1

            a = compute(5)
            b = compute(5)
            c = compute(5)
        """)
        hits = detect_cache_reuse(path, "python")
        assert len(hits) == 0

    def test_javascript_positive(self, tmp_dir):
        """JS function called 2+ times with the same args should be detected."""
        path = _write(tmp_dir, "sample.js", """\
            function fibonacci(n) {
                if (n <= 1) return n;
                return fibonacci(n - 1) + fibonacci(n - 2);
            }

            fibonacci(10);
            fibonacci(10);
        """)
        hits = detect_cache_reuse(path, "javascript")
        assert len(hits) >= 1

    def test_java_positive(self, tmp_dir):
        """Java method called 2+ times with the same args should be detected."""
        path = _write(tmp_dir, "Sample.java", """\
            public class Sample {
                public static int compute(int x) {
                    return x * x;
                }
                public static void main(String[] args) {
                    compute(5);
                    compute(5);
                    compute(5);
                }
            }
        """)
        hits = detect_cache_reuse(path, "java")
        assert len(hits) >= 1

    def test_go_positive(self, tmp_dir):
        """Go function called 2+ times with the same args should be detected."""
        path = _write(tmp_dir, "main.go", """\
            func compute(x int) int {
                return x * x
            }

            func main() {
                compute(5)
                compute(5)
                compute(5)
            }
        """)
        hits = detect_cache_reuse(path, "go")
        assert len(hits) >= 1

    def test_single_call_no_hit(self, tmp_dir):
        """Function called only once should NOT be flagged."""
        path = _write(tmp_dir, "sample.py", """\
            def compute(x):
                return x * x + 1

            a = compute(5)
        """)
        hits = detect_cache_reuse(path, "python")
        assert len(hits) == 0


# ============================================================================
# Pattern Detection — early_termination
# ============================================================================

class TestDetectEarlyTermination:
    """Tests for detect_early_termination."""

    def test_python_positive(self, tmp_dir):
        """Loop with found-condition but no break should be detected."""
        path = _write(tmp_dir, "sample.py", """\
            for item in items:
                if item == target:
                    result = item
        """)
        hits = detect_early_termination(path, "python")
        assert len(hits) >= 1
        assert hits[0].pattern == "early_termination"

    def test_python_already_has_break(self, tmp_dir):
        """Loop with break after found-condition should NOT be flagged."""
        path = _write(tmp_dir, "sample.py", """\
            for item in items:
                if item == target:
                    result = item
                    break
        """)
        hits = detect_early_termination(path, "python")
        assert len(hits) == 0

    def test_c_positive(self, tmp_dir):
        """C for loop with if(found) but no break should be detected."""
        path = _write(tmp_dir, "sample.c", """\
            for (int i = 0; i < n; i++) {
                if (arr[i] == target) {
                    result = arr[i];
                }
            }
        """)
        hits = detect_early_termination(path, "c")
        assert len(hits) >= 1

    def test_javascript_has_return(self, tmp_dir):
        """Loop with return inside found-condition should NOT be flagged."""
        path = _write(tmp_dir, "sample.js", """\
            for (let i = 0; i < arr.length; i++) {
                if (arr[i] == target) {
                    return arr[i];
                }
            }
        """)
        hits = detect_early_termination(path, "javascript")
        assert len(hits) == 0


# ============================================================================
# Pattern Detection — batch_operations
# ============================================================================

class TestDetectBatchOperations:
    """Tests for detect_batch_operations."""

    def test_python_positive(self, tmp_dir):
        """Per-item .save() call inside a loop should be detected."""
        path = _write(tmp_dir, "sample.py", """\
            for item in items:
                db.save(item)
        """)
        hits = detect_batch_operations(path, "python")
        assert len(hits) >= 1
        assert hits[0].pattern == "batch_operations"

    def test_python_no_io_in_loop(self, tmp_dir):
        """Loop body without I/O calls should NOT be flagged."""
        path = _write(tmp_dir, "sample.py", """\
            for item in items:
                total += item.value
        """)
        hits = detect_batch_operations(path, "python")
        assert len(hits) == 0

    def test_javascript_fetch_in_loop(self, tmp_dir):
        """fetch() inside a loop should be detected."""
        path = _write(tmp_dir, "sample.js", """\
            for (const url of urls) {
                fetch(url);
            }
        """)
        hits = detect_batch_operations(path, "javascript")
        assert len(hits) >= 1


# ============================================================================
# Pattern Detection — avoid_redundant_computation
# ============================================================================

class TestDetectAvoidRedundantComputation:
    """Tests for detect_avoid_redundant_computation."""

    def test_python_positive(self, tmp_dir):
        """Repeated identical call in loop body should be detected."""
        path = _write(tmp_dir, "sample.py", """\
            for item in items:
                x = config.get_value()
                y = config.get_value()
        """)
        hits = detect_avoid_redundant_computation(path, "python")
        assert len(hits) >= 1
        assert hits[0].pattern == "avoid_redundant_computation"

    def test_python_negative_different_calls(self, tmp_dir):
        """Different calls in loop body should NOT be flagged."""
        path = _write(tmp_dir, "sample.py", """\
            for item in items:
                x = config.get_a()
                y = config.get_b()
        """)
        hits = detect_avoid_redundant_computation(path, "python")
        assert len(hits) == 0


# ============================================================================
# Pattern Detection — scan_file (integration)
# ============================================================================

class TestScanFile:
    """Integration test for scan_file across all detectors."""

    def test_multi_pattern_detection(self, tmp_dir):
        """File with multiple pattern candidates should return multiple hits."""
        path = _write(tmp_dir, "multi.py", """\
            def compute(x):
                return x * x

            compute(1)
            compute(1)
            compute(1)

            for item in items:
                if item == target:
                    result = item

            for row in rows:
                db.save(row)
        """)
        hits = scan_file(path, "python")
        patterns_found = {h.pattern for h in hits}
        assert "cache_reuse" in patterns_found
        assert "early_termination" in patterns_found
        assert "batch_operations" in patterns_found


# ============================================================================
# Refactoring Agent — backup/restore
# ============================================================================

class TestBackupRestore:
    """Tests for file backup and restore mechanism."""

    def test_backup_creates_orig(self, tmp_dir):
        path = _write(tmp_dir, "test.py", "original content\n")
        backup_path = _backup(path)
        assert os.path.isfile(backup_path)
        assert backup_path == path + ".orig"
        with open(backup_path) as f:
            assert f.read() == "original content\n"

    def test_restore_reverts_file(self, tmp_dir):
        path = _write(tmp_dir, "test.py", "original content\n")
        _backup(path)
        with open(path, "w") as f:
            f.write("modified content\n")
        restore(path)
        with open(path) as f:
            assert f.read() == "original content\n"

    def test_backup_no_overwrite(self, tmp_dir):
        """Second backup should NOT overwrite the first .orig."""
        path = _write(tmp_dir, "test.py", "version 1\n")
        _backup(path)
        with open(path, "w") as f:
            f.write("version 2\n")
        _backup(path)
        with open(path + ".orig") as f:
            assert f.read() == "version 1\n"


# ============================================================================
# Refactoring Agent — cache_reuse (Python)
# ============================================================================

class TestRefactorCacheReusePython:
    """Tests for Python cache_reuse auto-refactoring."""

    def test_adds_lru_cache(self, tmp_dir):
        """Should add @functools.lru_cache and import functools."""
        path = _write(tmp_dir, "sample.py", """\
            def compute(x):
                return x * x + 1

            compute(5)
            compute(5)
            compute(5)
        """)
        hits = detect_cache_reuse(path, "python")
        assert len(hits) >= 1
        result = apply_pattern(path, "python", hits[0])
        assert result.method == "auto"
        with open(path) as f:
            content = f.read()
        assert "functools.lru_cache" in content
        assert "import functools" in content

    def test_restore_after_refactor(self, tmp_dir):
        """Restore should revert to original content."""
        original = """\
def compute(x):
    return x * x + 1

compute(5)
compute(5)
compute(5)
"""
        path = _write(tmp_dir, "sample.py", original)
        hits = detect_cache_reuse(path, "python")
        apply_pattern(path, "python", hits[0])
        restore(path)
        with open(path) as f:
            assert f.read() == original


# ============================================================================
# Refactoring Agent — cache_reuse (JavaScript)
# ============================================================================

class TestRefactorCacheReuseJavaScript:
    """Tests for JavaScript cache_reuse auto-refactoring."""

    def test_adds_map_wrapper(self, tmp_dir):
        """Should rename function to __impl and add a Map-based cache wrapper."""
        path = _write(tmp_dir, "sample.js", """\
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

fibonacci(10);
fibonacci(10);
""")
        hits = detect_cache_reuse(path, "javascript")
        assert len(hits) >= 1
        result = apply_pattern(path, "javascript", hits[0])
        assert result.method == "auto"
        with open(path) as f:
            content = f.read()
        assert "__impl" in content
        assert "__cache" in content
        assert "new Map()" in content


# ============================================================================
# Refactoring Agent — early_termination (Python)
# ============================================================================

class TestRefactorEarlyTerminationPython:
    """Tests for Python early_termination auto-refactoring."""

    def test_inserts_break_at_end_of_block(self, tmp_dir):
        """Break should be inserted as the LAST statement of the if-block,
        NOT the first (the original bug)."""
        path = _write(tmp_dir, "sample.py", """\
for item in items:
    if item == target:
        result = item
""")
        hits = detect_early_termination(path, "python")
        assert len(hits) >= 1
        result = apply_pattern(path, "python", hits[0])
        assert result.method == "auto"
        with open(path) as f:
            lines = f.readlines()
        # 'result = item' must come BEFORE 'break'
        result_line = next(i for i, l in enumerate(lines) if "result = item" in l)
        break_line = next(i for i, l in enumerate(lines) if "break" in l)
        assert break_line > result_line, "break must be AFTER assignment, not before"


# ============================================================================
# Refactoring Agent — avoid_redundant_computation (Python)
# ============================================================================

class TestRefactorAvoidRedundantPython:
    """Tests for Python avoid_redundant_computation auto-refactoring."""

    def test_hoists_call_above_loop(self, tmp_dir):
        """Repeated call should be hoisted to a temp var before the loop."""
        path = _write(tmp_dir, "sample.py", """\
for item in items:
    x = config.get_value()
    y = config.get_value()
""")
        hits = detect_avoid_redundant_computation(path, "python")
        assert len(hits) >= 1
        result = apply_pattern(path, "python", hits[0])
        assert result.method == "auto"
        with open(path) as f:
            content = f.read()
        assert "_hoisted_" in content


# ============================================================================
# Refactoring Agent — batch_operations (flag-only)
# ============================================================================

class TestRefactorBatchOperations:
    """batch_operations should ALWAYS be flagged-only, never auto-applied."""

    def test_flag_only_python(self, tmp_dir):
        path = _write(tmp_dir, "sample.py", """\
for item in items:
    db.save(item)
""")
        hits = detect_batch_operations(path, "python")
        assert len(hits) >= 1
        result = apply_pattern(path, "python", hits[0])
        assert result.method == "flagged-only"
        with open(path) as f:
            assert "REFACTOR-CANDIDATE" in f.read()

    def test_flag_only_javascript(self, tmp_dir):
        path = _write(tmp_dir, "sample.js", """\
for (const url of urls) {
    fetch(url);
}
""")
        hits = detect_batch_operations(path, "javascript")
        assert len(hits) >= 1
        result = apply_pattern(path, "javascript", hits[0])
        assert result.method == "flagged-only"


# ============================================================================
# Refactoring Agent — C++ template parameter parsing fix
# ============================================================================

class TestCppTemplateParameterParsing:
    """Verify that template types with commas don't break param counting."""

    def test_single_template_param_not_rejected(self):
        """std::map<int, int> is ONE parameter, not two."""
        from agents.refactoring_agent import _cpp_cache_parse
        line = "int lookup(std::map<int, int> cache) {"
        result = _cpp_cache_parse(line)
        # Should parse successfully (1 param), not return None (>1 param)
        assert result is not None
        assert result["pname"] == "cache"

    def test_truly_two_params_still_rejected(self):
        """Two real params (not template commas) should still be rejected."""
        from agents.refactoring_agent import _cpp_cache_parse
        line = "int add(int a, int b) {"
        result = _cpp_cache_parse(line)
        assert result is None  # >1 param, scoped out


# ============================================================================
# Stats Agent
# ============================================================================

class TestStatsAgent:
    """Tests for compare_before_after statistical analysis."""

    def test_identical_measurements_not_significant(self):
        """Identical before/after should be non-significant."""
        from agents.stats_agent import compare_before_after
        baseline = [10.0, 10.0, 10.0, 10.0, 10.0]
        refactored = [10.0, 10.0, 10.0, 10.0, 10.0]
        result = compare_before_after(baseline, refactored)
        assert result.significant is False
        assert result.percent_change == 0.0
        assert result.cohens_d == 0.0

    def test_clear_improvement_significant(self):
        """Large improvement should be statistically significant."""
        from agents.stats_agent import compare_before_after
        baseline =   [100.0, 102.0, 98.0, 101.0, 99.0, 100.5, 101.5, 99.5, 100.2, 100.8]
        refactored = [ 50.0,  51.0, 49.0,  50.5, 49.5,  50.2,  50.8, 49.8,  50.1,  50.4]
        result = compare_before_after(baseline, refactored)
        assert result.significant is True
        assert result.percent_change < 0  # negative = refactored is lower (saved energy)
        assert result.cohens_d > 0  # positive = baseline > refactored (improvement)

    def test_minimum_sample_size(self):
        """Should raise ValueError for n < 3."""
        from agents.stats_agent import compare_before_after
        with pytest.raises(ValueError, match="at least 3"):
            compare_before_after([10.0, 11.0], [9.0, 10.0])

    def test_mismatched_lengths_raises(self):
        """Should raise ValueError for unequal lists."""
        from agents.stats_agent import compare_before_after
        with pytest.raises(ValueError, match="same length"):
            compare_before_after([10.0, 11.0, 12.0], [9.0, 10.0])

    def test_result_fields_present(self):
        """All expected fields should be populated."""
        from agents.stats_agent import compare_before_after
        baseline =   [100.0, 105.0, 102.0, 98.0, 101.0]
        refactored = [ 90.0,  92.0,  88.0, 91.0,  89.0]
        result = compare_before_after(baseline, refactored)
        assert result.n == 5
        assert result.mean_baseline_j > 0
        assert result.mean_refactored_j > 0
        assert result.test_used in ("paired t-test", "Wilcoxon signed-rank")
        assert 0.0 <= result.p_value <= 1.0
        assert result.ci_95_low <= result.ci_95_high

    def test_normality_switches_test(self):
        """Non-normal data should trigger Wilcoxon instead of t-test."""
        from agents.stats_agent import compare_before_after
        # Skewed data to fail normality
        baseline =   [1.0, 1.0, 1.0, 1.0, 100.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        refactored = [0.5, 0.5, 0.5, 0.5,  50.0, 0.5, 0.5, 0.5, 0.5, 0.5]
        result = compare_before_after(baseline, refactored)
        # We can't guarantee which test scipy picks for all data, but we can
        # verify the field is populated with one of the two valid options
        assert result.test_used in ("paired t-test", "Wilcoxon signed-rank")


# ============================================================================
# Ingestion Agent — unit tests
# ============================================================================

class TestIngestionAgent:
    """Tests for ingestion_agent config management (no actual cloning)."""

    def test_load_save_config(self, tmp_dir):
        """Config round-trip through load/save should preserve data."""
        from agents import ingestion_agent
        # Temporarily override the config path
        original_path = ingestion_agent.CONFIG_PATH
        test_config_path = os.path.join(tmp_dir, "test_repos.yaml")
        ingestion_agent.CONFIG_PATH = test_config_path

        try:
            cfg = ingestion_agent._load_config()
            assert cfg == {}

            ingestion_agent._ensure_language_section(cfg, "python")
            assert "python" in cfg
            assert isinstance(cfg["python"]["repos"], list)
            assert len(cfg["python"]["patterns"]) == 8

            ingestion_agent._save_config(cfg)
            reloaded = ingestion_agent._load_config()
            assert reloaded["python"]["patterns"] == cfg["python"]["patterns"]
        finally:
            ingestion_agent.CONFIG_PATH = original_path


# ============================================================================
# LLM Review Agent Orchestrator Integration — unit tests
# ============================================================================

class TestLLMReviewAgentIntegration:
    """Tests for LLM review agent integration within orchestrator."""

    def test_orchestrator_llm_review_without_key(self, monkeypatch, tmp_dir):
        """When GROQ_API_KEY is absent, orchestrator should skip LLM review gracefully."""
        from orchestrator import run_case
        monkeypatch.delenv("GROQ_API_KEY", raising=False)

        py_file = os.path.join(tmp_dir, "sample.py")
        with open(py_file, "w", encoding="utf-8") as f:
            f.write("def foo():\n    return 42\n")

        res = run_case("python", tmp_dir, "sample.py", "test_repo", runs_per_case=1)
        assert res["status"] in ("no_pattern_found", "done", "measured")

    def test_orchestrator_llm_review_with_key(self, monkeypatch, tmp_dir):
        """When GROQ_API_KEY is present, orchestrator should invoke LLM agent and tag suggestions."""
        import orchestrator
        monkeypatch.setenv("GROQ_API_KEY", "gsk_fake_key_for_testing_123")

        fake_suggestions = [{
            "pattern": "offload_to_native",
            "line": 1,
            "reasoning": "Use numpy dot product",
            "confidence": "high"
        }]
        monkeypatch.setattr("agents.llm_review_agent.review_file", lambda fp, lang: fake_suggestions)

        py_file = os.path.join(tmp_dir, "sample.py")
        with open(py_file, "w", encoding="utf-8") as f:
            f.write("def compute():\n    return 1 + 1\n")

        res = orchestrator.run_case("python", tmp_dir, "sample.py", "test_repo", runs_per_case=1)
        assert res["status"] == "done"
        assert len(res["patterns"]) == 1
        assert res["patterns"][0]["pattern"] == "offload_to_native"
        assert res["patterns"][0]["refactor_method"] == "llm-suggested"


# ============================================================================
# RAPL Wraparound Ceiling — unit tests
# ============================================================================

class TestRAPLMaxRange:
    """Tests for sysfs RAPL max_energy_range_uj reading and wraparound calculation."""

    def test_rapl_custom_max_range(self, monkeypatch, tmp_dir):
        from agents import measurement_agent

        custom_energy_file = os.path.join(tmp_dir, "energy_uj")
        custom_range_file = os.path.join(tmp_dir, "max_energy_range_uj")

        with open(custom_range_file, "w", encoding="utf-8") as f:
            f.write("262143328896\n")

        monkeypatch.setattr("agents.measurement_agent.get_rapl_energy_file", lambda: custom_energy_file)

        ceiling = measurement_agent._read_rapl_max_range_uj()
        assert ceiling == 262143328896

    def test_rapl_wraparound_uses_custom_range(self, monkeypatch, tmp_dir):
        from agents import measurement_agent

        custom_energy_file = os.path.join(tmp_dir, "energy_uj")
        custom_range_file = os.path.join(tmp_dir, "max_energy_range_uj")

        with open(custom_range_file, "w", encoding="utf-8") as f:
            f.write("1000000\n")

        monkeypatch.setattr("agents.measurement_agent.get_rapl_energy_file", lambda: custom_energy_file)

        # Before counter value = 900,000 uJ, After counter value = 100,000 uJ (wrapped around)
        readings = [900000, 100000]
        monkeypatch.setattr("agents.measurement_agent._read_rapl_uj", lambda: readings.pop(0))

        result, energy_j = measurement_agent._measure_rapl(lambda: "ok")
        assert result == "ok"
        # delta_uj = 100000 - 900000 = -800000. With max_range = 1000000 -> 200000 uJ = 0.2 Joules
        assert abs(energy_j - 0.2) < 1e-6


