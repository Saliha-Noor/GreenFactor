"""
LLM Review Agent — for the 4 patterns that need semantic/domain judgment
and can't be safely auto-detected or auto-refactored by regex:
    - offload_to_native
    - high_perf_libraries
    - high_perf_data_structures
    - swap_library_impl

This agent only SUGGESTS. It never edits the file. A human (or the
Refactoring Agent, only after a person manually accepts the suggestion)
applies the change, then it goes through the same verify -> measure ->
stats path as everything else.

Requires GROQ_API_KEY in the environment. No key is hardcoded here.
"""
import json
import os
import urllib.request

GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SEMANTIC_PATTERNS = [
    "offload_to_native", "high_perf_libraries", "high_perf_data_structures", "swap_library_impl",
]

PROMPT_TEMPLATE = """You are reviewing a source file for energy-refactoring opportunities.
Language: {language}
Only consider these patterns, and ONLY report something if you are confident:
- offload_to_native: a hot pure-compute loop that could be moved to a native/compiled extension
- high_perf_libraries: use of a slow stdlib routine where a well-known faster library exists
- high_perf_data_structures: wrong data structure for the access pattern (e.g. list where a set/dict is used for membership checks)
- swap_library_impl: a heavier library used where a lighter, faster one does the same job

Respond ONLY with a JSON array (no prose, no markdown fences). Each element:
{{"pattern": "<one of the 4 names above>", "line": <int>, "reasoning": "<one sentence>", "confidence": "high"|"medium"|"low"}}
If nothing qualifies, respond with [].

File contents:
{code}
"""


def review_file(file_path: str, language: str) -> list[dict]:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY not set — LLM review skipped, semantic patterns will need manual review")

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    prompt = PROMPT_TEMPLATE.format(language=language, code=code[:8000])  # keep prompt bounded
    payload = json.dumps({
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }).encode()

    req = urllib.request.Request(
        GROQ_URL, data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())

    text = data["choices"][0]["message"]["content"].strip()
    text = text.strip("`").removeprefix("json").strip()
    try:
        suggestions = json.loads(text)
    except json.JSONDecodeError:
        return []

    # drop low-confidence and anything outside the 4 allowed patterns — never auto-apply these anyway
    return [
        s for s in suggestions
        if isinstance(s, dict) and s.get("pattern") in SEMANTIC_PATTERNS and s.get("confidence") != "low"
    ]
