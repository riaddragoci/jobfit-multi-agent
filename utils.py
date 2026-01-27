import json
import re

def _extract_json_object(raw: str) -> str:
    """
    Extract the first JSON object from a string.
    Handles cases where the model wraps JSON in ```json fences or adds extra text.
    """
    if not raw:
        raise ValueError("Empty LLM output")

    s = raw.strip()

    # Remove triple-backtick fences if present
    if s.startswith("```"):
        # remove the opening fence line (``` or ```json)
        first_newline = s.find("\n")
        if first_newline != -1:
            s = s[first_newline + 1:]
        # remove closing fence
        if s.strip().endswith("```"):
            s = s.strip()[:-3].strip()

    # Now find the first JSON object by locating the first '{' and last '}'
    start = s.find("{")
    end = s.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"Could not find JSON object in output:\n{s[:300]}")

    return s[start:end+1]

def normalize_jd_json(raw: str) -> dict:
    json_str = _extract_json_object(raw)
    data = json.loads(json_str)

    # Fix common key mistakes
    if "roles_title" in data and "role_title" not in data:
        data["role_title"] = data.pop("roles_title")

    # Ensure required keys exist
    data.setdefault("role_title", "")
    data.setdefault("seniority_level", "unspecified")
    data.setdefault("required_skills", [])
    data.setdefault("preferred_skills", [])
    data.setdefault("key_keywords", [])
    data.setdefault("responsibilities", [])
    data.setdefault("red_flags", [])

    return data


def normalize_cv_json(raw: str) -> dict:
    json_str = _extract_json_object(raw)
    data = json.loads(json_str)

    data.setdefault("candidate_name", "")
    data.setdefault("summary", "")
    data.setdefault("skills", [])
    data.setdefault("coursework", [])
    data.setdefault("projects", [])
    data.setdefault("experience", [])
    data.setdefault("achievements", [])

    return data

def extract_skills_from_text(cv_text: str) -> list[str]:
    """
    Lightweight skill extractor from raw CV text to catch tokens the LLM might miss (e.g., C++).
    """
    t = (cv_text or "").lower()

    skills = set()

    # Exact token checks
    if "c++" in t: skills.add("C++")
    if re.search(r"\bpython\b", t): skills.add("Python")
    if re.search(r"\bjava\b", t): skills.add("Java")
    if re.search(r"\brust\b", t): skills.add("Rust")
    if re.search(r"\bhadoop\b", t): skills.add("Hadoop")
    if re.search(r"\bhive\b", t): skills.add("Hive")
    if re.search(r"\bmapreduce\b", t): skills.add("MapReduce")
    if re.search(r"\blinux\b", t) or re.search(r"\bunix\b", t): skills.add("Linux/Unix")

    return sorted(skills)