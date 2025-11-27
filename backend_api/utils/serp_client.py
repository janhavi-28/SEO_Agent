# backend_api/utils/serp_client.py

import os
from typing import List, Dict, Any

import requests

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
SERPAPI_URL = "https://serpapi.com/search.json"


def google_search_news(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Simple Google search using SerpAPI.
    If SERPAPI_API_KEY is missing, returns an empty list instead of crashing.
    """
    if not SERPAPI_API_KEY:
        # Graceful fallback
        return []

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": num_results,
    }

    try:
        res = requests.get(SERPAPI_URL, params=params, timeout=15)
        res.raise_for_status()
        data = res.json()
        return data.get("organic_results", [])[:num_results]
    except Exception:
        return []
