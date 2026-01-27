from llm import call_llm

def parse_cv(cv_text: str) -> str:
    with open("prompts/cv_parser.txt", "r", encoding="utf-8") as f:
        prompt = f.read().replace("{{CV}}", cv_text)
    return call_llm(prompt)
