import os
import subprocess
import yaml

def check_dirty_repos():
    config_path = os.path.join(os.path.dirname(__file__), "config", "repos.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    dirty_repos = []
    checked = 0

    for lang, lang_data in config.items():
        if not isinstance(lang_data, dict): continue
        for repo in lang_data.get("repos", []):
            repo_path = os.path.join(os.path.dirname(__file__), repo["local_path"])
            if os.path.isdir(os.path.join(repo_path, ".git")):
                checked += 1
                try:
                    out = subprocess.check_output(
                        ["git", "status", "--porcelain"], 
                        cwd=repo_path, 
                        stderr=subprocess.STDOUT
                    ).decode("utf-8").strip()
                    if out:
                        dirty_repos.append((f"{lang}/{repo['name']}", out))
                except Exception as e:
                    dirty_repos.append((f"{lang}/{repo['name']}", f"Error running git status: {e}"))

    print(f"Checked {checked} cloned repos for dirty states.")
    if dirty_repos:
        print("\nWARNING: The following repos are dirty/modified:")
        for name, diff in dirty_repos:
            print(f" - {name}")
            for line in diff.split('\n'):
                print(f"    {line}")
    else:
        print("\nAll cloned repos are perfectly clean.")

if __name__ == "__main__":
    check_dirty_repos()
