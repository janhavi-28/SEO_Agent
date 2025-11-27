# backend_api/seo_analyzer.py

from typing import Dict, Any, List, Optional
import requests
from bs4 import BeautifulSoup

from .utils.gemini_client import generate_json


def _fetch_html(url: str) -> Optional[str]:
    try:
        res = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        res.raise_for_status()
        return res.text
    except Exception:
        return None


def run_seo_analyzer(url: str, target_keywords: Optional[List[str]] = None) -> Dict[str, Any]:
    html = _fetch_html(url)

    basic_info = {
        "url": url,
        "has_html": bool(html),
    }

    title = ""
    meta_desc = ""
    h1 = ""

    if html:
        soup = BeautifulSoup(html, "html.parser")
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        desc_tag = soup.find("meta", attrs={"name": "description"})
        if desc_tag and desc_tag.get("content"):
            meta_desc = desc_tag["content"].strip()
        h1_tag = soup.find("h1")
        if h1_tag:
            h1 = h1_tag.get_text(strip=True)

    system_msg = """
You are an SEO expert. You will receive:
- Basic on-page info (title, meta description, H1)
- Optional target keywords

Return ONLY JSON with:
- high_level_score (0-100)
- issues (list of strings)
- recommendations (list of strings)
- suggested_title
- suggested_meta_description
"""

    user_msg = f"""
Page URL: {url}

Current title: {title}
Meta description: {meta_desc}
H1: {h1}

Target keywords: {", ".join(target_keywords or [])}
"""

    json_template = {
        "high_level_score": 0,
        "issues": [],
        "recommendations": [],
        "suggested_title": "",
        "suggested_meta_description": "",
    }

    ai_analysis = generate_json(system_msg, user_msg, json_template)

    return {
        "page_info": {
            "title": title,
            "meta_description": meta_desc,
            "h1": h1,
        },
        "ai_analysis": ai_analysis,
        "basic_info": basic_info,
    }
