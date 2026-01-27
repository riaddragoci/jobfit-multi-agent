# JobFit Multi-Agent (JD ↔ CV Matcher + Advice + Safe Rewrite)

A multi-agent, evidence-based CLI tool that:
- Extracts structured data from a Job Description (JD)
- Parses a CV into structured JSON
- Computes an alignment score using deterministic matching
- Generates honest, practical next actions (no invented skills)
- Produces a constrained CV rewrite (anti-hallucination guardrails)

## Features
- Works with any `jd.txt` and `cv.txt`
- Timestamped outputs for reproducibility
- Outputs report + JSON artifacts (JD, CV, match, advice, rewrite)

## Setup

### Install Ollama + model
Install Ollama and pull a model (example):
```bash
ollama pull llama3.1:8b

## Run (Demo)
```bash
python main.py --jd data/sample_jd.txt --cv data/sample_cv.txt --out outputs
