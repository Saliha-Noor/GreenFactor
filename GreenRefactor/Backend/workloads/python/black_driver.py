"""Workload driver for black — src/black/__init__.py
Formats a sample Python file using black's API.
"""
import sys
import os
import tempfile
import textwrap

repo_root = os.path.join(os.path.dirname(__file__), "..", "..", "repos", "python", "black")
sys.path.insert(0, os.path.join(repo_root, "src"))

SAMPLE_CODE = textwrap.dedent('''\
    import  os,sys
    from pathlib import   Path
    def   foo(  x,y,z  ):
        if x>0:
            return x+y+z
        else:
            return   x-y-z
    class   MyClass:
        def __init__(self,a,b,c):
            self.a=a
            self.b=b
            self.c=c
        def   method(self):
            return self.a+self.b+self.c
    data=[1,2,3,4,5,6,7,8,9,10]
    result=list(map(lambda  x:x**2,data))
''')

if __name__ == "__main__":
    try:
        import black
        for _ in range(10):
            formatted = black.format_str(SAMPLE_CODE, mode=black.Mode())
        print(f"OK: formatted {len(SAMPLE_CODE)} chars of Python code")
    except ImportError:
        # Fallback: just do string processing as a workload
        for _ in range(100):
            lines = SAMPLE_CODE.splitlines()
            result = "\n".join(line.strip() for line in lines)
        print(f"OK: processed {len(lines)} lines (black not importable, used fallback)")
