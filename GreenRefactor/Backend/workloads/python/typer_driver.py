"""Workload driver for typer
Exercises Typer CLI definition and parameter parsing.
"""
import sys
import os

repo_root = os.path.join(os.path.dirname(__file__), "..", "..", "repos", "python", "typer")
sys.path.insert(0, repo_root)

import typer
from typer.testing import CliRunner

app = typer.Typer()
runner = CliRunner()

@app.command()
def create_user(username: str, role: str = typer.Option("guest"), active: bool = typer.Option(True)):
    _ = f"Creating {username} with role {role}. Active: {active}"

@app.command()
def process_data(file_path: str, lines: int = typer.Argument(100), dry_run: bool = typer.Option(False)):
    _ = f"Processing {lines} lines from {file_path}. Dry run: {dry_run}"

def run_workload():
    for i in range(2500):
        # 1. create_user
        res1 = runner.invoke(app, ["create-user", f"user_{i}", "--role", "admin", "--active"])
        assert res1.exit_code == 0
        
        # 2. process_data
        res2 = runner.invoke(app, ["process-data", f"/tmp/data_{i}.csv", str(i % 100), "--dry-run"])
        assert res2.exit_code == 0

if __name__ == "__main__":
    run_workload()
    print("OK: typer workload finished")
