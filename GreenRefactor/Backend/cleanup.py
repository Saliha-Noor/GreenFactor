import os
import glob
import shutil
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
greenrefactor_dir = os.path.abspath(os.path.join(backend_dir, ".."))
workspace_dir = os.path.abspath(os.path.join(greenrefactor_dir, ".."))
project_root = workspace_dir

print("🧹 Starting Comprehensive GreenRefactor Project Cleanup...\n")

# 1. Restore original files from .orig backups
print("1. Restoring original benchmark files from .orig backups...")
orig_count = 0
for search_path in [greenrefactor_dir, workspace_dir]:
    for orig in glob.glob(os.path.join(search_path, "**", "*.orig"), recursive=True):
        target = orig[:-5]
        print(f"   [restore] {os.path.basename(target)}")
        shutil.copy2(orig, target)
        os.remove(orig)
        orig_count += 1
if orig_count == 0:
    print("   ✓ No .orig backup files found.")

# 2. Delete JVM crash log and replay log files
print("\n2. Removing JVM crash logs and temporary log files...")
logs = (
    glob.glob(os.path.join(workspace_dir, "*.log")) +
    glob.glob(os.path.join(workspace_dir, "**", "*.log"), recursive=True) +
    glob.glob(os.path.join(greenrefactor_dir, "*.log")) +
    glob.glob(os.path.join(greenrefactor_dir, "**", "*.log"), recursive=True)
)
log_count = 0
for log_file in set(logs):
    if os.path.isfile(log_file):
        try:
            os.remove(log_file)
            print(f"   [deleted log] {os.path.basename(log_file)}")
            log_count += 1
        except Exception as e:
            print(f"   [warning] Could not delete {log_file}: {e}")
if log_count == 0:
    print("   ✓ No .log crash files found.")

# 3. Delete unneeded scratch/deprecated files
print("\n3. Removing unneeded scratch and deprecated files...")
trash_files = [
    os.path.join(backend_dir, "test_parse.py"),
]
# These three were previously force-deleted unconditionally, on the assumption
# they were leftover scratch components. That assumption doesn't hold anymore --
# the current frontend uses these as real, live tabs (same names, still wired to
# this backend's API) -- so deleting them here would silently break the UI with
# no confirmation prompt. Only touch them if the caller explicitly opts in.
frontend_candidates = [
    os.path.join(project_root, "greenrefactor", "Frontend", "src", "components", "CodePlaygroundTab.jsx"),
    os.path.join(project_root, "greenrefactor", "Frontend", "src", "components", "RepoExplorerTab.jsx"),
    os.path.join(project_root, "greenrefactor", "Frontend", "src", "components", "PatternCatalogTab.jsx"),
]
if "--delete-frontend-scratch" in sys.argv:
    trash_files.extend(frontend_candidates)
else:
    existing = [f for f in frontend_candidates if os.path.exists(f)]
    if existing:
        print("   [skipped] These look like LIVE frontend tab components, not scratch files:")
        for f in existing:
            print(f"     - {os.path.relpath(f, project_root)}")
        print("   Re-run with --delete-frontend-scratch if you're certain they're unused.")
trash_count = 0
for t_file in trash_files:
    if os.path.exists(t_file):
        try:
            os.remove(t_file)
            print(f"   [deleted file] {os.path.relpath(t_file, project_root)}")
            trash_count += 1
        except Exception as e:
            print(f"   [warning] Could not delete {t_file}: {e}")
if trash_count == 0:
    print("   ✓ No unnecessary scratch files found.")

# 4. Clean Python bytecode and pytest caches
print("\n4. Cleaning Python bytecode and test caches...")
cache_dirs = (
    glob.glob(os.path.join(project_root, "**", "__pycache__"), recursive=True) +
    glob.glob(os.path.join(project_root, "**", ".pytest_cache"), recursive=True)
)
cache_count = 0
for cache_dir in set(cache_dirs):
    if os.path.exists(cache_dir):
        try:
            shutil.rmtree(cache_dir, ignore_errors=True)
            print(f"   [deleted cache] {os.path.relpath(cache_dir, project_root)}")
            cache_count += 1
        except Exception as e:
            pass
if cache_count == 0:
    print("   ✓ No bytecode/test cache directories found.")

print("\n✨ Cleanup Complete! All unnecessary log, cache, and scratch files have been removed.")
