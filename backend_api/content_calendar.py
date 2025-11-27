# backend_api/content_calendar.py

from typing import Dict, Any, List

from .utils.gemini_client import generate_json


def run_content_calendar(payload: Dict[str, Any]) -> Dict[str, Any]:
    business = payload.get("business_info", "")
    goal = payload.get("campaign_goal", "")
    product = payload.get("product_info", "")
    audience = payload.get("audience", "")
    platforms: List[str] = payload.get("platforms", []) or []
    duration_weeks = payload.get("duration_weeks", 4)
    posts_per_week = payload.get("posts_per_week", 3)

    system_msg = """
You are an AI content strategist creating a posting calendar.

Return ONLY JSON with:
- overview: short description
- weeks: list of week objects
Each week object:
  - week_number (int)
  - posts: list of posts, where each post has:
        - platform
        - title
        - description
        - suggested_format
"""

    user_msg = f"""
Business: {business}
Goal: {goal}
Product: {product}
Audience: {audience}
Platforms: {", ".join(platforms)}
Duration (weeks): {duration_weeks}
Posts per week: {posts_per_week}
"""

    json_template = {
        "overview": "",
        "weeks": [
            {
                "week_number": 1,
                "posts": [
                    {
                        "platform": "",
                        "title": "",
                        "description": "",
                        "suggested_format": "",
                    }
                ],
            }
        ],
    }

    return generate_json(system_msg, user_msg, json_template)
