"""
Run ONE language's full batch (up to 15 repos), independently of the other
7 languages. For each repo: baseline measure -> detect patterns -> refactor
-> verify -> measure refactored -> stats (all via orchestrator.run_case).

Results land in results/<language>/<repo_name>.json — compare_results.py
picks up whatever's there whenever you're ready to compare across languages.

Usage:
    python3 run_language_batch.py --language python --config config/repos.yaml
"""
import argparse
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from agents import env_detect
from orchestrator import run_case

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def run_batch(language: str, config_path: str, runs_per_case: int = 30, max_hits: int = None, target_repo: str = None):
    mode_file = os.path.join(os.path.dirname(__file__), "config", "measurement_mode.json")
    if not os.path.isfile(mode_file):
        info = env_detect.run_detection()
        print(f"[env] measurement_mode = {info['measurement_mode']} (rapl_vendor={info['rapl_vendor']})")
    else:
        with open(mode_file) as f:
            print(f"[env] measurement_mode = {json.load(f)['measurement_mode']} (from earlier detection)")

    config = load_config(config_path)
    lang_cfg = config.get(language)
    if not lang_cfg:
        raise ValueError(f"No config entry for language '{language}' in {config_path}")

    all_repos = lang_cfg.get("repos", [])

    # Enforce config/repos.yaml's excluded: true / exclusion_reason fields. These repos are
    # formally excluded from the measured dataset (see README's "Methodological Exclusions"
    # table) and must never be queued, built, run, or measured, regardless of --repo.
    excluded_repos = [r for r in all_repos if r.get("excluded")]
    for r in excluded_repos:
        reason = r.get("exclusion_reason", "no reason recorded")
        print(f"[skip] {r['name']} — excluded: {reason}")

    repos = [r for r in all_repos if not r.get("excluded")]

    if target_repo:
        excluded_match = next((r for r in excluded_repos if r["name"] == target_repo), None)
        if excluded_match:
            raise ValueError(
                f"Repo '{target_repo}' is formally excluded ({excluded_match.get('exclusion_reason', 'no reason recorded')}) "
                f"and cannot be run. Remove 'excluded: true' from config/repos.yaml if this was a mistake."
            )
        repos = [r for r in repos if r["name"] == target_repo]
        if not repos:
            raise ValueError(f"Repo '{target_repo}' not found in {language} config")

    print(f"[{language}] {len(repos)} repos queued ({len(excluded_repos)} excluded) — 8 patterns checked per repo automatically")

    summary = {}
    for repo in repos:
        repo_name = repo["name"]
        
        # SKIP ALREADY-MEASURED REPOS
        result_path = os.path.join(RESULTS_DIR, language, f"{repo_name}.json")
        if os.path.exists(result_path):
            try:
                with open(result_path) as rf:
                    past_data = json.load(rf)
                if any(p.get("status") == "measured" and "stats" in p for p in past_data.get("patterns", [])):
                    print(f"     status: already_measured (skipping)")
                    summary["already_measured"] = summary.get("already_measured", 0) + 1
                    continue
            except Exception:
                pass
                
        repo_path = os.path.join(os.path.dirname(__file__), repo["local_path"])
        
        # SECOND INDEPENDENT SAFETY NET: Unconditional clean state
        # The overarching project itself has no git history locally, but the individual 
        # ingested repos cloned into Backend/repos DO have .git folders. We force clean them.
        import subprocess
        if os.path.isdir(os.path.join(repo_path, ".git")):
            try:
                subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=repo_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["git", "clean", "-fd"], cwd=repo_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"     [warning] git reset failed for {repo_name}: {e}")

        entrypoint = repo["entrypoint"]
        workload_entrypoint = repo.get("workload_entrypoint")
        workload_args = repo.get("workload_args")
        url = repo.get("url")
        try:
            result = run_case(language, repo_path, entrypoint, repo_name, runs_per_case, workload_entrypoint=workload_entrypoint, workload_args=workload_args, max_hits=max_hits, url=url)
            status = result.get("status", "unknown")
        except Exception as e:
            print(f"     CRASH: {str(e)}")
            status = "crash"
            
        summary[status] = summary.get(status, 0) + 1
        print(f"     status: {status}")

    print(f"[{language}] batch done: {summary}")
    print(f"[{language}] results in results/{language}/")


ALL_LANGUAGES = ["python", "c", "cpp", "java", "go", "rust", "csharp", "javascript"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", required=True, choices=ALL_LANGUAGES + ["all"],
                         help="One language, or 'all' to run the full 120-repo suite across all 8 languages in one command")
    parser.add_argument("--config", default="config/repos.yaml")
    parser.add_argument("--runs-per-case", type=int, default=30)
    parser.add_argument("--max-hits", type=int, default=None, help="Max pattern candidate hits to evaluate per repo")
    parser.add_argument("--repo", default=None, help="Filter to a specific repo name (not valid with --language all)")
    args = parser.parse_args()

    if args.language == "all":
        if args.repo:
            raise SystemExit("--repo cannot be combined with --language all")
        grand_summary = {}
        for lang in ALL_LANGUAGES:
            run_batch(lang, args.config, args.runs_per_case, max_hits=args.max_hits, target_repo=None)
            print()
        print("[all] full 120-repo suite complete — see results/<language>/ for each repo's result file")
    else:
        run_batch(args.language, args.config, args.runs_per_case, max_hits=args.max_hits, target_repo=args.repo)
