"""
Agent 2 - Pattern Detection Agent

Regex and heuristic-based pattern detector for multi-language AST scanning
across all 8 target programming languages.

Covers the 4 mechanical patterns:
    - cache_reuse
    - batch_operations
    - early_termination
    - avoid_redundant_computation

The remaining 4 semantic patterns (offload_to_native, high_perf_libraries,
high_perf_data_structures, swap_library_impl) are analyzed via llm_review_agent.py.
"""
import re
from dataclasses import dataclass, field


@dataclass
class PatternHit:
    pattern: str
    file_path: str
    line_number: int
    snippet: str
    confidence: str  # "high" | "medium" | "low"


# ---------------------------------------------------------------------------
# Per-language syntax hints for the 4 mechanical patterns
# ---------------------------------------------------------------------------
LOOP_KEYWORDS = {
    "python": r"for\s+\w+\s+in\s+", "java": r"for\s*\(", "cpp": r"for\s*\(", "c": r"for\s*\(",
    "go": r"for\s+", "rust": r"for\s+\w+\s+in\s+", "csharp": r"for\s*\(|foreach\s*\(",
    "javascript": r"for\s*\(|\.forEach\(|\.map\(",
}

# a `break`/`return` INSIDE a loop body already handles early-termination —
# absence of one where an if-condition clearly signals "found it" is the flag
FOUND_CONDITION_RE = re.compile(
    r"if\s*\(?.*(found|match|==\s*target|is\s+target).*\)?\s*[:{]", re.IGNORECASE
)
BREAK_KEYWORDS = {
    "python": "break", "java": "break", "cpp": "break", "c": "break",
    "go": "break", "rust": "break", "csharp": "break", "javascript": "break",
}

# recomputing the same call/expression across iterations of the SAME loop body
REPEATED_CALL_RE = re.compile(r"(\b[\w\.]+\([^()]*\))")

# single-item DB/file/network calls placed inside a loop = missed batching
PER_ITEM_IO_HINTS = [
    r"\.save\(", r"\.insert\(", r"\.execute\(", r"\.write\(", r"\.append\(.*\)\s*$",
    r"requests\.(get|post)\(", r"fetch\(", r"\.query\(",
]

# already-memoized markers (so we don't flag something already cached)
CACHE_MARKERS = {
    "python": [r"@lru_cache", r"@cache", r"functools\.cache", r"functools\.lru_cache"],
    "java": [r"Cache<", r"ConcurrentHashMap.*computeIfAbsent"],
    "csharp": [r"MemoryCache", r"ConcurrentDictionary.*GetOrAdd"],
    "javascript": [r"memoize\(", r"new Map\(\)"],
    "go": [r"sync\.Map", r"sync\.Once"],
    "rust": [r"lazy_static", r"once_cell", r"HashMap::new\(\)\.entry"],
    "cpp": [r"std::unordered_map.*cache", r"static\s+std::map"],
    "c": [r"static\s+.*cache"],
}

FUNC_DEF_RE = {
    "python": re.compile(r"^\s*def\s+(\w+)\s*\("),
    "java": re.compile(r"^\s*(public|private|protected|static).*\s(\w+)\s*\([^;]*\)\s*\{"),
    "csharp": re.compile(r"^\s*(public|private|protected|static).*\s(\w+)\s*\([^;]*\)\s*\{"),
    "cpp": re.compile(r"^\s*[\w:<>&\*]+\s+(\w+)\s*\([^;]*\)\s*\{"),
    "c": re.compile(r"^\s*[\w\*]+\s+(\w+)\s*\([^;]*\)\s*\{"),
    "go": re.compile(r"^\s*func\s+(\w+)\s*\("),
    "rust": re.compile(r"^\s*(pub\s+)?fn\s+(\w+)\s*\("),
    "javascript": re.compile(r"^\s*function\s+(\w+)\s*\(|^\s*const\s+(\w+)\s*=\s*\("),
}


def _lines(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.readlines()


def detect_cache_reuse(file_path: str, language: str) -> list[PatternHit]:
    """Flag pure-looking functions (no I/O keywords, called with the same
    args repeatedly nearby) that AREN'T already memoized."""
    lines = _lines(file_path)
    text = "".join(lines)
    already_cached = any(re.search(m, text) for m in CACHE_MARKERS.get(language, []))
    if already_cached:
        return []
    hits = []
    func_re = FUNC_DEF_RE.get(language)
    if not func_re:
        return []
    for i, line in enumerate(lines):
        m = func_re.match(line)
        if not m:
            continue
        fname = next((g for g in m.groups() if g and g not in ("public", "private", "protected", "static", "pub ")), None)
        if not fname:
            continue
        # heuristic: the point of caching is "same input -> skip recompute", so we
        # only flag this as a cache_reuse candidate if the SAME call, with the SAME
        # argument text, appears 2+ times elsewhere in the file. Calling a function
        # with different arguments each time is not something a cache would help with.
        call_re = re.compile(rf"\b{re.escape(fname)}\s*\(([^()]*)\)")
        arg_lists = call_re.findall(text)
        if not arg_lists:
            continue
        from collections import Counter
        counts = Counter(a.strip() for a in arg_lists)
        # exclude the definition line itself's "call" (won't match since def uses
        # `def name(` not `name(`, so no adjustment needed here)
        repeated_same_args = any(c >= 2 for c in counts.values())
        if repeated_same_args:
            hits.append(PatternHit(
                pattern="cache_reuse", file_path=file_path, line_number=i + 1,
                snippet=line.strip(), confidence="medium",
            ))
    return hits


def detect_early_termination(file_path: str, language: str) -> list[PatternHit]:
    lines = _lines(file_path)
    loop_re = re.compile(LOOP_KEYWORDS.get(language, r"for\s*\("))
    hits = []
    in_loop_at = None
    loop_indent = ""
    for i, line in enumerate(lines):
        if loop_re.search(line):
            in_loop_at = i
            loop_indent = re.match(r"(\s*)", line).group(1)
            continue
        # once we dedent back to (or past) the loop's own indent level, we've left
        # its body entirely -- stop treating later lines as "inside this loop"
        if in_loop_at is not None and line.strip() and \
                len(re.match(r"(\s*)", line).group(1)) <= len(loop_indent):
            in_loop_at = None
        if in_loop_at is not None and FOUND_CONDITION_RE.search(line):
            if_indent = re.match(r"(\s*)", line).group(1)
            # scan only the if-block itself (lines more indented than the if),
            # not unrelated code after the block ends
            has_exit = False
            for j in range(i + 1, min(i + 15, len(lines))):
                body_line = lines[j]
                if not body_line.strip():
                    continue
                body_indent = re.match(r"(\s*)", body_line).group(1)
                if len(body_indent) <= len(if_indent):
                    break  # if-block ended
                if BREAK_KEYWORDS.get(language, "break") in body_line or "return" in body_line:
                    has_exit = True
                    break
            if not has_exit:
                hits.append(PatternHit(
                    pattern="early_termination", file_path=file_path, line_number=i + 1,
                    snippet=line.strip(), confidence="low",
                ))
            in_loop_at = None
    return hits


def detect_batch_operations(file_path: str, language: str) -> list[PatternHit]:
    lines = _lines(file_path)
    loop_re = re.compile(LOOP_KEYWORDS.get(language, r"for\s*\("))
    io_re = re.compile("|".join(PER_ITEM_IO_HINTS))
    hits = []
    in_loop = False
    loop_indent = ""
    for i, line in enumerate(lines):
        if loop_re.search(line):
            in_loop = True
            loop_indent = re.match(r"(\s*)", line).group(1)
            continue
        # dedenting back to (or past) the loop's own indent means we've left its
        # body -- without this, every I/O call for the rest of the file (even in
        # unrelated functions) gets flagged as "inside a loop needing batching"
        if in_loop and line.strip() and \
                len(re.match(r"(\s*)", line).group(1)) <= len(loop_indent):
            in_loop = False
        if in_loop and io_re.search(line):
            hits.append(PatternHit(
                pattern="batch_operations", file_path=file_path, line_number=i + 1,
                snippet=line.strip(), confidence="medium",
            ))
    return hits


def detect_avoid_redundant_computation(file_path: str, language: str) -> list[PatternHit]:
    lines = _lines(file_path)
    loop_re = re.compile(LOOP_KEYWORDS.get(language, r"for\s*\("))
    hits = []
    in_loop_body: list[str] = []
    collecting = False
    loop_indent = ""
    for i, line in enumerate(lines):
        if loop_re.search(line):
            collecting = True
            in_loop_body = []
            loop_indent = re.match(r"(\s*)", line).group(1)
            continue
        if collecting:
            if line.strip() and len(re.match(r"(\s*)", line).group(1)) <= len(loop_indent):
                collecting = False  # dedented back out of the loop body
                continue
            in_loop_body.append(line)
            calls = REPEATED_CALL_RE.findall(line)
            for call in calls:
                # invariant-looking: no loop-index-like variable name in the call args
                if not re.search(r"\[i\]|\[j\]|\[idx\]|_i\b", call):
                    count_in_body = "".join(in_loop_body).count(call)
                    if count_in_body >= 2:
                        hits.append(PatternHit(
                            pattern="avoid_redundant_computation", file_path=file_path,
                            line_number=i + 1, snippet=call, confidence="low",
                        ))
            if len(in_loop_body) > 15:
                collecting = False
    return hits


DETECTORS = {
    "cache_reuse": detect_cache_reuse,
    "early_termination": detect_early_termination,
    "batch_operations": detect_batch_operations,
    "avoid_redundant_computation": detect_avoid_redundant_computation,
}


def scan_file(file_path: str, language: str) -> list[PatternHit]:
    hits = []
    for name, fn in DETECTORS.items():
        try:
            hits.extend(fn(file_path, language))
        except Exception as e:
            print(f"[pattern-detect] {name} failed on {file_path}: {e}")
    return hits
