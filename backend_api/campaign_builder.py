# backend_api/campaign_builder.py

from typing import Dict, Any

# Import the generate_json that already includes:
# - WORKFLOW_SYSTEM_PROMPT
# - WORKFLOW_JSON_TEMPLATE
from backend_api.utils.gemini_client import generate_json


def run_campaign_builder(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a full 7-step marketing workflow using Gemini JSON mode.
    This follows the workflow template defined inside gemini_client.py
    """

    # Extract user inputs
    business = payload.get("business_info", "")
    goal = payload.get("campaign_goal", "")
    product = payload.get("product_info", "")
    audience = payload.get("audience", "")
    platforms = payload.get("platforms", []) or []
    duration_weeks = payload.get("duration_weeks")
    posts_per_week = payload.get("posts_per_week")
    budget = payload.get("budget")
    website_url = payload.get("website_url")

    # The user prompt sent to Gemini
    user_msg = f"""
Business Information: {business}
Campaign Goal: {goal}
Product/Service: {product}
Target Audience: {audience}
Platforms to Use: {", ".join(platforms)}

Campaign Duration (weeks): {duration_weeks}
Posts per Week: {posts_per_week}
Monthly Budget: {budget}
Website URL: {website_url}

Generate a full 7-step marketing workflow including:
1. Business Understanding
2. Campaign Strategy
3. Ad Copywriting (platform-specific)
4. Content Calendar (4 weeks)
5. SEO Research (keywords + difficulty)
6. Performance Prediction (reach, clicks, conversions)
7. Final Recommendations (budget split, platform priority, risks, next steps)

Follow the JSON format EXACTLY like the template.
""".strip()

    # ---- IMPORTANT ----
    # The JSON template + system prompt are already inside generate_json()
    # so you only pass the user message:
    
    result = generate_json(user_prompt=user_msg)

    return result
