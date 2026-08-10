"""
Orchestrator - runs ONE full case end-to-end:
  1. measure baseline (N runs, unmodified code)
  2. detect pattern instances in the target file
  3. apply refactor (auto for cache_reuse py/js, flagged-only comment otherwise)
  4. verify (test suite, or build-and-run fallback) — restore + reject if broken
  5. measure refactored (N runs) — only if verification passed
  6. run paired stats on baseline vs refactored energy
Saves one JSON per case to results/<language>/<repo>__<pattern>.json
"""
import json
import os
from dataclasses import asdict

from agents import env_detect
from agents.build_run_agent import get_adapter
from agents.measurement_agent import measure_n_runs
from agents.pattern_detection_agent import scan_file, PatternHit
from agents.refactoring_agent import apply_pattern, restore
from agents.verification_agent import verify_before_after
from agents.stats_agent import compare_before_after

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

def _save_out(out, language, repo_name):
    out_dir = os.path.join(RESULTS_DIR, language)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, f"{repo_name}.json"), "w") as f:
        json.dump(out, f, indent=2)


def run_case(
    language: str,
    repo_path: str,
    entrypoint: str,
    repo_name: str,
    runs_per_case: int = 30,
    workload_entrypoint: str = None,
    workload_args: list = None,
    interleave: bool = False,
    max_hits: int = None,
    url: str = None,
) -> dict:
    file_path = os.path.join(repo_path, entrypoint)
    mode_info = "unknown"
    mode_file = os.path.join(os.path.dirname(__file__), "config", "measurement_mode.json")
    if os.path.isfile(mode_file):
        with open(mode_file) as f:
            mode_info = json.load(f).get("measurement_mode", "unknown")

    out = {
        "language": language, "repo": repo_name, "file": entrypoint,
        "measurement_mode": mode_info,
        "status": None, "detail": None,
    }

    if not os.path.isfile(file_path):
        if url:
            from agents.ingestion_agent import clone_repo
            clone_repo(url, repo_path)
        if not os.path.isfile(file_path):
            # Distinct status from "no_pattern_found" on purpose: this is a missing/bad
            # entrypoint (config error, failed clone, wrong path), not "we scanned the file
            # and found nothing to refactor." Conflating the two hid this case's results
            # entirely in prior versions of this function.
            out["status"] = "entrypoint_not_found"
            out["detail"] = f"Entrypoint file {entrypoint} not found in {repo_path}"
            _save_out(out, language, repo_name)
            return out

    adapter = get_adapter(language, repo_path, entrypoint, workload_args=workload_args, workload_entrypoint=workload_entrypoint)
    try:
        adapter.check_toolchain()
    except EnvironmentError as e:
        out["status"] = "skipped"
        out["detail"] = str(e)
        _save_out(out, language, repo_name)
        return out

    build_result = adapter.build()
    if build_result.exit_code != 0:
        out["status"] = "build_failed"
        out["detail"] = build_result.stderr[:300]
        _save_out(out, language, repo_name)
        return out

    # Note on Measurement Methodology & Thermal/Drift Limitations:
    # By default (interleave=False), baseline runs are performed in batch upfront before any code
    # transformations are applied, followed by refactored runs. This eliminates build/restore overhead
    # between individual runs but introduces a potential confound from thermal throttling or CPU frequency
    # drift over long benchmark suites. When interleave=True is enabled, baseline and refactored runs alternate.

    # 1. baseline measurement (before touching the file at all)
    baseline_measurements = measure_n_runs(adapter, n=runs_per_case)
    baseline_energies = [m.energy_joules for m in baseline_measurements if m.energy_joules is not None]

    # 2. detect patterns (mechanical heuristic scanner)
    raw_hits = scan_file(file_path, language)
    hits = []
    for h in raw_hits:
        if h.pattern == "system_flag:oversized_file":
            out["oversized_file_skipped"] = True
            out["file_lines"] = h.line_number
        else:
            hits.append(h)

    # 2b. semantic / LLM review agent integration
    try:
        from agents.llm_review_agent import review_file
        llm_suggestions = review_file(file_path, language)
        for s in llm_suggestions:
            if isinstance(s, dict) and "pattern" in s:
                hit_obj = PatternHit(
                    pattern=s["pattern"],
                    file_path=file_path,
                    line_number=s.get("line", 1),
                    snippet=s.get("reasoning", "LLM-suggested pattern"),
                    confidence=s.get("confidence", "medium"),
                )
                setattr(hit_obj, "is_llm", True)
                hits.append(hit_obj)
    except EnvironmentError as e:
        # GROQ_API_KEY environment variable missing — log skip note and continue gracefully
        pass
    except Exception as e:
        pass

    if not hits:
        out["status"] = "no_pattern_found"
        out["baseline_mean_j"] = sum(baseline_energies) / len(baseline_energies) if baseline_energies else None
        print(f"     [baseline_measured] mean energy: {out['baseline_mean_j']} Joules")
        _save_out(out, language, repo_name)
        return out

    if max_hits and len(hits) > max_hits:
        hits = hits[:max_hits]

    case_results = []
    total_hits = len(hits)
    print(f"     found {total_hits} pattern hits in {entrypoint}")
    for idx, hit in enumerate(hits, 1):
        print(f"     [{idx}/{total_hits}] Testing {hit.pattern} @ line {hit.line_number}... ", end="", flush=True)
        # 3. apply refactor
        refactor_result = apply_pattern(file_path, language, hit)
        try:
            rebuild = adapter.build()
            if rebuild.exit_code != 0:
                print("REBUILD FAILED")
                case_results.append({
                    "pattern": hit.pattern, "line": hit.line_number, "status": "rebuild_failed_after_refactor",
                })
                continue

            # 4. verify
            accepted, verification, note = verify_before_after(repo_path, language, file_path, adapter)
            if not accepted:
                print("REJECTED")
                case_results.append({
                    "pattern": hit.pattern, "line": hit.line_number, "status": "rejected_by_verification",
                    "note": note,
                })
                continue

            print("ACCEPTED & MEASURING... ", end="", flush=True)

            # 5. measure refactored
            if interleave:
                # Opt-in interleaved sampling to mitigate thermal drift: alternate 1 baseline and 1 refactored run
                refactored_measurements = []
                interleaved_baseline = []
                for _ in range(runs_per_case):
                    refactored_measurements.extend(measure_n_runs(adapter, n=1))
                    restore(file_path)
                    adapter.build()
                    interleaved_baseline.extend(measure_n_runs(adapter, n=1))
                    apply_pattern(file_path, language, hit)
                    adapter.build()
                baseline_energies = [m.energy_joules for m in interleaved_baseline if m.energy_joules is not None]
            else:
                refactored_measurements = measure_n_runs(adapter, n=runs_per_case)

            refactored_energies = [m.energy_joules for m in refactored_measurements if m.energy_joules is not None]

            is_llm = getattr(hit, "is_llm", False)
            method_label = "llm-suggested" if is_llm else refactor_result.method

            entry = {
                "pattern": hit.pattern, "line": hit.line_number,
                "refactor_method": method_label,
                "status": "measured",
            }

            # 6. stats — only meaningful for auto-applied refactors with a real energy change to test
            n = min(len(baseline_energies), len(refactored_energies))
            if (refactor_result.method == "auto" or is_llm) and n >= 3:
                try:
                    comparison = compare_before_after(baseline_energies[:n], refactored_energies[:n])
                    entry["stats"] = asdict(comparison)
                except Exception as e:
                    entry["stats_error"] = str(e)
            else:
                entry["note"] = "flagged-only refactor (no auto-applied code change) — nothing to statistically compare yet"

            case_results.append(entry)
            print("DONE", flush=True)
        finally:
            # restore original so the next hit in this same file starts clean
            restore(file_path)
            adapter.build()

    out["status"] = "done"
    out["baseline_mean_j"] = sum(baseline_energies) / len(baseline_energies) if baseline_energies else None
    out["patterns"] = case_results

    _save_out(out, language, repo_name)
    return out


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", required=True)
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--entrypoint", required=True)
    parser.add_argument("--repo-name", required=True)
    parser.add_argument("--runs", type=int, default=30)
    args = parser.parse_args()

    if not os.path.isfile(os.path.join(os.path.dirname(__file__), "config", "measurement_mode.json")):
        env_detect.run_detection()

    result = run_case(args.language, args.repo_path, args.entrypoint, args.repo_name, args.runs)
    print(json.dumps(result, indent=2, default=str))
