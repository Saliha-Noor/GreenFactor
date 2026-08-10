import os
import yaml
import json

backend_dir = os.path.dirname(os.path.abspath(__file__))
repos_yaml = os.path.join(backend_dir, "config", "repos.yaml")
out_js = os.path.join(backend_dir, "..", "Frontend", "src", "data", "reposData.js")

with open(repos_yaml, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

repos_list = []
for lang, data in cfg.items():
    for repo in data.get("repos", []):
        excluded = bool(repo.get("excluded"))
        repos_list.append({
            "name": repo["name"],
            "language": lang,
            "entrypoint": repo["entrypoint"],
            "url": repo["url"],
            "status": "Excluded" if excluded else "Configured & Ingested",
            "excluded": excluded,
            "exclusion_reason": repo.get("exclusion_reason") if excluded else None,
            "patterns_checked": 0 if excluded else len(data.get("patterns", []))
        })

js_content = f"// Automatically generated from Backend/config/repos.yaml ({len(repos_list)} repositories)\n"
js_content += f"export const realBenchmarkRepos = {json.dumps(repos_list, indent=2)};\n"

os.makedirs(os.path.dirname(out_js), exist_ok=True)
with open(out_js, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Generated reposData.js with {len(repos_list)} repositories!")
