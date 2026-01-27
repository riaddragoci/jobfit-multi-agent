import json
from llm import call_llm

ALLOWED_KEYS = {"summary", "strengths", "gaps", "next_actions"}


# Parsing helpers (robust)

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

def _repair_json_with_llm(bad_json_text: str) -> dict:
    prompt = (
        "Fix the JSON below so it is valid JSON.\n"
        "Rules:\n"
        "- Return VALID JSON ONLY.\n"
        "- Do NOT add new keys.\n"
        "- Do NOT add new content.\n"
        "- Only fix syntax (missing commas/quotes/brackets).\n\n"
        f"JSON:\n{bad_json_text}\n"
    )
    fixed_raw = call_llm(prompt)
    return _try_load_json(fixed_raw)

def _force_json_only(text: str) -> dict:
    prompt = (
        "Return VALID JSON ONLY with EXACTLY these keys:\n"
        "summary (string), strengths (array of strings), gaps (array of strings), next_actions (array of strings).\n"
        "No markdown. No extra keys.\n\n"
        "Convert the following content into that JSON now:\n"
        f"{text}\n"
    )
    raw = call_llm(prompt)
    return _try_load_json(raw)


# Normalization helpers

def _as_list(x):
    if x is None:
        return []
    if isinstance(x, str):
        return [x]
    if isinstance(x, list):
        return x
    return []

def _normalize_next_actions(next_actions):
    """
    Force next_actions to list[str].
    If model returns dicts, convert them into readable strings.
    """
    out = []
    for item in _as_list(next_actions):
        if isinstance(item, str):
            s = item.strip()
            if s:
                out.append(s)
        elif isinstance(item, dict):
            deliverable = (item.get("deliverable") or item.get("action") or "").strip()
            evidence = _as_list(item.get("evidence_it_produces") or item.get("evidence"))
            evidence = [e for e in evidence if isinstance(e, str) and e.strip()]
            if deliverable and evidence:
                out.append(f"{deliverable} (evidence: {', '.join(evidence[:3])})")
            elif deliverable:
                out.append(deliverable)
        else:
            s = str(item).strip()
            if s:
                out.append(s)

    return out[:6]

def _finalise_advice(data: dict) -> dict:
    """
    Ensure stable schema and remove ANY unexpected keys (including suggested_projects).
    """
    if not isinstance(data, dict):
        data = {}

# Keep only allowed keys

    data = {k: v for k, v in data.items() if k in ALLOWED_KEYS}

    summary = (data.get("summary") or "").strip()

    strengths = [s.strip() for s in _as_list(data.get("strengths")) if isinstance(s, str) and s.strip()]
    gaps = [g.strip() for g in _as_list(data.get("gaps")) if isinstance(g, str) and g.strip()]
    next_actions = _normalize_next_actions(data.get("next_actions"))

    return {
        "summary": summary,
        "strengths": strengths[:6],
        "gaps": gaps[:8],
        "next_actions": next_actions
    }


# Public function
def generate_advice(jd_data: dict, cv_data: dict, match_data: dict) -> dict:
    with open("prompts/advice.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    prompt = prompt.replace("{{JD_JSON}}", json.dumps(jd_data, ensure_ascii=False, indent=2))
    prompt = prompt.replace("{{CV_JSON}}", json.dumps(cv_data, ensure_ascii=False, indent=2))
    prompt = prompt.replace("{{MATCH_JSON}}", json.dumps(match_data, ensure_ascii=False, indent=2))

    raw = call_llm(prompt)

    try:
        data = _try_load_json(raw)
    except (json.JSONDecodeError, ValueError):
        if "{" in (raw or "") and "}" in (raw or ""):
            bad_obj = _extract_json_object(raw)
            data = _repair_json_with_llm(bad_obj)
        else:
            data = _force_json_only(raw)

    return _finalise_advice(data)
