from llm import call_llm

def extract_jd(jd_text: str) -> str:
    with open("prompts/jd_extractor.txt", "r", encoding="utf-8") as f:
        prompt = f.read().replace("{{JD}}", jd_text)
    return call_llm(prompt)