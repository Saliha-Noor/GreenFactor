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


def run_batch(language: str, config_path: str, runs_per_case: int = 30):
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

    repos = lang_cfg.get("repos", [])
    print(f"[{language}] {len(repos)} repos queued (8 patterns checked per repo automatically)")

    summary = {}
    for repo in repos:
        repo_name = repo["name"]
        repo_path = os.path.join(os.path.dirname(__file__), repo["local_path"])
        entrypoint = repo["entrypoint"]
        workload_entrypoint = repo.get("workload_entrypoint")
        print(f"  -> {repo_name}")
        result = run_case(language, repo_path, entrypoint, repo_name, runs_per_case, workload_entrypoint=workload_entrypoint)
        status = result["status"]
        summary[status] = summary.get(status, 0) + 1
        print(f"     status: {status}")

    print(f"[{language}] batch done: {summary}")
    print(f"[{language}] results in results/{language}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", required=True, choices=[
        "python", "c", "cpp", "java", "go", "rust", "csharp", "javascript"
    ])
    parser.add_argument("--config", default="config/repos.yaml")
    parser.add_argument("--runs-per-case", type=int, default=30)
    args = parser.parse_args()
    run_batch(args.language, args.config, args.runs_per_case)
