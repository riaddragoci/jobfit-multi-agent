from datetime import datetime


def make_markdown_report(
    jd: dict,
    cv: dict,
    match: dict,
    advice: dict | None = None,
    rewrite: dict | None = None,
) -> str:

    role = jd.get("role_title", "Unknown role")
    seniority = jd.get("seniority_level", "unspecified")
    candidate = cv.get("candidate_name", "Candidate")

    lines = []
    lines.append("# Job ↔ CV Match Report")
    lines.append("")
    lines.append(f"**Candidate:** {candidate}")
    lines.append(f"**Role:** {role}")
    lines.append(f"**Seniority (from JD):** {seniority}")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    lines.append("## Match Score")
    lines.append(f"**{match.get('score', 0)} / 100**")
    lines.append("")

    lines.append("## Interpretation Notes")
    lines.append("- This score reflects alignment to the specific JD, not overall ability.")
    lines.append("- Low scores are common for highly specialized roles.")
    lines.append("- Missing items are treated as gaps; no experience is assumed.")
    lines.append("")

    lines.append("## Strong Matches")
    for x in match.get("required_hit", []) or ["None detected"]:
        lines.append(f"- {x}")
    lines.append("")

    lines.append("## Missing Requirements")
    for x in match.get("required_missing", []) or ["None"]:
        lines.append(f"- {x}")
    lines.append("")

    lines.append("## Red Flags Missing")
    for x in match.get("red_flags_missing", []) or ["None"]:
        lines.append(f"- {x}")
    lines.append("")

    lines.append("## Advice")
    if advice:
        lines.append(advice.get("summary", ""))
        lines.append("")

        for section, key, limit in [
            ("Strengths", "strengths", 6),
            ("Gaps", "gaps", 8),
            ("Next actions", "next_actions", 6),
        ]:
            items = advice.get(key, [])
            if items:
                lines.append(f"**{section}**")
                for i in items[:limit]:
                    lines.append(f"- {i}")
                lines.append("")
    else:
        lines.append("- Advice agent not run.")
        lines.append("")

    # CV Rewrite section
    if rewrite:
        lines.append("## CV Rewrite (aligned wording, no invented experience)")
        if rewrite.get("headline"):
            lines.append(f"**Headline:** {rewrite['headline']}")
        if rewrite.get("summary"):
            lines.append("")
            lines.append(rewrite["summary"])
        lines.append("")

        for item in rewrite.get("project_bullets", []):
            lines.append(f"**{item.get('project')}**")
            for b in item.get("bullets", [])[:5]:
                lines.append(f"- {b}")
            lines.append("")

        if rewrite.get("skills"):
            lines.append("**Skills (cleaned)**")
            for s in rewrite["skills"][:20]:
                lines.append(f"- {s}")
            lines.append("")

        if rewrite.get("notes"):
            lines.append("**Notes (not claimed)**")
            for n in rewrite["notes"][:8]:
                lines.append(f"- {n}")
            lines.append("")

    return "\n".join(lines)
