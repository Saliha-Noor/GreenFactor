"""Workload driver for rich
Exercises Console rendering of Tables, Trees, and Syntax into an in-memory buffer.
"""
import sys
import os
import io

repo_root = os.path.join(os.path.dirname(__file__), "..", "..", "repos", "python", "rich")
sys.path.insert(0, repo_root)

from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.syntax import Syntax

def run_workload():
    buf = io.StringIO()
    console = Console(file=buf, force_terminal=True, width=120)
    
    code = '''
def hello_world(name):
    print(f"Hello {name}")
    for i in range(10):
        yield i
'''

    for i in range(1000):
        # 1. Render Table
        table = Table(title=f"Benchmark Table {i}")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Status", justify="right", style="green")
        for r in range(10):
            table.add_row(str(r), f"Row_{r}_{i}", "Success")
        console.print(table)
        
        # 2. Render Tree
        tree = Tree(f"Root_{i}")
        for j in range(3):
            child = tree.add(f"Child_{j}")
            child.add(f"Grandchild_{j}_1")
            child.add(f"Grandchild_{j}_2")
        console.print(tree)
        
        # 3. Render Syntax
        syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
        console.print(syntax)
        
        # Clear buffer periodically to avoid memory exhaustion
        if i % 100 == 0:
            buf.seek(0)
            buf.truncate(0)

if __name__ == "__main__":
    run_workload()
    print("OK: rich workload finished")
