import re
from typing import Dict, List, Set

# Canonicalization: collapse near-duplicates so the report is clean + honest
CANON = {
    # algorithms variants
    "algo": "algorithms",
    "algorithm": "algorithms",
    "algorithms": "algorithms",

    # real-time variants
    "real time": "real-time",
    "real-time": "real-time",
    "real time systems": "real-time systems",
    "real-time systems": "real-time systems",

    # multithreading variants
    "multithreaded": "multithreading",
    "multi-threaded": "multithreading",
    "multi threaded": "multithreading",
    "multithreaded programming": "multithreading",
    "multi-threaded programming": "multithreading",
    "multi threaded programming": "multithreading",
    "multithreading": "multithreading",
    "threading": "multithreading",
    "concurrency": "multithreading",

    # linux variants
    "linux/unix environments": "linux/unix",
    "linux unix environments": "linux/unix",
    "linux environments": "linux/unix",
    "linux/unix": "linux/unix",
    "unix": "linux/unix",
    "posix": "linux/unix",
    "linux": "linux/unix",

    # latency variants
    "ultra low latency": "ultra-low-latency",
    "ultra-low-latency": "ultra-low-latency",
    "low latency": "low-latency",
    "minimal latency": "low-latency",
    "low-latency": "low-latency",

    # throughput variants
    "high throughput": "high-throughput",
    "high-throughput": "high-throughput",

    # scale variants
    "large scale": "massive scale",
    "extreme scale": "massive scale",
    "massive scale": "massive scale",
    "big data": "massive scale",

    # minor cleanups
    "linux unix": "linux/unix",
}

# Synonyms: help matching when wording differs (honest “equivalents”)
SYNONYMS = {
    "multithreading": [
        "multi-threaded",
        "multi threaded",
        "multithreaded",
        "threading",
        "concurrency",
        "multi-threaded programming",
    ],
    "linux/unix": [
        "linux",
        "unix",
        "posix",
        "linux environments",
        "linux/unix environments",
    ],
    "data structures": [
        "data structures and algorithms",
        "data structures & algorithms",
        "dsa",
    ],
    "algorithms": [
        "algorithm",
        "algo",
    ],
    "real-time systems": [
        "real time systems",
        "real-time",
        "real time",
    ],
    "ultra-low-latency": [
        "ultra low latency",
        "low latency",
        "minimal latency",
        "low-latency",
    ],
    "high-throughput": [
        "high throughput",
        "throughput",
    ],
    "massive scale": [
        "large scale",
        "extreme scale",
        "big data",
        "hdfs",
        "mapreduce",
    ],
    "performance tuning": [
        "profiling",
        "benchmarking",
        "optimization",
        "optimisation",
    ],
    "market data": [
        "real-time market data",
        "tick data",
        "market feed",
    ],
}

# Phrases we can detect from bullets/coursework even if not in explicit skills
BULLET_PHRASES = [
    "event-driven",
    "queue",
    "throughput",
    "latency",
    "data structures",
    "algorithms",
    "software design",
    "networking",
    "tcp/ip",
    "dns",
    "operating systems",
    "linux",
    "unix",
    "hdfs",
    "hive",
    "mapreduce",
    "hadoop",
    "machine learning",
    "classification",
    "feature scaling",
]

def _norm(s: str) -> str:
    s = (s or "").strip().lower()
    # Keep + - / for tokens like c++ or linux/unix
    s = re.sub(r"[^a-z0-9+\-/ ]+", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return CANON.get(s, s)

def _set(items: List[str]) -> Set[str]:
    return {_norm(x) for x in items if isinstance(x, str) and x.strip()}

def _expand_terms_if_base_present(terms: Set[str]) -> Set[str]:
    """If a base term is present, add its aliases."""
    expanded = set(terms)
    for base, aliases in SYNONYMS.items():
        b = _norm(base)
        if b in expanded:
            for a in aliases:
                expanded.add(_norm(a))
    return expanded

def _add_base_if_alias_present(terms: Set[str]) -> Set[str]:
    """If an alias is present, also add the base term."""
    expanded = set(terms)
    for base, aliases in SYNONYMS.items():
        b = _norm(base)
        for a in aliases:
            if _norm(a) in expanded:
                expanded.add(b)
    return expanded

def _enrich_cv_terms_from_bullets(cv: Dict) -> Set[str]:
    """Pull signal terms from project bullets so we don’t rely only on the skills list."""
    bullet_terms: Set[str] = set()

    for p in cv.get("projects", []) or []:
        if not isinstance(p, dict):
            continue
        bullets = p.get("bullets", []) or []
        for b in bullets:
            b_n = (b or "").lower()
            for phrase in BULLET_PHRASES:
                if phrase in b_n:
                    bullet_terms.add(_norm(phrase))

    return bullet_terms

def _unique_sorted(items) -> List[str]:
    return sorted(set(items))

def score_match(jd: Dict, cv: Dict) -> Dict:
    # JD sets
    req = _set(jd.get("required_skills", []))
    pref = _set(jd.get("preferred_skills", []))
    keywords = _set(jd.get("key_keywords", []))
    red_flags = _set(jd.get("red_flags", []))

    # CV sets (skills + coursework + project technologies + bullet signals)
    cv_skills = _set(cv.get("skills", []))
    cv_course = _set(cv.get("coursework", []))

    project_tech = []
    for p in cv.get("projects", []) or []:
        if isinstance(p, dict):
            project_tech += p.get("technologies", []) or []
    cv_tech = _set(project_tech)

    cv_bullets = _enrich_cv_terms_from_bullets(cv)

    cv_all = cv_skills | cv_course | cv_tech | cv_bullets

    # Expand/normalize in both directions (aliases count)
    req = _add_base_if_alias_present(_expand_terms_if_base_present(req))
    pref = _add_base_if_alias_present(_expand_terms_if_base_present(pref))
    keywords = _add_base_if_alias_present(_expand_terms_if_base_present(keywords))
    red_flags = _add_base_if_alias_present(_expand_terms_if_base_present(red_flags))

    cv_all = _add_base_if_alias_present(_expand_terms_if_base_present(cv_all))

    #Hits/misses
    req_hit = req & cv_all
    pref_hit = pref & cv_all
    key_hit = keywords & cv_all
    rf_hit = red_flags & cv_all

    req_missing = sorted(req - cv_all)
    rf_missing = sorted(red_flags - cv_all)

    def pct(hit: Set[str], total: Set[str]) -> float:
        return (len(hit) / len(total)) if total else 0.0

    #Transparent weights (simple MVP)
    score = 0.0
    score += 60 * pct(req_hit, req)
    score += 15 * pct(pref_hit, pref)
    score += 15 * pct(key_hit, keywords)
    score += 10 * pct(rf_hit, red_flags)

    return {
        "score": int(round(min(100, score))),
        "required_hit": _unique_sorted(req_hit),
        "required_missing": _unique_sorted(req_missing),
        "keywords_hit": _unique_sorted(key_hit),
        "red_flags_missing": _unique_sorted(rf_missing),
    }
