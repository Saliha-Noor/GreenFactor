"""
Agent 3 - Refactoring Agent

Implements automated code transformations for mechanical green patterns
(early_termination, avoid_redundant_computation, batch_operations, cache_reuse)
across target programming languages (Python, JavaScript, Java, C#, C++, C, Go, Rust).

Transformation behavior:
  - Creates a .orig backup prior to modifying source files.
  - Returns a RefactorResult object allowing rollback via restore().
  - Falls back to safe comment flagging (REFACTOR-CANDIDATE) for complex or
    flagged-only patterns like batch_operations.
"""
import os
import re
import shutil
from dataclasses import dataclass

from agents.pattern_detection_agent import PatternHit, LOOP_KEYWORDS


@dataclass
class RefactorResult:
    applied: bool
    method: str  # "auto" | "flagged-only" | "skipped-no-handler"
    backup_path: str


def _backup(file_path: str) -> str:
    backup_path = file_path + ".orig"
    if not os.path.exists(backup_path):
        shutil.copyfile(file_path, backup_path)
    return backup_path


def restore(file_path: str) -> None:
    backup_path = file_path + ".orig"
    if os.path.exists(backup_path):
        shutil.copyfile(backup_path, file_path)


def _indent_of(line: str) -> str:
    return re.match(r"(\s*)", line).group(1)


def _find_matching_close_brace(lines: list[str], start_idx: int, indent: str):
    """First later line that is JUST a closing brace at the same indent as
    the opening definition line. Same simplifying assumption the original
    JS cache_reuse handler used — a real brace-matcher would need a proper
    tokenizer; this is heuristic and can miss unusually-formatted code
    (in which case the caller bails to flagged-only, never guesses)."""
    for j in range(start_idx + 1, len(lines)):
        if lines[j].rstrip() == f"{indent}}}":
            return j
    return None


def _param_names(params: str) -> list[str]:
    names = []
    for seg in params.split(","):
        seg = seg.strip()
        if not seg:
            continue
        toks = seg.split()
        tok = toks[-1] if toks else seg
        tok = re.sub(r"^[\*&\[\]]+", "", tok)
        if tok:
            names.append(tok)
    return names


# ===========================================================================
# cache_reuse
# ===========================================================================

# ---- python (tested) ----
def _apply_cache_python(file_path: str, hit: PatternHit) -> RefactorResult:
    backup_path = _backup(file_path)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    target_idx = hit.line_number - 1
    if target_idx < 0 or target_idx >= len(lines):
        return RefactorResult(False, "skipped-no-handler", backup_path)

    if "def " not in lines[target_idx]:
        return RefactorResult(False, "skipped-no-handler", backup_path)

    already = target_idx > 0 and "lru_cache" in lines[target_idx - 1]
    if already:
        return RefactorResult(False, "skipped-no-handler", backup_path)

    indent = _indent_of(lines[target_idx])
    lines.insert(target_idx, f"{indent}@functools.lru_cache(maxsize=None)\n")

    text = "".join(lines)
    if "import functools" not in text:
        lines.insert(0, "import functools\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return RefactorResult(True, "auto", backup_path)


# ---- javascript (tested) ----
def _apply_cache_javascript(file_path: str, hit: PatternHit) -> RefactorResult:
    backup_path = _backup(file_path)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    target_idx = hit.line_number - 1
    if target_idx < 0 or target_idx >= len(lines):
        return RefactorResult(False, "skipped-no-handler", backup_path)

    m = re.match(r"(\s*)function\s+(\w+)\s*\(", lines[target_idx])
    if not m:
        return RefactorResult(False, "skipped-no-handler", backup_path)
    indent, fname = m.group(1), m.group(2)

    lines[target_idx] = lines[target_idx].replace(f"function {fname}(", f"function {fname}__impl(")
    end_idx = None
    for j in range(target_idx + 1, len(lines)):
        if lines[j].rstrip() == f"{indent}}}":
            end_idx = j
            break
    if end_idx is None:
        restore(file_path)
        return RefactorResult(False, "skipped-no-handler", backup_path)

    wrapper = (
        f"{indent}const {fname}__cache = new Map();\n"
        f"{indent}function {fname}(...args) {{\n"
        f"{indent}  const key = JSON.stringify(args);\n"
        f"{indent}  if ({fname}__cache.has(key)) return {fname}__cache.get(key);\n"
        f"{indent}  const result = {fname}__impl(...args);\n"
        f"{indent}  {fname}__cache.set(key, result);\n"
        f"{indent}  return result;\n"
        f"{indent}}}\n"
    )
    lines.insert(end_idx + 1, wrapper)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return RefactorResult(True, "auto", backup_path)


# ---- shared generic builder for the brace-language cache handlers ----
def _build_cache_wrapper_generic(file_path, hit, parse_fn, build_fn):
    backup_path = _backup(file_path)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    idx = hit.line_number - 1
    if idx >= len(lines):
        return RefactorResult(False, "skipped-no-handler", backup_path)

    parsed = parse_fn(lines[idx])
    if not parsed:
        return RefactorResult(False, "skipped-no-handler", backup_path)

    indent = parsed["indent"]
    end_idx = _find_matching_close_brace(lines, idx, indent)
    if end_idx is None:
        return RefactorResult(False, "skipped-no-handler", backup_path)

    built = build_fn(parsed)
    impl_line, wrapper_text = built[0], built[1]
    extra_top = built[2] if len(built) > 2 else None

    lines[idx] = impl_line
    lines.insert(end_idx + 1, wrapper_text)

    if extra_top:
        text = "".join(lines)
        for top_line in reversed(extra_top):
            probe = top_line.strip()
            if probe and probe not in text:
                lines.insert(0, top_line if top_line.endswith("\n") else top_line + "\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return RefactorResult(True, "auto", backup_path)


# ---- java ----
_JAVA_SIG_RE = re.compile(
    r"^(?P<indent>\s*)(?P<mods>(?:(?:public|private|protected|static|final|synchronized)\s+)*)"
    r"(?P<ret>[\w<>\[\],\.]+)\s+(?P<name>\w+)\s*\((?P<params>[^)]*)\)\s*\{"
)
_JAVA_BOX = {
    "int": "Integer", "long": "Long", "double": "Double", "float": "Float",
    "boolean": "Boolean", "char": "Character", "byte": "Byte", "short": "Short",
}


def _java_cache_parse(line):
    m = _JAVA_SIG_RE.match(line)
    if not m:
        return None
    ret = m.group("ret").strip()
    if ret == "void":
        return None
    return {
        "indent": m.group("indent"), "mods": m.group("mods"), "ret": ret,
        "name": m.group("name"), "params": m.group("params").strip(),
    }


def _java_cache_build(p):
    indent, mods, ret, name, params = p["indent"], p["mods"], p["ret"], p["name"], p["params"]
    names = _param_names(params)
    map_type = _JAVA_BOX.get(ret, ret)
    key_expr = " + \"|\" + ".join(f"String.valueOf({n})" for n in names) if names else '"noargs"'
    impl_line = f"{indent}{mods}{ret} {name}Impl({params}) {{\n"
    wrapper = (
        f"{indent}private static final java.util.Map<String, {map_type}> {name}Cache = "
        f"new java.util.concurrent.ConcurrentHashMap<>();\n"
        f"{indent}{mods}{ret} {name}({params}) {{\n"
        f"{indent}    String __key = {key_expr};\n"
        f"{indent}    if ({name}Cache.containsKey(__key)) return {name}Cache.get(__key);\n"
        f"{indent}    {ret} __result = {name}Impl({', '.join(names)});\n"
        f"{indent}    {name}Cache.put(__key, __result);\n"
        f"{indent}    return __result;\n"
        f"{indent}}}\n"
    )
    return impl_line, wrapper


def _apply_cache_java(file_path: str, hit: PatternHit) -> RefactorResult:
    return _build_cache_wrapper_generic(file_path, hit, _java_cache_parse, _java_cache_build)


# ---- csharp ----
_CSHARP_SIG_RE = re.compile(
    r"^(?P<indent>\s*)(?P<mods>(?:(?:public|private|protected|internal|static|virtual|override|sealed|async)\s+)*)"
    r"(?P<ret>[\w<>\[\],\.]+)\s+(?P<name>\w+)\s*\((?P<params>[^)]*)\)\s*\{"
)


def _csharp_cache_parse(line):
    m = _CSHARP_SIG_RE.match(line)
    if not m:
        return None
    ret = m.group("ret").strip()
    if ret == "void":
        return None
    return {
        "indent": m.group("indent"), "mods": m.group("mods"), "ret": ret,
        "name": m.group("name"), "params": m.group("params").strip(),
    }


def _csharp_cache_build(p):
    indent, mods, ret, name, params = p["indent"], p["mods"], p["ret"], p["name"], p["params"]
    names = _param_names(params)
    key_expr = " + \"|\" + ".join(f"System.Convert.ToString({n})" for n in names) if names else '"noargs"'
    impl_line = f"{indent}{mods}{ret} {name}Impl({params}) {{\n"
    wrapper = (
        f"{indent}private static readonly System.Collections.Concurrent.ConcurrentDictionary<string, {ret}> "
        f"{name}Cache = new System.Collections.Concurrent.ConcurrentDictionary<string, {ret}>();\n"
        f"{indent}{mods}{ret} {name}({params}) {{\n"
        f"{indent}    string __key = {key_expr};\n"
        f"{indent}    if ({name}Cache.TryGetValue(__key, out var __cached)) return __cached;\n"
        f"{indent}    {ret} __result = {name}Impl({', '.join(names)});\n"
        f"{indent}    {name}Cache[__key] = __result;\n"
        f"{indent}    return __result;\n"
        f"{indent}}}\n"
    )
    return impl_line, wrapper


def _apply_cache_csharp(file_path: str, hit: PatternHit) -> RefactorResult:
    return _build_cache_wrapper_generic(file_path, hit, _csharp_cache_parse, _csharp_cache_build)


# ---- cpp (scoped to 0-1 parameter, see module docstring) ----
_CPP_SIG_RE = re.compile(
    r"^(?P<indent>\s*)(?P<mods>(?:(?:static|inline|virtual|constexpr)\s+)*)"
    r"(?P<ret>[\w:<>&\*]+)\s+(?P<name>\w+)\s*\((?P<params>[^)]*)\)\s*\{"
)
_CPP_NUMERIC = {
    "int", "long", "short", "float", "double", "unsigned", "size_t", "bool",
    "char", "long long", "unsigned long", "unsigned int", "unsigned short",
}


def _split_params_angle_aware(params_str: str) -> list[str]:
    """Split a C++ parameter list on commas, but ignore commas inside
    angle brackets (template arguments like std::map<int, int>)."""
    parts = []
    depth = 0
    current = []
    for ch in params_str:
        if ch == '<':
            depth += 1
            current.append(ch)
        elif ch == '>':
            depth = max(depth - 1, 0)
            current.append(ch)
        elif ch == ',' and depth == 0:
            parts.append(''.join(current).strip())
            current = []
        else:
            current.append(ch)
    tail = ''.join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def _cpp_cache_parse(line):
    m = _CPP_SIG_RE.match(line)
    if not m:
        return None
    ret = m.group("ret").strip()
    if ret == "void":
        return None
    params = m.group("params").strip()
    # Use angle-bracket-aware splitter so template types like
    # std::map<int, int> don't look like two separate parameters.
    parts = [s for s in _split_params_angle_aware(params) if s]
    if len(parts) > 1:
        return None  # scoped to 0-1 param — see module docstring
    pname, ptype = None, None
    if parts:
        seg = parts[0]
        toks = seg.split()
        if not toks:
            return None
        tok = toks[-1]
        pname = re.sub(r"^[\*&]+", "", tok)
        ptype = seg[: seg.rfind(tok)].strip()
    return {
        "indent": m.group("indent"), "mods": m.group("mods"), "ret": ret,
        "name": m.group("name"), "params": params, "pname": pname, "ptype": ptype,
    }


def _cpp_cache_build(p):
    indent, mods, ret, name, params = p["indent"], p["mods"], p["ret"], p["name"], p["params"]
    pname, ptype = p["pname"], p["ptype"]
    if pname is None:
        key_expr, arg = '"noargs"', ""
    else:
        base = ptype.replace("const", "").replace("&", "").strip()
        if base in _CPP_NUMERIC or base.endswith("int"):
            key_expr = f"std::to_string({pname})"
        else:
            key_expr = f"std::string({pname})"
        arg = pname
    impl_line = f"{indent}{mods}{ret} {name}Impl({params}) {{\n"
    wrapper = (
        f"{indent}static std::unordered_map<std::string, {ret}> {name}_cache;\n"
        f"{indent}{mods}{ret} {name}({params}) {{\n"
        f"{indent}    std::string __key = {key_expr};\n"
        f"{indent}    auto __it = {name}_cache.find(__key);\n"
        f"{indent}    if (__it != {name}_cache.end()) return __it->second;\n"
        f"{indent}    {ret} __result = {name}Impl({arg});\n"
        f"{indent}    {name}_cache[__key] = __result;\n"
        f"{indent}    return __result;\n"
        f"{indent}}}\n"
    )
    extra_top = ["#include <unordered_map>", "#include <string>"]
    return impl_line, wrapper, extra_top


def _apply_cache_cpp(file_path: str, hit: PatternHit) -> RefactorResult:
    return _build_cache_wrapper_generic(file_path, hit, _cpp_cache_parse, _cpp_cache_build)


# ---- c (scoped to exactly 1 integer-like, non-pointer param — see module docstring) ----
_C_SIG_RE = re.compile(
    r"^(?P<indent>\s*)(?P<mods>(?:(?:static|inline)\s+)*)"
    r"(?P<ret>[\w\*]+)\s+(?P<name>\w+)\s*\((?P<params>[^)]*)\)\s*\{"
)
_C_INT_TYPES = {"int", "long", "short", "unsigned", "unsigned int", "unsigned long", "size_t", "long long"}


def _c_cache_parse(line):
    m = _C_SIG_RE.match(line)
    if not m:
        return None
    ret = m.group("ret").strip()
    if ret == "void" or "*" in ret:
        return None
    params = m.group("params").strip()
    parts = [s.strip() for s in params.split(",") if s.strip()]
    if len(parts) != 1:
        return None
    seg = parts[0]
    if "*" in seg:
        return None
    toks = seg.split()
    if not toks:
        return None
    pname = toks[-1]
    ptype = seg[: seg.rfind(pname)].strip()
    if ptype not in _C_INT_TYPES:
        return None
    return {
        "indent": m.group("indent"), "mods": m.group("mods"), "ret": ret,
        "name": m.group("name"), "params": params, "pname": pname,
    }


def _c_cache_build(p):
    indent, mods, ret, name, params, pname = p["indent"], p["mods"], p["ret"], p["name"], p["params"], p["pname"]
    impl_line = f"{indent}{mods}{ret} {name}Impl({params}) {{\n"
    wrapper = (
        f"{indent}static long {name}_cache_key[4096];\n"
        f"{indent}static {ret} {name}_cache_val[4096];\n"
        f"{indent}static char {name}_cache_set[4096];\n"
        f"{indent}{mods}{ret} {name}({params}) {{\n"
        f"{indent}    unsigned int __idx = ((unsigned long){pname}) & 4095u;\n"
        f"{indent}    if ({name}_cache_set[__idx] && {name}_cache_key[__idx] == (long){pname}) "
        f"return {name}_cache_val[__idx];\n"
        f"{indent}    {ret} __result = {name}Impl({pname});\n"
        f"{indent}    {name}_cache_key[__idx] = (long){pname};\n"
        f"{indent}    {name}_cache_val[__idx] = __result;\n"
        f"{indent}    {name}_cache_set[__idx] = 1;\n"
        f"{indent}    return __result;\n"
        f"{indent}}}\n"
    )
    return impl_line, wrapper


def _apply_cache_c(file_path: str, hit: PatternHit) -> RefactorResult:
    return _build_cache_wrapper_generic(file_path, hit, _c_cache_parse, _c_cache_build)


# ---- go (own function, not the generic builder — Go's import placement
#          rules mean the "insert at top of file" trick used for cpp
#          would break the required `package` line ordering) ----
_GO_SIG_RE = re.compile(
    r"^(?P<indent>\s*)func\s+(?P<name>\w+)\s*\((?P<params>[^)]*)\)\s*(?P<ret>[\w\[\]\*\.]*)\s*\{"
)


def _go_cache_parse(line):
    m = _GO_SIG_RE.match(line)
    if not m:
        return None
    ret = m.group("ret").strip()
    if not ret or ret == "error":
        return None  # no return value, or error-only return — nothing worth caching
    return {"indent": m.group("indent"), "ret": ret, "name": m.group("name"), "params": m.group("params").strip()}


def _go_param_names(params: str) -> list[str]:
    names = []
    for seg in params.split(","):
        seg = seg.strip()
        if not seg:
            continue
        toks = seg.split()
        if len(toks) > 0:
            names.append(toks[0]) # In Go, the name comes first: `x int`
    return names

def _go_cache_build(p):
    indent, ret, name, params = p["indent"], p["ret"], p["name"], p["params"]
    names = _go_param_names(params)
    args_literal = ", ".join(names)
    fmt_args = ", ".join(names) if names else '"noargs"'
    impl_line = f"{indent}func {name}Impl({params}) {ret} {{\n"
    wrapper = (
        f"{indent}var {name}Cache = map[string]{ret}{{}}\n"
        f"{indent}func {name}({params}) {ret} {{\n"
        f"{indent}    __key := fmt.Sprintf(\"%v\", []interface{{}}{{{fmt_args}}})\n"
        f"{indent}    if __v, __ok := {name}Cache[__key]; __ok {{\n"
        f"{indent}        return __v\n"
        f"{indent}    }}\n"
        f"{indent}    __result := {name}Impl({args_literal})\n"
        f"{indent}    {name}Cache[__key] = __result\n"
        f"{indent}    return __result\n"
        f"{indent}}}\n"
    )
    return impl_line, wrapper


def _apply_cache_go(file_path: str, hit: PatternHit) -> RefactorResult:
    backup_path = _backup(file_path)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    idx = hit.line_number - 1
    if idx >= len(lines):
        return RefactorResult(False, "skipped-no-handler", backup_path)

    parsed = _go_cache_parse(lines[idx])
    if not parsed:
        return RefactorResult(False, "skipped-no-handler", backup_path)

    indent = parsed["indent"]
    end_idx = _find_matching_close_brace(lines, idx, indent)
    if end_idx is None:
        return RefactorResult(False, "skipped-no-handler", backup_path)

    impl_line, wrapper_text = _go_cache_build(parsed)
    lines[idx] = impl_line
    lines.insert(end_idx + 1, wrapper_text)

    text = "".join(lines)
    if '"fmt"' not in text:
        for j, line in enumerate(lines):
            if line.strip().startswith("package "):
                lines.insert(j + 1, 'import "fmt"\n')
                break

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return RefactorResult(True, "auto", backup_path)


# cache_reuse x rust: intentionally NOT handled here — see module docstring.


# ===========================================================================
# early_termination
# ===========================================================================

# ---- python (tested; break-position bug fixed below — see docstring) ----
def _apply_early_termination_python(file_path: str, hit: PatternHit) -> RefactorResult:
    backup_path = _backup(file_path)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    idx = hit.line_number - 1
    if idx >= len(lines) or ":" not in lines[idx]:
        return RefactorResult(False, "skipped-no-handler", backup_path)
    if_indent = _indent_of(lines[idx])

    body_idx = idx + 1
    while body_idx < len(lines) and lines[body_idx].strip() == "":
        body_idx += 1
    if body_idx >= len(lines):
        return RefactorResult(False, "skipped-no-handler", backup_path)

    body_indent = _indent_of(lines[body_idx])
    if len(body_indent) <= len(if_indent):
        return RefactorResult(False, "skipped-no-handler", backup_path)

    # walk to the end of the if-block: first later line dedented back to
    # if_indent or less (or end of file)
    end_idx = len(lines)
    for j in range(body_idx + 1, len(lines)):
        stripped = lines[j].strip()
        if not stripped:
            continue
        j_indent = _indent_of(lines[j])
        if len(j_indent) <= len(if_indent):
            end_idx = j
            break

    lines.insert(end_idx, f"{body_indent}break\n")
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return RefactorResult(True, "auto", backup_path)


# ---- shared handler for every brace-based language ----
_BREAK_STMT = {
    "javascript": "break;", "java": "break;", "csharp": "break;",
    "cpp": "break;", "c": "break;", "go": "break", "rust": "break;",
}


def _apply_early_termination_brace_lang(file_path: str, hit: PatternHit, language: str) -> RefactorResult:
    backup_path = _backup(file_path)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    idx = hit.line_number - 1
    if idx >= len(lines):
        return RefactorResult(False, "skipped-no-handler", backup_path)
    line = lines[idx]
    if_indent = _indent_of(line)

    if not line.rstrip().endswith("{"):
        # not a same-line brace-opening `if` — not safe to blind-insert into
        return RefactorResult(False, "skipped-no-handler", backup_path)

    close_idx = None
    for j in range(idx + 1, len(lines)):
        if lines[j].rstrip() == f"{if_indent}}}":
            close_idx = j
            break
    if close_idx is None or close_idx == idx + 1:
        # no matching close found, or an empty block — not safe to blind-insert into
        return RefactorResult(False, "skipped-no-handler", backup_path)

    last_body_line = lines[close_idx - 1]
    if not last_body_line.strip():
        return RefactorResult(False, "skipped-no-handler", backup_path)
    body_indent = _indent_of(last_body_line)
    if len(body_indent) <= len(if_indent):
        return RefactorResult(False, "skipped-no-handler", backup_path)

    lines.insert(close_idx, f"{body_indent}{_BREAK_STMT.get(language, 'break;')}\n")
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return RefactorResult(True, "auto", backup_path)


# ===========================================================================
# avoid_redundant_computation
# ===========================================================================

# ---- python (tested) ----
def _apply_avoid_redundant_computation_python(file_path: str, hit: PatternHit) -> RefactorResult:
    backup_path = _backup(file_path)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    call_text = hit.snippet.strip()
    hit_idx = hit.line_number - 1
    if hit_idx >= len(lines) or call_text not in lines[hit_idx]:
        return RefactorResult(False, "skipped-no-handler", backup_path)
    hit_indent = _indent_of(lines[hit_idx])

    loop_idx = None
    for j in range(hit_idx - 1, -1, -1):
        stripped = lines[j].strip()
        if not stripped:
            continue
        j_indent = _indent_of(lines[j])
        if len(j_indent) < len(hit_indent) and re.match(r"for\s+\w+\s+in\s+", stripped):
            loop_idx = j
            break
        if len(j_indent) < len(hit_indent) and not stripped.startswith(("for ", "if ", "elif ", "else")):
            break
    if loop_idx is None:
        return RefactorResult(False, "skipped-no-handler", backup_path)

    loop_indent = _indent_of(lines[loop_idx])
    safe_name = re.sub(r"[^a-zA-Z0-9_]", "_", call_text).strip("_")[:40]
    temp_var = f"_hoisted_{safe_name}"

    end_idx = len(lines)
    for j in range(loop_idx + 1, len(lines)):
        stripped = lines[j].strip()
        if not stripped:
            continue
        j_indent = _indent_of(lines[j])
        if len(j_indent) <= len(loop_indent):
            end_idx = j
            break

    replaced_any = False
    for j in range(loop_idx + 1, end_idx):
        if call_text in lines[j]:
            lines[j] = lines[j].replace(call_text, temp_var)
            replaced_any = True
    if not replaced_any:
        return RefactorResult(False, "skipped-no-handler", backup_path)

    lines.insert(loop_idx, f"{loop_indent}{temp_var} = {call_text}\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return RefactorResult(True, "auto", backup_path)


# ---- shared handler for every other language ----
_VAR_DECL_TEMPLATES = {
    "javascript": "const {v} = {c};",
    "java": "var {v} = {c};",
    "csharp": "var {v} = {c};",
    "cpp": "auto {v} = {c};",
    "c": "__auto_type {v} = {c}; /* GNU C extension (gcc/clang) */",
    "go": "{v} := {c}",
    "rust": "let {v} = {c};",
}
_STRUCTURAL_KW_RE = re.compile(r"^\s*(for|foreach|if|else\s+if|elif|else|while|switch|case|try|catch)\b")


def _apply_avoid_redundant_computation_generic(file_path: str, hit: PatternHit, language: str) -> RefactorResult:
    backup_path = _backup(file_path)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    call_text = hit.snippet.strip()
    hit_idx = hit.line_number - 1
    if hit_idx >= len(lines) or call_text not in lines[hit_idx]:
        return RefactorResult(False, "skipped-no-handler", backup_path)
    hit_indent = _indent_of(lines[hit_idx])

    loop_re = re.compile(LOOP_KEYWORDS.get(language, r"for\s*\("))
    loop_idx = None
    for j in range(hit_idx - 1, -1, -1):
        stripped = lines[j].strip()
        if not stripped:
            continue
        j_indent = _indent_of(lines[j])
        if len(j_indent) < len(hit_indent) and loop_re.search(lines[j]):
            loop_idx = j
            break
        if len(j_indent) < len(hit_indent) and not _STRUCTURAL_KW_RE.match(stripped):
            break
    if loop_idx is None:
        return RefactorResult(False, "skipped-no-handler", backup_path)

    loop_indent = _indent_of(lines[loop_idx])
    safe_name = re.sub(r"[^a-zA-Z0-9_]", "_", call_text).strip("_")[:40]
    temp_var = f"_hoisted_{safe_name}"

    end_idx = len(lines)
    for j in range(loop_idx + 1, len(lines)):
        stripped = lines[j].strip()
        if not stripped:
            continue
        j_indent = _indent_of(lines[j])
        if len(j_indent) <= len(loop_indent):
            end_idx = j
            break

    replaced_any = False
    for j in range(loop_idx + 1, end_idx):
        if call_text in lines[j]:
            lines[j] = lines[j].replace(call_text, temp_var)
            replaced_any = True
    if not replaced_any:
        return RefactorResult(False, "skipped-no-handler", backup_path)

    decl_template = _VAR_DECL_TEMPLATES.get(language)
    if not decl_template:
        return RefactorResult(False, "skipped-no-handler", backup_path)
    decl = decl_template.format(v=temp_var, c=call_text)
    lines.insert(loop_idx, f"{loop_indent}{decl}\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return RefactorResult(True, "auto", backup_path)


# ===========================================================================
# batch_operations: intentionally NEVER auto-applied, for any language —
# see module docstring. Always falls through to _flag_only via apply_pattern.
# ===========================================================================

PATTERN_HANDLERS = {
    ("cache_reuse", "python"): _apply_cache_python,
    ("cache_reuse", "javascript"): _apply_cache_javascript,
    ("cache_reuse", "java"): _apply_cache_java,
    ("cache_reuse", "csharp"): _apply_cache_csharp,
    ("cache_reuse", "cpp"): _apply_cache_cpp,
    ("cache_reuse", "c"): _apply_cache_c,
    ("cache_reuse", "go"): _apply_cache_go,
    # ("cache_reuse", "rust") intentionally absent — see module docstring

    ("early_termination", "python"): _apply_early_termination_python,
    ("early_termination", "javascript"): lambda fp, h: _apply_early_termination_brace_lang(fp, h, "javascript"),
    ("early_termination", "java"): lambda fp, h: _apply_early_termination_brace_lang(fp, h, "java"),
    ("early_termination", "csharp"): lambda fp, h: _apply_early_termination_brace_lang(fp, h, "csharp"),
    ("early_termination", "cpp"): lambda fp, h: _apply_early_termination_brace_lang(fp, h, "cpp"),
    ("early_termination", "c"): lambda fp, h: _apply_early_termination_brace_lang(fp, h, "c"),
    ("early_termination", "go"): lambda fp, h: _apply_early_termination_brace_lang(fp, h, "go"),
    ("early_termination", "rust"): lambda fp, h: _apply_early_termination_brace_lang(fp, h, "rust"),

    ("avoid_redundant_computation", "python"): _apply_avoid_redundant_computation_python,
    ("avoid_redundant_computation", "javascript"): lambda fp, h: _apply_avoid_redundant_computation_generic(fp, h, "javascript"),
    ("avoid_redundant_computation", "java"): lambda fp, h: _apply_avoid_redundant_computation_generic(fp, h, "java"),
    ("avoid_redundant_computation", "csharp"): lambda fp, h: _apply_avoid_redundant_computation_generic(fp, h, "csharp"),
    ("avoid_redundant_computation", "cpp"): lambda fp, h: _apply_avoid_redundant_computation_generic(fp, h, "cpp"),
    ("avoid_redundant_computation", "c"): lambda fp, h: _apply_avoid_redundant_computation_generic(fp, h, "c"),
    ("avoid_redundant_computation", "go"): lambda fp, h: _apply_avoid_redundant_computation_generic(fp, h, "go"),
    ("avoid_redundant_computation", "rust"): lambda fp, h: _apply_avoid_redundant_computation_generic(fp, h, "rust"),

    # batch_operations is intentionally NEVER auto-applied for any language —
    # turning a per-item I/O call into a batched one requires knowing the
    # specific bulk API (bulk_insert, executemany, Promise.all, etc.), which
    # differs per library and isn't safely guessable from the call site alone.
    # It stays flagged-only everywhere; write a repo-specific handler here
    # only once you've confirmed the actual bulk API that repo's dependency exposes.
}


COMMENT_PREFIX = {
    "python": "#", "rust": "//", "go": "//", "javascript": "//",
    "java": "//", "csharp": "//", "cpp": "//", "c": "//",
}


def _flag_only(file_path: str, language: str, hit: PatternHit) -> RefactorResult:
    backup_path = _backup(file_path)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    idx = hit.line_number - 1
    if idx < 0 or idx >= len(lines):
        return RefactorResult(False, "skipped-no-handler", backup_path)
    indent = _indent_of(lines[idx])
    prefix = COMMENT_PREFIX.get(language, "//")
    marker = f"{indent}{prefix} REFACTOR-CANDIDATE: {hit.pattern} - needs manual/LLM-assisted edit (see llm_review_agent.py)\n"
    lines.insert(idx, marker)
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return RefactorResult(True, "flagged-only", backup_path)


def apply_pattern(file_path: str, language: str, hit: PatternHit) -> RefactorResult:
    handler = PATTERN_HANDLERS.get((hit.pattern, language))
    if handler:
        result = handler(file_path, hit)
        if result.applied:
            return result
        # Handler declined (signature too complex / structure not confidently
        # matched). Bug fix vs. the original version: previously this case
        # returned "skipped-no-handler" straight through, leaving the file
        # completely untouched with no record that anything was skipped —
        # it would look identical to "no refactor needed" in the results.
        # Now it always falls back to a safe comment flag, consistent with
        # what happens for a (pattern, language) cell with no handler at all.
        return _flag_only(file_path, language, hit)
    return _flag_only(file_path, language, hit)
