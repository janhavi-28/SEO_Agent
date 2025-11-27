# backend_api/utils/gemini_client.py

import os
import json
from typing import Any, Dict

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY is not set in .env")

genai.configure(api_key=API_KEY)
_model = genai.GenerativeModel(MODEL_NAME)


# ----------------------------------------------------
# CLEAN JSON FROM GEMINI
# ----------------------------------------------------
def _clean_to_json(text: str) -> str:
    text = text.strip()

    text = text.replace("```json", "").replace("```", "").strip()

    if text.lower().startswith("json"):
        text = text[4:].lstrip()

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start : end + 1]

    return text


# ----------------------------------------------------
# WORKFLOW JSON TEMPLATE (Matches Your DOCX File)
# ----------------------------------------------------
WORKFLOW_JSON_TEMPLATE = {
    "1_business_understanding": {
        "business_info": "",
        "product_or_service": "",
        "value_proposition": "",
        "target_audience": ""
    },
    "2_campaign_strategy": {
        "goal": "",
        "positioning_strategy": "",
        "key_messages": ""
    },
    "3_ad_copywriting": {
        "facebook_ads": [],
        "instagram_ads": [],
        "email_marketing": []
    },
    "4_content_calendar": {
        "weekly_plan": [
            {"week": 1, "posts": []},
            {"week": 2, "posts": []},
            {"week": 3, "posts": []},
            {"week": 4, "posts": []}
        ]
    },
    "5_seo_research": {
        "primary_keywords": [],
        "long_tail_keywords": [],
        "keyword_difficulty_score": ""
    },
    "6_performance_prediction": {
        "expected_reach": "",
        "expected_clicks": "",
        "conversion_rate_estimate": ""
    },
    "7_final_recommendations": {
        "budget_split": "",
        "platform_priority": "",
        "risk_factors": "",
        "next_steps": ""
    }
}


# ----------------------------------------------------
# SYSTEM PROMPT (Matches Your Workflow)
# ----------------------------------------------------
WORKFLOW_SYSTEM_PROMPT = """
You are an AI Marketing Workflow Generator.
Always respond ONLY in valid JSON.

Follow this exact 7-step workflow:

1. Business Understanding
2. Campaign Strategy
3. Ad Copywriting
4. Content Calendar
5. SEO Research
6. Performance Prediction
7. Final Recommendations

Rules:
- Do NOT add markdown.
- Do NOT add backticks.
- Do NOT add explanations.
- Only output JSON.
"""


# ----------------------------------------------------
# GENERATE JSON WITH TEMPLATE
# ----------------------------------------------------
def generate_json(
    user_prompt: str,
    system_prompt: str = WORKFLOW_SYSTEM_PROMPT,
    json_template: Dict[str, Any] = WORKFLOW_JSON_TEMPLATE,
    temperature: float = 0.4,
    max_tokens: int = 2048,
) -> Dict[str, Any]:

    template_str = json.dumps(json_template, indent=2)

    prompt = f"""
{system_prompt.strip()}

You MUST obey these rules:
1. Respond ONLY with valid JSON.
2. Use exactly this JSON structure:

{template_str}

USER REQUEST:
{user_prompt}
""".strip()

    resp = _model.generate_content(
        prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        },
    )

    raw_text = resp.text or ""
    cleaned = _clean_to_json(raw_text)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "error": "❌ Failed to parse Gemini response as JSON",
            "raw_response": raw_text,
        }
