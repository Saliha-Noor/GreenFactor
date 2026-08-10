import os, json, yaml, subprocess, sys

def check_toolchains():
    print("\n" + "="*60)
    print("STEP 3: PIPELINE TOOLCHAIN & MODE CHECK")
    print("="*60)
    tools = [
        ("Rust", "rustc -V"), ("Go", "go version"), 
        ("C# (dotnet)", "dotnet --version"), ("Java (javac)", "javac -version"), 
        ("JavaScript (node)", "node -v"), ("C/C++ (gcc)", "gcc --version"), 
        ("Python", "python --version")
    ]
    for name, cmd in tools:
        try:
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip().split('\n')[0]
            print(f"✅ {name:18}: {out}")
        except Exception:
            print(f"❌ {name:18}: MISSING or NOT IN PATH")

    mode_file = "config/measurement_mode.json"
    if os.path.exists(mode_file):
        with open(mode_file) as f:
            print(f"\n[Environment Mode]: {json.load(f).get('measurement_mode')} (Note: RAPL is Linux-only. If on Windows, this is gracefully using a TDP estimate).")

def analyze_results():
    results_dir = "results"
    cfg_path = "config/repos.yaml"
    with open(cfg_path, encoding='utf-8') as f:
        config = yaml.safe_load(f)
        
    valid_repos = set()
    file_status = []
    total_json_files = 0
    
    for lang in os.listdir(results_dir):
        lang_dir = os.path.join(results_dir, lang)
        if not os.path.isdir(lang_dir): continue
        for f in os.listdir(lang_dir):
            if not f.endswith(".json") or f == "comparison_summary.json": continue
            total_json_files += 1
            path = os.path.join(lang_dir, f)
            with open(path, encoding='utf-8') as fp:
                data = json.load(fp)
            repo = f[:-5]
            
            reasons = []
            has_measured = False
            for p in data.get("patterns", []):
                st = p.get("status")
                if st == "measured" and "stats" in p:
                    has_measured = True
                    break
                reasons.append(f"{p.get('pattern')}:{st}")
            
            if not data.get("patterns"):
                reasons.append(f"batch_status:{data.get('status', 'unknown')}")
                if "detail" in data and data["detail"]:
                    reasons.append(f"detail:{data['detail'][:50]}...")
            
            if has_measured:
                valid_repos.add(f"{lang}/{repo}")
                file_status.append((lang, repo, "VALID", "-"))
            else:
                file_status.append((lang, repo, "INVALID", ", ".join(reasons) or "No patterns processed"))
                
    print("\n" + "="*60)
    print(f"STEP 1: THE {total_json_files} -> {len(valid_repos)} DISCREPANCY TABLE")
    print("="*60)
    print(f"{'Repo':<25} | {'Status':<7} | {'Reason'}")
    print("-"*60)
    for lang, repo, status, reason in sorted(file_status, key=lambda x: (x[0], x[1])):
        name = f"{lang}/{repo}"
        print(f"{name:<25} | {status:<7} | {reason}")
        
    print("\n" + "="*60)
    print("STEP 2: EXACT GAP OF MISSING REPOS (excluded repos are not counted as missing)")
    print("="*60)
    missing_by_lang = {}
    total_excluded = 0
    for lang, v in config.items():
        if not isinstance(v, dict): continue
        missing = []
        for r in v.get("repos", []):
            if r.get("excluded"):
                total_excluded += 1
                continue
            if f"{lang}/{r['name']}" not in valid_repos:
                missing.append(r['name'])
        if missing:
            missing_by_lang[lang] = missing
            print(f"{lang:10} ({len(missing):>2} missing): {', '.join(missing)}")
    print(f"\n({total_excluded} formally-excluded repos across all languages were skipped in this gap check — see README's Methodological Exclusions table)")

    print("\n" + "="*60)
    print("STEP 4: COMMANDS TO RUN (Copy & Paste)")
    print("="*60)
    print("cd Backend  # run from the Backend/ directory of this project")
    for lang in missing_by_lang:
        print(f"python run_language_batch.py --language {lang}")

if __name__ == "__main__":
    check_toolchains()
    analyze_results()
