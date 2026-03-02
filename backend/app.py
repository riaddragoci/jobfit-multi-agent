import sys
import os
import json
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents.jd_extractor import extract_jd
from agents.cv_parser import parse_cv
from agents.matcher import match
from agents.advice import generate_advice
from agents.rewriter import rewrite_cv
from utils import normalize_jd_json, normalize_cv_json, extract_skills_from_text

app = FastAPI(
    title="CV JD Matcher API",
    description="Multi-agent CV and Job Description matching system powered by Ollama",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    cv_text: str
    jd_text: str


class AnalyzeResponse(BaseModel):
    jd_data: dict
    cv_data: dict
    match_data: dict
    advice_data: dict
    rewrite_data: dict


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    try:
        jd_data = normalize_jd_json(extract_jd(request.jd_text))
        cv_data = normalize_cv_json(parse_cv(request.cv_text))
        extra_skills = extract_skills_from_text(request.cv_text)
        cv_data["skills"] = sorted(set(cv_data.get("skills", [])).union(extra_skills))
        match_data = match(jd_data, cv_data)
        advice_data = generate_advice(jd_data, cv_data, match_data)
        rewrite_data = rewrite_cv(jd_data, cv_data, match_data)
        return AnalyzeResponse(
            jd_data=jd_data,
            cv_data=cv_data,
            match_data=match_data,
            advice_data=advice_data,
            rewrite_data=rewrite_data,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")