import yaml
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "repos.yaml")

import argparse

def clone_all(target_lang: str | None = None):
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Config file not found at {CONFIG_PATH}")
        sys.exit(1)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    all_languages = ["python", "javascript", "java", "csharp", "c", "cpp", "go", "rust"]
    if target_lang:
        if target_lang.lower() not in all_languages:
            print(f"Error: Unknown language '{target_lang}'. Options: {all_languages}")
            sys.exit(1)
        languages = [target_lang.lower()]
    else:
        languages = all_languages

    for lang in languages:
        all_repos = cfg.get(lang, {}).get("repos", [])
        excluded = [r for r in all_repos if r.get("excluded")]
        repos = [r for r in all_repos if not r.get("excluded")]
        print(f"\n==========================================")
        print(f"Starting ingestion for {len(repos)} [{lang.upper()}] repositories ({len(excluded)} formally excluded, skipped)")
        print(f"==========================================")
        for r in excluded:
            print(f"  [skip] {r['name']} — excluded: {r.get('exclusion_reason', 'no reason recorded')}")

        for repo in repos:
            name = repo.get("name")
            url = repo.get("url")
            entrypoint = repo.get("entrypoint")
            
            if name and url and entrypoint:
                print(f"\n---> Ingesting [{lang}] {name} from {url}...")
                cmd = [
                    sys.executable,
                    os.path.join(BASE_DIR, "agents", "ingestion_agent.py"),
                    "add",
                    "--language", lang,
                    "--url", url,
                    "--entrypoint", entrypoint,
                    "--name", name
                ]
                subprocess.run(cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clone benchmark repositories for GreenRefactor")
    parser.add_argument("--language", type=str, default=None, help="Target language (e.g. python, javascript, java)")
    args = parser.parse_args()
    clone_all(args.language)
