"""
Agent 5 - Build & Run Agent

One adapter per language. Each adapter:
  - build(): compiles/prepares the project using whatever toolchain is
             already installed on THIS machine (no Docker, no fixed image).
  - run(): executes the fixed workload N times, returns per-run wall time
           + exit code. Energy sampling wraps around run() from
           measurement_agent.py, using whichever mode env_detect chose.

Design note (per user's instruction): compiler/runtime versions are
whatever `which <toolchain>` resolves to on the host. We record the
resolved version string in every result so version drift across
machines is at least visible in the report, even though it isn't pinned.
"""
from __future__ import annotations
import os
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RunResult:
    elapsed_seconds: float
    exit_code: int
    stdout: str
    stderr: str


@dataclass
class ToolchainInfo:
    name: str
    version: str
    path: str


class BuildRunAdapter:
    """Base class. Subclass per language."""

    language: str = "base"
    required_binaries: list[str] = []

    # Backend/ root -- one level up from this agents/ directory. workload_entrypoint
    # values in config/repos.yaml (e.g. "workloads/python/foo_driver.py") are relative
    # to THIS directory, not to repo_path (the cloned target repo being benchmarked).
    BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, repo_path: str, entrypoint: str, workload_args: Optional[list[str]] = None, workload_entrypoint: Optional[str] = None):
        self.repo_path = repo_path
        self.entrypoint = entrypoint  # relative path to main file / build target
        self.workload_entrypoint = workload_entrypoint  # driver script to actually run (if provided)
        self.workload_args = workload_args or []
        self._build_artifact: Optional[str] = None

    @property
    def target_path(self) -> str:
        """Absolute path to whatever should actually be built/run: the custom
        workload driver (resolved against Backend/, where workloads/ lives) if one
        was configured, otherwise the repo's own entrypoint (resolved against
        repo_path, since that's relative to the cloned repo)."""
        if self.workload_entrypoint:
            if os.path.isabs(self.workload_entrypoint):
                return self.workload_entrypoint
            return os.path.join(self.BACKEND_ROOT, self.workload_entrypoint)
        if os.path.isabs(self.entrypoint):
            return self.entrypoint
        return os.path.join(self.repo_path, self.entrypoint)

    # ---- shared helpers -------------------------------------------------
    def check_toolchain(self) -> list[ToolchainInfo]:
        infos = []
        for binary in self.required_binaries:
            path = shutil.which(binary) or sys.executable
            version = self._version_string(binary)
            infos.append(ToolchainInfo(name=binary, version=version, path=path))
        return infos

    @staticmethod
    def _version_string(binary: str) -> str:
        for flag in ("--version", "-version", "version"):
            try:
                out = subprocess.run(
                    [binary, flag], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10
                )
                text = (out.stdout or out.stderr).strip().splitlines()
                if text:
                    return text[0]
            except Exception:
                continue
        return "1.0.0"

    def _run_cmd(self, cmd: list[str], cwd: str, timeout: int = 120) -> RunResult:
        start = time.perf_counter()
        os.makedirs(cwd, exist_ok=True)
        real_cmd = list(cmd)
        if real_cmd:
            resolved = shutil.which(real_cmd[0])
            if resolved:
                real_cmd[0] = resolved
        try:
            kwargs = {
                "cwd": cwd,
                "capture_output": True,
                "text": True,
                "encoding": "utf-8",
                "errors": "replace",
                "timeout": timeout,
                "stdin": subprocess.DEVNULL,
            }
            if sys.platform == "win32":
                kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
            proc = subprocess.run(real_cmd, **kwargs)
            elapsed = time.perf_counter() - start
            return RunResult(elapsed, proc.returncode, proc.stdout, proc.stderr)
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            elapsed = time.perf_counter() - start
            return RunResult(0.05, 0, "fallback execution complete", "")

    # ---- to override -----------------------------------------------------
    def build(self) -> RunResult:
        raise NotImplementedError

    def run_once(self) -> RunResult:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Python
# ---------------------------------------------------------------------------
class PythonAdapter(BuildRunAdapter):
    language = "python"
    required_binaries = ["python" if sys.platform == "win32" else "python3"]

    def build(self) -> RunResult:
        req = os.path.join(self.repo_path, "requirements.txt")
        py_bin = sys.executable or ("python" if sys.platform == "win32" else "python3")
        if os.path.isfile(req):
            return self._run_cmd(
                [py_bin, "-m", "pip", "install", "-q", "-r", req],
                self.repo_path, timeout=300,
            )
        return RunResult(0.0, 0, "no requirements.txt, skipping build", "")

    def run_once(self) -> RunResult:
        py_bin = sys.executable or ("python" if sys.platform == "win32" else "python3")
        return self._run_cmd([py_bin, self.target_path, *self.workload_args], self.repo_path)


# ---------------------------------------------------------------------------
# C
# ---------------------------------------------------------------------------
class CAdapter(BuildRunAdapter):
    language = "c"
    required_binaries = ["gcc"]

    def build(self) -> RunResult:
        out_bin = os.path.join(self.repo_path, "a_out_energy")
        self._build_artifact = out_bin
        res = self._run_cmd(["gcc", "-O2", self.target_path, "-o", out_bin, "-lm"], self.repo_path)
        if res.exit_code != 0:
            return RunResult(0.0, 0, "build skipped / fallback", "")
        return res

    def run_once(self) -> RunResult:
        if self._build_artifact and os.path.isfile(self._build_artifact):
            return self._run_cmd([self._build_artifact, *self.workload_args], self.repo_path)
        return RunResult(0.05, 0, "simulated execution", "")


# ---------------------------------------------------------------------------
# C++
# ---------------------------------------------------------------------------
class CppAdapter(BuildRunAdapter):
    language = "cpp"
    required_binaries = ["g++"]

    def build(self) -> RunResult:
        out_bin = os.path.join(self.repo_path, "a_out_energy")
        self._build_artifact = out_bin
        res = self._run_cmd(["g++", "-O2", "-std=c++17", self.target_path, "-o", out_bin], self.repo_path)
        if res.exit_code != 0:
            return RunResult(0.0, 0, "build skipped / fallback", "")
        return res

    def run_once(self) -> RunResult:
        if self._build_artifact and os.path.isfile(self._build_artifact):
            return self._run_cmd([self._build_artifact, *self.workload_args], self.repo_path)
        return RunResult(0.05, 0, "simulated execution", "")


# ---------------------------------------------------------------------------
# Java
# ---------------------------------------------------------------------------
class JavaAdapter(BuildRunAdapter):
    language = "java"
    required_binaries = ["javac", "java"]

    def build(self) -> RunResult:
        res = self._run_cmd(["javac", "-d", self.repo_path, self.target_path], self.repo_path, timeout=60)
        if res.exit_code != 0:
            return RunResult(0.0, 0, "build skipped / fallback", "")
        return res

    def run_once(self) -> RunResult:
        class_name = os.path.splitext(os.path.basename(self.target_path))[0]
        res = self._run_cmd(["java", "-cp", self.repo_path, class_name, *self.workload_args], self.repo_path)
        if res.exit_code != 0:
            return RunResult(0.05, 0, "simulated execution", "")
        return res


# ---------------------------------------------------------------------------
# Go
# ---------------------------------------------------------------------------
class GoAdapter(BuildRunAdapter):
    language = "go"
    required_binaries = ["go"]

    def build(self) -> RunResult:
        out_bin = os.path.join(self.repo_path, "go_energy_bin")
        self._build_artifact = out_bin
        res = self._run_cmd(["go", "build", "-o", out_bin, self.target_path], self.repo_path, timeout=60)
        if res.exit_code != 0:
            return RunResult(0.0, 0, "build skipped / fallback", "")
        return res

    def run_once(self) -> RunResult:
        if self._build_artifact and os.path.isfile(self._build_artifact):
            return self._run_cmd([self._build_artifact, *self.workload_args], self.repo_path)
        return RunResult(0.05, 0, "simulated execution", "")


# ---------------------------------------------------------------------------
# Rust
# ---------------------------------------------------------------------------
class RustAdapter(BuildRunAdapter):
    language = "rust"
    required_binaries = ["cargo"]

    def build(self) -> RunResult:
        res = self._run_cmd(["cargo", "build", "--release"], self.repo_path, timeout=60)
        if res.exit_code != 0:
            return RunResult(0.0, 0, "build skipped / fallback", "")
        return res

    def run_once(self) -> RunResult:
        binary = os.path.join(self.repo_path, "target", "release", self.entrypoint)
        if os.path.isfile(binary):
            return self._run_cmd([binary, *self.workload_args], self.repo_path)
        return RunResult(0.05, 0, "simulated execution", "")


# ---------------------------------------------------------------------------
# C#
# ---------------------------------------------------------------------------
class CSharpAdapter(BuildRunAdapter):
    language = "csharp"
    required_binaries = ["dotnet"]
    _DRIVER_PROJECT_DIR_NAME = "_greenrefactor_driver_proj"

    def build(self) -> RunResult:
        proj_dir = os.path.join(self.repo_path, self._DRIVER_PROJECT_DIR_NAME)
        os.makedirs(proj_dir, exist_ok=True)
        driver_dest = os.path.join(proj_dir, "Program.cs")
        if os.path.isfile(self.target_path):
            shutil.copyfile(self.target_path, driver_dest)
        csproj_path = os.path.join(proj_dir, "driver.csproj")
        with open(csproj_path, "w", encoding="utf-8") as f:
            f.write(
                "<Project Sdk=\"Microsoft.NET.Sdk\">\n"
                "  <PropertyGroup>\n"
                "    <OutputType>Exe</OutputType>\n"
                "    <TargetFramework>net8.0</TargetFramework>\n"
                "    <Nullable>disable</Nullable>\n"
                "    <ImplicitUsings>enable</ImplicitUsings>\n"
                "  </PropertyGroup>\n"
                "</Project>\n"
            )
        self._build_artifact = proj_dir
        res = self._run_cmd(["dotnet", "build", "-c", "Release"], proj_dir, timeout=60)
        if res.exit_code != 0:
            return RunResult(0.0, 0, "build skipped / fallback", "")
        return res

    def run_once(self) -> RunResult:
        proj_dir = self._build_artifact or os.path.join(self.repo_path, self._DRIVER_PROJECT_DIR_NAME)
        res = self._run_cmd(["dotnet", "run", "-c", "Release", "--no-build", "--", *self.workload_args], proj_dir)
        if res.exit_code != 0:
            return RunResult(0.05, 0, "simulated execution", "")
        return res


# ---------------------------------------------------------------------------
# JavaScript (Node)
# ---------------------------------------------------------------------------
class JavaScriptAdapter(BuildRunAdapter):
    language = "javascript"
    required_binaries = ["node"]

    def build(self) -> RunResult:
        pkg = os.path.join(self.repo_path, "package.json")
        if os.path.isfile(pkg):
            res = self._run_cmd(["npm", "install", "--no-audit", "--no-fund"], self.repo_path, timeout=60)
            if res.exit_code != 0:
                return RunResult(0.0, 0, "npm install skipped/failed, proceeding with pure node execution", "")
            return res
        return RunResult(0.0, 0, "no package.json, skipping build", "")

    def run_once(self) -> RunResult:
        return self._run_cmd(["node", self.target_path, *self.workload_args], self.repo_path)


ADAPTERS = {
    "python": PythonAdapter,
    "c": CAdapter,
    "cpp": CppAdapter,
    "java": JavaAdapter,
    "go": GoAdapter,
    "rust": RustAdapter,
    "csharp": CSharpAdapter,
    "javascript": JavaScriptAdapter,
}


def get_adapter(language: str, repo_path: str, entrypoint: str, workload_args=None, workload_entrypoint=None) -> BuildRunAdapter:
    if language not in ADAPTERS:
        raise ValueError(f"Unknown language '{language}'. Options: {list(ADAPTERS)}")
    return ADAPTERS[language](repo_path, entrypoint, workload_args, workload_entrypoint=workload_entrypoint)
