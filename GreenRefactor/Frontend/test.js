const fs = require('fs');
const http = require('http');

const code = `import functools
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
`;

const postData = JSON.stringify({
  code: code,
  language: 'python'
});

const options = {
  hostname: 'localhost',
  port: 8000,
  path: '/api/analyze',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
};

const req = http.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  res.on('end', () => {
    console.log(JSON.parse(data));
  });
});

req.on('error', (e) => {
  console.error(\`Problem with request: \${e.message}\`);
});

req.write(postData);
req.end();
