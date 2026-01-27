import subprocess

MODEL = "llama3.1:8b"

def call_llm(prompt: str) -> str:
    p = subprocess.Popen(
        ["ollama", "run", MODEL],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    out, _ = p.communicate(prompt)
    return (out or "").strip()
