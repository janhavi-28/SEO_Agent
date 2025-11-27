# backend_api/keyword_research.py

from typing import Dict, Any, List, Optional

from .utils.serp_client import google_search_news
from .utils.gemini_client import generate_json


def run_keyword_research(business_info: str,
                         product_info: str,
                         audience: str,
                         seed_keywords: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Combine SerpAPI (if available) + Gemini suggestions.
    """
    seed_keywords = seed_keywords or []

    # Get some competitor / SERP context if SerpAPI key is present
    serp_results = google_search_news(
        query=f"{product_info} {audience}",
        num_results=5,
    )

    system_msg = """
You are an SEO keyword strategist.

You must return ONLY valid JSON with:
- core_keywords: list of primary intent keywords
- long_tail_keywords: list of long-tail variants
- competitor_themes: list of topic themes from competitors
"""

    serp_snippets = [
        r.get("title", "") + " - " + r.get("snippet", "")
        for r in serp_results
    ]

    user_msg = f"""
Business: {business_info}
Product: {product_info}
Audience: {audience}
Seed keywords: {", ".join(seed_keywords)}

Top SERP snippets:
{chr(10).join(serp_snippets)}
"""

    json_template = {
        "core_keywords": [],
        "long_tail_keywords": [],
        "competitor_themes": [],
    }

    ai_keywords = generate_json(system_msg, user_msg, json_template)

    return {
        "serp_samples": serp_results,
        "ai_keywords": ai_keywords,
    }
