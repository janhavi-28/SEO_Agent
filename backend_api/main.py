# backend_api/main.py

from typing import List, Optional, Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Correct imports
from .campaign_builder import run_campaign_builder
from .seo_analyzer import run_seo_analyzer
from .keyword_research import run_keyword_research
from .performance_predictor import run_performance_forecast
from .content_calendar import run_content_calendar

app = FastAPI(title="AI Marketing & SEO Suite API")

# Allow all origins for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request Models
# -------------------------

class CampaignRequest(BaseModel):
    business_info: str
    campaign_goal: str
    product_info: str
    audience: str
    platforms: List[str]
    website_url: Optional[str] = None
    duration_weeks: Optional[int] = 4
    posts_per_week: Optional[int] = 3
    budget: Optional[float] = None
    seed_keywords: Optional[List[str]] = None


class SEORequest(BaseModel):
    url: str
    target_keywords: Optional[List[str]] = None


class KeywordRequest(BaseModel):
    business_info: str
    product_info: str
    audience: str
    seed_keywords: Optional[List[str]] = None


class PerformanceRequest(BaseModel):
    business_info: str
    campaign_goal: str
    platforms: List[str]
    budget: Optional[float] = None
    duration_weeks: Optional[int] = 4
    posts_per_week: Optional[int] = 3


class CalendarRequest(CampaignRequest):
    pass


# -------------------------
# API Endpoints
# -------------------------

@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/generate_campaign")
def generate_campaign(req: CampaignRequest):
    return {"campaign": run_campaign_builder(req.dict())}


@app.post("/api/seo_analyze")
def seo_analyze(req: SEORequest):
    return {"seo_report": run_seo_analyzer(req.url, req.target_keywords)}


@app.post("/api/keyword_research")
def keyword_research(req: KeywordRequest):
    return {
        "keyword_research": run_keyword_research(
            business_info=req.business_info,
            product_info=req.product_info,
            audience=req.audience,
            seed_keywords=req.seed_keywords,
        )
    }


@app.post("/api/performance_forecast")
def performance_forecast(req: PerformanceRequest):
    return {"performance_forecast": run_performance_forecast(req.dict())}


@app.post("/api/content_calendar")
def content_calendar(req: CalendarRequest):
    return {"content_calendar": run_content_calendar(req.dict())}
