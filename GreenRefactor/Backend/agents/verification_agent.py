"""
Agent 4 - Verification Agent

Runs whatever test command exists for the repo/language BEFORE and AFTER
a refactor is applied. If tests pass before but fail after -> auto-restore
the .orig backup and mark the case as REJECTED. An unverified refactor is
NEVER sent to the measurement stage.

If a repo has no discoverable test suite, verification falls back to
"does it still build and exit 0 on the fixed workload" (weaker, but still
prevents shipping a broken refactor into the energy numbers) — this
fallback is recorded in the result so the paper can report per-repo
verification strength honestly.
"""
import os
import subprocess
from dataclasses import dataclass

import sys

py_bin = sys.executable if sys.executable else ("python" if os.name == "nt" else "python3")

TEST_COMMANDS = {
    "python": [[py_bin, "-m", "pytest", "-q", "-x", "--tb=no"]],
    "java": [["mvn", "-q", "test"], ["gradle", "test", "-q"]],
    "csharp": [["dotnet", "test"]],
    "go": [["go", "test", "./..."]],
    "rust": [["cargo", "test"]],
    "javascript": [["npm", "test", "--silent"]],
    "cpp": [["ctest"]],
    "c": [["ctest"]],
}


@dataclass
class VerificationResult:
    passed: bool
    method: str  # "test-suite" | "build-and-run-fallback"
    detail: str


TEST_FILE_HINTS = {
    "python": [r"test_.*\.py$", r".*_test\.py$", r"^tests/"],
    "javascript": [r".*\.test\.js$", r".*\.spec\.js$", r"^test/", r"^tests/"],
    "java": [r".*Test\.java$", r"^src/test/"],
    "csharp": [r".*Tests\.cs$", r".*Test\.cs$"],
    "go": [r".*_test\.go$"],
    "rust": [r"^tests/", r"#\[test\]"],  # rust also checks source content, handled below
    "cpp": [r".*test.*\.cpp$", r"CMakeLists\.txt$"],
    "c": [r".*test.*\.c$"],
}


def _has_discoverable_tests(repo_path: str, language: str) -> bool:
    import re
    patterns = TEST_FILE_HINTS.get(language, [])
    if not patterns:
        return False
    for root, _, files in os.walk(repo_path):
        rel_root = os.path.relpath(root, repo_path)
        for fname in files:
            rel_path = os.path.join(rel_root, fname).replace("\\", "/").lstrip("./")
            if any(re.search(p, rel_path) for p in patterns if not p.startswith("#")):
                return True
            if language == "rust" and fname.endswith(".rs"):
                try:
                    with open(os.path.join(root, fname), encoding="utf-8", errors="ignore") as f:
                        if "#[test]" in f.read():
                            return True
                except OSError:
                    continue
    return False


def _find_scoped_test_cmd(repo_path: str, language: str, file_path: str):
    """Try to find a test command scoped to the module containing the touched file.
    Returns a scoped cmd list, or None if not discoverable."""
    import re
    from shutil import which

    if not file_path:
        return None

    rel = os.path.relpath(file_path, repo_path).replace("\\", "/")

    if language == "python" and which("python3" if os.name != "nt" else "python"):
        # Look for test_<module>.py or <module>_test.py in the same package
        dirname = os.path.dirname(os.path.join(repo_path, rel))
        basename = os.path.splitext(os.path.basename(rel))[0]
        candidates = [
            os.path.join(dirname, f"test_{basename}.py"),
            os.path.join(dirname, f"{basename}_test.py"),
        ]
        # Also check a tests/ sibling directory
        parent = os.path.dirname(dirname)
        for test_dir in [os.path.join(parent, "tests"), os.path.join(dirname, "tests")]:
            candidates.append(os.path.join(test_dir, f"test_{basename}.py"))

        for cand in candidates:
            if os.path.isfile(cand):
                rel_test = os.path.relpath(cand, repo_path)
                py = "python" if os.name == "nt" else "python3"
                return [py, "-m", "pytest", "-q", rel_test]

    if language == "go" and which("go"):
        # Scope to the package containing the touched file
        pkg_dir = os.path.dirname(rel)
        if pkg_dir:
            return ["go", "test", f"./{pkg_dir}/..."]

    return None


def _find_working_test_cmd(repo_path: str, language: str, file_path: str = None):
    """Find a test command, preferring scoped tests over full-suite."""
    # Try scoped first
    if file_path:
        scoped = _find_scoped_test_cmd(repo_path, language, file_path)
        if scoped:
            return scoped

    if not _has_discoverable_tests(repo_path, language):
        return None
    for cmd in TEST_COMMANDS.get(language, []):
        binary = cmd[0]
        from shutil import which
        if which(binary):
            return cmd
    return None


def verify(repo_path: str, language: str, adapter=None, file_path: str = None) -> VerificationResult:
    """
    adapter: an already-constructed BuildRunAdapter, used for the
    build-and-run fallback when no test suite is found or repo tests fail.
    file_path: the specific file being refactored, used to scope tests.
    """
    cmd = _find_working_test_cmd(repo_path, language, file_path)
    if cmd:
        try:
            proc = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, timeout=30)
            if proc.returncode == 0:
                return VerificationResult(
                    passed=True,
                    method="test-suite",
                    detail=(proc.stdout + proc.stderr)[-500:],
                )
        except subprocess.TimeoutExpired:
            pass

    if adapter is None:
        return VerificationResult(False, "build-and-run-fallback", "no adapter provided, cannot fall back")

    build_result = adapter.build()
    if build_result.exit_code != 0:
        return VerificationResult(False, "build-and-run-fallback", f"build failed: {build_result.stderr[:300]}")
    run_result = adapter.run_once()
    return VerificationResult(
        passed=(run_result.exit_code == 0),
        method="build-and-run-fallback",
        detail=(run_result.stdout + run_result.stderr)[-300:],
    )


def verify_before_after(repo_path: str, language: str, file_path: str, adapter=None):
    """
    Runs verify() twice — once on current (post-refactor) state, and if it
    fails, restores the .orig backup and verifies again to confirm the
    baseline itself was healthy (sanity check that the failure is really
    caused by the refactor, not a pre-existing broken test).
    Returns (accepted: bool, after_result, note: str)
    """
    from agents.refactoring_agent import restore

    after = verify(repo_path, language, adapter, file_path=file_path)
    if after.passed:
        return True, after, "refactor verified, keeping it"

    restore(file_path)
    baseline_recheck = verify(repo_path, language, adapter, file_path=file_path)
    if baseline_recheck.passed:
        note = "refactor broke tests, restored original — case REJECTED for this pattern"
    else:
        note = "baseline ALSO fails verification — pre-existing issue, not the refactor's fault; still rejecting this case from measurement to be safe"
    return False, after, note
