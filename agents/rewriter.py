import json
from llm import call_llm


def _strip_fences(s: str) -> str:
    s = (s or "").strip()
    if s.startswith("```"):
        first_newline = s.find("\n")
        if first_newline != -1:
            s = s[first_newline + 1:]
        s = s.strip()
        if s.endswith("```"):
            s = s[:-3].strip()
    return s


def _extract_json_object(raw: str) -> str:
    s = _strip_fences(raw)
    start = s.find("{")
    end = s.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"No JSON object found:\n{s[:500]}")
    return s[start:end + 1]


def _try_load_json(raw: str) -> dict:
    return json.loads(_extract_json_object(raw))


def rewrite_cv(jd_data: dict, cv_data: dict, match_data: dict) -> dict:
    """
    Returns JSON with EXACT structure:
    {
      "headline": str,
      "summary": str,
      "project_bullets": [{"project": str, "bullets": [str]}],
      "skills": [str],
      "notes": [str]
    }
    """

    with open("prompts/rewriter.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    prompt = prompt.replace("{{JD_JSON}}", json.dumps(jd_data, indent=2, ensure_ascii=False))
    prompt = prompt.replace("{{CV_JSON}}", json.dumps(cv_data, indent=2, ensure_ascii=False))
    prompt = prompt.replace("{{MATCH_JSON}}", json.dumps(match_data, indent=2, ensure_ascii=False))

    raw = call_llm(prompt)
    data = _try_load_json(raw)

    out = {
        "headline": str(data.get("headline", "")).strip(),
        "summary": str(data.get("summary", "")).strip(),
        "project_bullets": data.get("project_bullets", []),
        "skills": data.get("skills", []),
        "notes": data.get("notes", []),
    }

    if not isinstance(out["project_bullets"], list):
        out["project_bullets"] = []
    if not isinstance(out["skills"], list):
        out["skills"] = []
    if not isinstance(out["notes"], list):
        out["notes"] = []


    # SAFETY CLAMP (prevents invented experience)
    
    BANNED_PHRASES = [
        "trading",
        "high-performance",
        "high performance",
        "low-latency",
        "low latency",
        "performance tuning",
        "ultra-low-latency",
        "ultra low latency",
        "real-time trading",
    ]

    headline_l = out["headline"].lower()
    summary_l = out["summary"].lower()

    for phrase in BANNED_PHRASES:
        if phrase in headline_l:
            out["headline"] = ""
            break

    for phrase in BANNED_PHRASES:
        if phrase in summary_l:
            out["summary"] = ""
            break

    return out
