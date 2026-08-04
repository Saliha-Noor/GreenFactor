"""
Agent 1 - Repository Ingestion Agent

Automates cloning, validation, and registration of benchmark repositories
for the GreenRefactor pipeline. Each repository is:
  1. Cloned (shallow, depth=1) into repos/<language>/<repo_name>/
  2. Validated: entrypoint file must exist
  3. Registered into config/repos.yaml

Usage:
    # Add a single repo:
    python agents/ingestion_agent.py --language python \
        --url https://github.com/user/repo.git \
        --entrypoint main.py \
        --name my_repo

    # Add from a JSON manifest (bulk):
    python agents/ingestion_agent.py --from-manifest repos_manifest.json
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOS_DIR = os.path.join(BASE_DIR, "repos")
CONFIG_PATH = os.path.join(BASE_DIR, "config", "repos.yaml")

SUPPORTED_LANGUAGES = [
    "python", "javascript", "java", "csharp", "c", "cpp", "go", "rust",
]

DEFAULT_PATTERNS = [
    "early_termination", "avoid_redundant_computation", "batch_operations",
    "cache_reuse", "offload_to_native", "high_perf_libraries",
    "high_perf_data_structures", "swap_library_impl",
]


def _load_config() -> dict:
    """Load the existing repos.yaml, or return a skeleton if missing."""
    if os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        if cfg is None:
            cfg = {}
        return cfg
    return {}


def _save_config(cfg: dict) -> None:
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)


def _ensure_language_section(cfg: dict, language: str) -> None:
    """Ensure the language key exists with patterns and repos list."""
    if language not in cfg or not isinstance(cfg[language], dict):
        cfg[language] = {"patterns": list(DEFAULT_PATTERNS), "repos": []}
    if "repos" not in cfg[language]:
        cfg[language]["repos"] = []
    if "patterns" not in cfg[language]:
        cfg[language]["patterns"] = list(DEFAULT_PATTERNS)


def clone_repo(url: str, dest_path: str, shallow: bool = True) -> bool:
    """Clone a git repository. Returns True on success."""
    git_dir = os.path.join(dest_path, ".git")
    if os.path.isdir(dest_path):
        if os.path.isdir(git_dir):
            print(f"  [skip] {dest_path} already exists, skipping clone")
            return True
        else:
            print(f"  [cleanup] Removing incomplete folder {dest_path} before re-cloning...")
            shutil.rmtree(dest_path, ignore_errors=True)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    cmd = ["git", "clone", "--single-branch"]
    if shallow:
        cmd += ["--depth", "1"]
    cmd += [url, dest_path]

    print(f"  [clone] {url} -> {dest_path}")
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300
        )
        if result.returncode != 0:
            print(f"  [error] git clone failed: {result.stderr[:300]}")
            shutil.rmtree(dest_path, ignore_errors=True)
            return False
        return True
    except FileNotFoundError:
        print("  [error] git not found on PATH — install git first")
        return False
    except subprocess.TimeoutExpired:
        print("  [error] git clone timed out after 300s — cleaning up partial clone")
        shutil.rmtree(dest_path, ignore_errors=True)
        return False


def validate_entrypoint(repo_path: str, entrypoint: str) -> bool:
    """Check that the entrypoint file exists within the cloned repo."""
    full_path = os.path.join(repo_path, entrypoint)
    if os.path.isfile(full_path):
        return True
    print(f"  [warn] entrypoint not found: {full_path}")
    return False


def register_repo(
    language: str,
    name: str,
    url: str,
    entrypoint: str,
    workload_args: list[str] | None = None,
) -> dict:
    """
    Clone, validate, and register a single repository.
    Returns a status dict.
    """
    if language not in SUPPORTED_LANGUAGES:
        return {"name": name, "status": "error", "detail": f"unsupported language: {language}"}

    repo_path = os.path.join(REPOS_DIR, language, name)

    # 1. Clone
    if not clone_repo(url, repo_path):
        return {"name": name, "status": "clone_failed"}

    # 2. Validate entrypoint
    if not validate_entrypoint(repo_path, entrypoint):
        return {"name": name, "status": "entrypoint_missing",
                "detail": f"expected {entrypoint} in {repo_path}"}

    # 3. Register in config
    cfg = _load_config()
    _ensure_language_section(cfg, language)

    # avoid duplicates
    existing_names = {r["name"] for r in cfg[language]["repos"]}
    if name in existing_names:
        print(f"  [skip] {name} already registered in repos.yaml for {language}")
        return {"name": name, "status": "already_registered"}

    entry = {
        "name": name,
        "local_path": os.path.relpath(repo_path, BASE_DIR).replace("\\", "/"),
        "entrypoint": entrypoint,
        "url": url,
    }
    if workload_args:
        entry["workload_args"] = workload_args

    cfg[language]["repos"].append(entry)
    _save_config(cfg)
    print(f"  [registered] {name} for {language} in repos.yaml")

    return {"name": name, "status": "ok", "local_path": entry["local_path"]}


def ingest_from_manifest(manifest_path: str) -> list[dict]:
    """
    Bulk-ingest from a JSON manifest file. Expected format:
    [
      {
        "language": "python",
        "name": "some_repo",
        "url": "https://github.com/...",
        "entrypoint": "main.py",
        "workload_args": ["--input", "data.txt"]  // optional
      },
      ...
    ]
    """
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    results = []
    for entry in manifest:
        language = entry.get("language")
        name = entry.get("name")
        url = entry.get("url")
        entrypoint = entry.get("entrypoint")
        workload_args = entry.get("workload_args")

        if not all([language, name, url, entrypoint]):
            results.append({"name": name or "unknown", "status": "invalid_entry"})
            continue

        print(f"\n[{language}] ingesting {name}...")
        result = register_repo(language, name, url, entrypoint, workload_args)
        results.append(result)

    return results


def remove_repo(language: str, name: str, delete_files: bool = False) -> dict:
    """Remove a repo from config (and optionally delete cloned files)."""
    cfg = _load_config()
    if language not in cfg or "repos" not in cfg[language]:
        return {"name": name, "status": "not_found"}

    original_len = len(cfg[language]["repos"])
    cfg[language]["repos"] = [r for r in cfg[language]["repos"] if r["name"] != name]

    if len(cfg[language]["repos"]) == original_len:
        return {"name": name, "status": "not_found"}

    _save_config(cfg)

    if delete_files:
        repo_path = os.path.join(REPOS_DIR, language, name)
        if os.path.isdir(repo_path):
            shutil.rmtree(repo_path)
            print(f"  [deleted] {repo_path}")

    return {"name": name, "status": "removed"}


def list_repos(language: str | None = None) -> None:
    """Print registered repos for one or all languages."""
    cfg = _load_config()
    languages = [language] if language else SUPPORTED_LANGUAGES

    for lang in languages:
        if lang not in cfg or not cfg[lang].get("repos"):
            print(f"  {lang}: (no repos registered)")
            continue
        repos = cfg[lang]["repos"]
        print(f"  {lang}: {len(repos)} repos")
        for r in repos:
            print(f"    - {r['name']}: {r.get('local_path', '?')} -> {r.get('entrypoint', '?')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GreenRefactor Repository Ingestion Agent")
    sub = parser.add_subparsers(dest="command", help="sub-command")

    # --- add ---
    add_p = sub.add_parser("add", help="Clone and register a single repo")
    add_p.add_argument("--language", required=True, choices=SUPPORTED_LANGUAGES)
    add_p.add_argument("--url", required=True, help="Git clone URL")
    add_p.add_argument("--entrypoint", required=True, help="Relative path to main file")
    add_p.add_argument("--name", required=True, help="Short repo identifier")
    add_p.add_argument("--workload-args", nargs="*", default=None)

    # --- bulk ---
    bulk_p = sub.add_parser("bulk", help="Ingest repos from a JSON manifest")
    bulk_p.add_argument("--manifest", required=True, help="Path to JSON manifest file")

    # --- list ---
    list_p = sub.add_parser("list", help="List registered repos")
    list_p.add_argument("--language", choices=SUPPORTED_LANGUAGES, default=None)

    # --- remove ---
    rm_p = sub.add_parser("remove", help="Remove a registered repo")
    rm_p.add_argument("--language", required=True, choices=SUPPORTED_LANGUAGES)
    rm_p.add_argument("--name", required=True)
    rm_p.add_argument("--delete-files", action="store_true")

    args = parser.parse_args()

    if args.command == "add":
        result = register_repo(args.language, args.name, args.url, args.entrypoint, args.workload_args)
        print(json.dumps(result, indent=2))
    elif args.command == "bulk":
        results = ingest_from_manifest(args.manifest)
        print(json.dumps(results, indent=2))
    elif args.command == "list":
        list_repos(args.language)
    elif args.command == "remove":
        result = remove_repo(args.language, args.name, args.delete_files)
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()
