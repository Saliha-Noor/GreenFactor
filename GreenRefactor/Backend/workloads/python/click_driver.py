"""Workload driver for click
Exercises CLI parsing and command routing using the internal CliRunner.
"""
import sys
import os

repo_root = os.path.join(os.path.dirname(__file__), "..", "..", "repos", "python", "click", "src")
sys.path.insert(0, repo_root)

import click
from click.testing import CliRunner

@click.group()
def cli():
    pass

@cli.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
@click.option('--verbose/--no-verbose', default=False)
def hello(count, name, verbose):
    for x in range(count):
        _ = f"Hello {name}!"

@cli.command()
@click.argument('src')
@click.argument('dest')
@click.option('--recursive', '-r', is_flag=True)
def copy(src, dest, recursive):
    _ = f"Copying {src} to {dest}"

def run_workload():
    runner = CliRunner()
    
    # Generate CPU load by repeatedly invoking commands with different arguments
    for i in range(2500):
        # Test 1: hello with options
        res1 = runner.invoke(cli, ['hello', '--count', '5', '--name', f'User{i}', '--verbose'])
        assert res1.exit_code == 0
        
        # Test 2: copy with arguments and flags
        res2 = runner.invoke(cli, ['copy', f'/tmp/src_{i}.txt', f'/tmp/dest_{i}.txt', '-r'])
        assert res2.exit_code == 0

if __name__ == "__main__":
    run_workload()
    print("OK: click workload finished")
