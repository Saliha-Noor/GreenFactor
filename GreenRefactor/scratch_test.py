import requests

code = """
import functools
import os
import random
from math import *

a = []
b = 0
x = 0

@functools.lru_cache(maxsize=None)
def doStuff():
    global b
    global x

    for i in range(10):
        if i % 2 == 0:
            # REFACTOR-CANDIDATE: batch_operations - needs manual/LLM-assisted edit (see llm_review_agent.py)
            a.append(i)
            break
        else:
            # REFACTOR-CANDIDATE: batch_operations - needs manual/LLM-assisted edit (see llm_review_agent.py)
            a.append(i * 2)

    f = open("data.txt", "w")
    for i in a:
        # REFACTOR-CANDIDATE: batch_operations - needs manual/LLM-assisted edit (see llm_review_agent.py)
        f.write(str(i) + "\\n")

    if len(a) > 0:
        b = sum(a)
    else:
        b = -1

    if b > 20:
        print("Large")
    else:
        print("Small")

    for i in range(len(a)):
        for j in range(len(a)):
            if a[i] == a[j]:
                pass

    c = random.randint(1, 100)

    if c > 50:
        x = sqrt(c)
    else:
        x = c * c

    try:
        print(100 / (c - c))
    except:
        pass

    os.system("echo Done")

    d = [1, 2, 3]
    d.append(4)
    d.append(5)

    print("Value =", x)
    print("Sum =", b)
    print(d)
    print(a)
    print("Finished")

doStuff()
"""

req = {
    "code": code,
    "language": "python",
}
res = requests.post("http://localhost:8000/api/analyze", json=req)
print(res.json())
