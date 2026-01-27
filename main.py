import os
import json
import argparse
from datetime import datetime

from agents.jd_extractor import extract_jd
from agents.cv_parser import parse_cv
from agents.matcher import match
from agents.advice import generate_advice
from agents.rewriter import rewrite_cv

from utils import normalize_jd_json, normalize_cv_json, extract_skills_from_text
from report import make_markdown_report


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def write_json(path: str, obj: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Multi-agent JD ↔ CV matcher (Ollama)")
    parser.add_argument("--jd", default="data/jd.txt")
    parser.add_argument("--cv", default="data/cv.txt")
    parser.add_argument("--out", default="outputs")
    args = parser.parse_args()

    jd_text = read_file(args.jd)
    cv_text = read_file(args.cv)

    jd_data = normalize_jd_json(extract_jd(jd_text))
    cv_data = normalize_cv_json(parse_cv(cv_text))

    extra_skills = extract_skills_from_text(cv_text)
    cv_data["skills"] = sorted(set(cv_data.get("skills", [])).union(extra_skills))

    match_data = match(jd_data, cv_data)
    advice_data = generate_advice(jd_data, cv_data, match_data)
    rewrite_data = rewrite_cv(jd_data, cv_data, match_data)

    md = make_markdown_report(jd_data, cv_data, match_data, advice_data, rewrite_data)

    os.makedirs(args.out, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    write_text(os.path.join(args.out, f"report_{stamp}.md"), md)
    write_json(os.path.join(args.out, f"rewrite_{stamp}.json"), rewrite_data)

    print("\n✅ Generated report + rewritten CV\n")
    print(md)


if __name__ == "__main__":
    main()
