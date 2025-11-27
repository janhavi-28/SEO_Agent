# backend_api/performance_predictor.py

from typing import Dict, Any, List

from .utils.gemini_client import generate_json


def run_performance_forecast(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Rough performance forecast using Gemini.
    This is qualitative + simple numeric ranges.
    """
    business = payload.get("business_info", "")
    goal = payload.get("campaign_goal", "")
    platforms: List[str] = payload.get("platforms", []) or []
    budget = payload.get("budget")
    duration_weeks = payload.get("duration_weeks")
    posts_per_week = payload.get("posts_per_week")

    system_msg = """
You are a cautious performance marketer.

You must output ONLY JSON with:
- summary: short explanation
- ctr_estimate: object with min/max percentage
- cpc_estimate: object with min/max in USD
- conversions_estimate: object with min/max integers
- caveats: list of bullets explaining uncertainty
"""

    user_msg = f"""
Business: {business}
Goal: {goal}
Platforms: {", ".join(platforms)}
Budget per month: {budget}
Duration (weeks): {duration_weeks}
Posts per week: {posts_per_week}
"""

    json_template = {
        "summary": "",
        "ctr_estimate": {"min": 0.0, "max": 0.0},
        "cpc_estimate": {"min": 0.0, "max": 0.0},
        "conversions_estimate": {"min": 0, "max": 0},
        "caveats": [],
    }

    return generate_json(system_msg, user_msg, json_template)
