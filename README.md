# JobFit Multi-Agent
### Evidence-Based Job Description ↔ CV Matcher with Advice & Safe Rewrite

JobFit Multi-Agent is a CLI tool that analyses how well a CV aligns with a Job Description using **multiple constrained AI agents** and **deterministic matching**.

It is designed to be:
- Honest (no invented skills)
- Evidence-based
- Reproducible
- Portfolio-ready

---

## What it does

Given a plain-text Job Description and CV, the tool:

1. Extracts structured data from the Job Description  
2. Parses the CV into structured JSON  
3. Computes an alignment score using deterministic matching  
4. Identifies **strong matches**, **missing requirements**, and **red flags**  
5. Generates **honest next actions** (no assumed experience)  
6. Produces a **safe CV rewrite** that rephrases existing content only  

> ❗ The system is explicitly designed to **not hallucinate experience**.

---

## Key Features

- Works with any `jd.txt` and `cv.txt`
- Multi-agent architecture (extract → parse → match → advise → rewrite)
- Deterministic scoring (repeatable results)
- Guardrails to prevent invented skills or tools
- Timestamped outputs for full reproducibility
- Generates both human-readable reports and machine-readable JSON

---

## Architecture Overview

┌────────────────────┐        ┌────────────────────────┐
│  Job Description   │───────▶│  JD Extractor Agent     │
└────────────────────┘        └──────────┬─────────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │ Matcher & Scorer │
                                └──────────┬───────┘
                                           │
        ┌────────────────────┐             │
        │      CV Text       │─────────────┘
        └──────────┬─────────┘
                   ▼
          ┌──────────────────┐
          │  CV Parser Agent │
          └──────────┬───────┘
                     ▼
              ┌──────────────────┐
              │  Advice Agent    │
              └──────────┬───────┘
                         ▼
              ┌──────────────────┐
              │ CV Rewrite Agent │
              └──────────┬───────┘
                         ▼
              ┌──────────────────┐
              │ Markdown Report  │
              └──────────────────┘


---

## Example Output

The tool generates a structured report like:

- Match score with interpretation
- Strong matches (evidence found)
- Missing requirements
- Red flags (hard constraints)
- Honest next actions
- Safe CV rewrite (no invented experience)

Example snippet:

Match Score: 38 / 100

Strong Matches:

C++

Java

Python

Missing Requirements:

Multithreading

Linux/Unix

Real-time systems


---

## Setup

### 1) Requirements

- Python 3.10+
- Ollama (local LLM runtime)

### 2) Install dependencies

```bash
pip install -r requirements.txt
3) Install Ollama and pull a model
ollama pull llama3.1:8b
(You can change the model inside llm.py.)

Quick Start (Demo)
Run using the provided sample files:

python main.py --jd data/sample_jd.txt --cv data/sample_cv.txt --out outputs
This will generate:

outputs/
├─ report_YYYYMMDD_HHMM.md
├─ jd_YYYYMMDD_HHMM.json
├─ cv_YYYYMMDD_HHMM.json
├─ match_YYYYMMDD_HHMM.json
├─ advice_YYYYMMDD_HHMM.json
└─ rewrite_YYYYMMDD_HHMM.json
Design Philosophy
This project intentionally does not:

Inflate match scores

Pretend missing skills exist

Rewrite CVs with invented tools or experience

Instead, it mirrors how strong candidates actually improve:

Identify gaps

Take targeted action

Rewrite truthfully

Use Cases
Portfolio project demonstrating applied AI + systems thinking

Honest CV/JD alignment analysis

Career planning with concrete next steps

Recruiter-style evaluation tooling

License
MIT License — free to use, modify, and distribute.

Author
Riad Dragoci
Final-year Software Engineering student
Built as a portfolio-quality AI systems project