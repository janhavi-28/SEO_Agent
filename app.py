import streamlit as st
import requests
import json
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Marketing & SEO Suite",
    layout="wide"
)

PAGES = [
    "Dashboard",
    "AI Campaign Builder",
    "SEO Analyzer",
    "Keyword & Competitor Research",
    "Performance Predictor",
    "Content Calendar Automation",
]

def call_api(endpoint: str, payload: dict | None = None, method: str = "post"):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method.lower() == "post":
            resp = requests.post(url, json=payload or {})
        else:
            resp = requests.get(url, params=payload or {})
        if resp.status_code != 200:
            st.error(f"API error {resp.status_code}: {resp.text}")
            return None
        return resp.json()
    except Exception as e:
        st.error(f"Failed to reach backend: {e}")
        return None

def dashboard_page():
    st.title("📊 AI Marketing & SEO Suite – Dashboard")
    st.markdown("Quick overview of your campaigns, SEO health, and forecasts.")
    col1, col2, col3, col4 = st.columns(4)
    for c, label in zip((col1,col2,col3,col4),
                        ("Active Campaigns","Average CTR","Avg Conversion Rate","Estimated ROI")):
        with c:
            st.metric(label, "—")
    st.info("Analytics wiring is stubbed. Connect to a DB or analytics service to make this live.")

def campaign_builder_page():
    st.title("🚀 AI Campaign Builder")

    with st.form("campaign_form"):
        col1, col2 = st.columns(2)
        with col1:
            goal = st.selectbox(
                "Campaign Goal",
                ["Drive Sales", "Increase Website Traffic", "Generate Leads", "Boost Brand Awareness"],
            )
            product = st.text_area("Product / Service Description", height=120)
            target_audience = st.text_area("Target Audience", height=120)
        with col2:
            platforms = st.multiselect(
                "Platforms",
                ["Facebook Ads", "Google Ads", "Instagram", "Email", "Landing Page", "LinkedIn"],
                default=["Facebook Ads","Instagram","Email"]
            )
            tone = st.selectbox(
                "Tone & Style",
                ["Professional", "Casual", "Friendly", "Bold", "Luxury", "Technical"],
            )
            language = st.text_input("Language", "English")
        submit = st.form_submit_button("Generate Campaign")

    if submit:
        if not product.strip():
            st.warning("Please describe your product/service.")
            return
        payload = {
            "goal": goal,
            "product_description": product,
            "target_audience": target_audience,
            "platforms": platforms,
            "tone": tone,
            "language": language,
        }
        with st.spinner("Generating campaign with AI..."):
            data = call_api("/api/generate_campaign", payload)
        if data:
            st.success("Campaign generated!")
            st.subheader("Campaign Overview")
            st.write(data.get("summary", ""))

            st.subheader("Assets")
            tabs = st.tabs(["Ad Copy", "Emails", "Social Posts", "Landing Page"])
            ad_copy = data.get("ad_copy", {})
            emails = data.get("emails", [])
            social_posts = data.get("social_posts", [])
            landing_page = data.get("landing_page", {})

            with tabs[0]:
                for platform, text in ad_copy.items():
                    st.markdown(f"#### {platform}")
                    st.write(text)
            with tabs[1]:
                for i, email in enumerate(emails, start=1):
                    st.markdown(f"#### Email #{i}")
                    st.write(email)
            with tabs[2]:
                for i, post in enumerate(social_posts, start=1):
                    st.markdown(f"#### Post #{i}")
                    st.write(post)
            with tabs[3]:
                st.markdown("### Landing Page Content")
                st.write(landing_page.get("headline",""))
                st.write(landing_page.get("subheadline",""))
                st.write(landing_page.get("sections",""))

            st.download_button(
                "Download JSON",
                data=json.dumps(data, indent=2),
                file_name="campaign.json",
                mime="application/json",
            )

def seo_analyzer_page():
    st.title("🕵️ SEO Analyzer")
    url = st.text_input("Website URL to scan", placeholder="https://example.com")
    depth = st.slider("Crawl depth (number of pages to follow)", 1, 3, 1)
    if st.button("Run SEO Audit"):
        if not url.strip():
            st.warning("Please enter a URL")
            return
        payload = {"url": url, "depth": depth}
        with st.spinner("Running SEO audit..."):
            data = call_api("/api/seo_analyze", payload)
        if data:
            st.success("SEO audit complete!")
            st.subheader("Summary")
            st.write(data.get("summary",""))

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Technical Issues")
                for issue in data.get("technical_issues", []):
                    st.write(f"- {issue}")
            with col2:
                st.markdown("### Content Issues")
                for issue in data.get("content_issues", []):
                    st.write(f"- {issue}")

            st.markdown("### Detailed Findings")
            st.json(data.get("details", {}))

def keyword_page():
    st.title("🔎 Keyword & Competitor Research")
    col1, col2 = st.columns(2)
    with col1:
        seed_keywords = st.text_area("Seed Keywords (comma separated)", "ai marketing, seo automation")
        region = st.text_input("Region / Country", "us")
        language = st.text_input("Language code", "en")
    with col2:
        competitor_domains = st.text_area("Competitor Domains (one per line)", "example.com")
        max_results = st.slider("Max keywords", 10, 100, 30)

    if st.button("Run Research"):
        payload = {
            "seed_keywords": [k.strip() for k in seed_keywords.split(",") if k.strip()],
            "region": region,
            "language": language,
            "competitor_domains": [d.strip() for d in competitor_domains.splitlines() if d.strip()],
            "max_results": max_results,
        }
        with st.spinner("Querying search data via SerpAPI..."):
            data = call_api("/api/keyword_research", payload)
        if data:
            st.success("Research complete!")
            st.subheader("Keyword Suggestions")
            st.table(data.get("keywords", []))

            st.subheader("Keyword Gaps")
            st.table(data.get("keyword_gaps", []))

            st.subheader("Competitor Rankings")
            st.table(data.get("competitors", []))

def performance_page():
    st.title("📈 Performance Predictor")
    st.markdown("Paste or upload your campaign JSON to estimate CTR, conversions, and ROI.")

    uploaded = st.file_uploader("Upload campaign.json", type=["json"])
    raw = st.text_area("Or paste campaign JSON")
    payload_campaign = None

    if uploaded is not None:
        try:
            payload_campaign = json.load(uploaded)
        except Exception as e:
            st.error(f"Invalid JSON file: {e}")
    elif raw.strip():
        try:
            payload_campaign = json.loads(raw)
        except Exception as e:
            st.error(f"Invalid JSON in text: {e}")

    if st.button("Predict Performance"):
        if not payload_campaign:
            st.warning("Please provide a valid campaign JSON.")
            return
        with st.spinner("Predicting performance using AI..."):
            data = call_api("/api/predict_performance", {"campaign": payload_campaign})
        if data:
            st.success("Prediction ready!")
            st.json(data)

def calendar_page():
    st.title("🗓 Content Calendar Automation")
    goal = st.text_input("Primary campaign goal", "Increase brand awareness")
    audience = st.text_input("Target audience", "Solo founders and small business owners")
    topics = st.text_area("Core topics (comma separated)", "ai marketing, seo, automation")
    duration = st.slider("Number of days", 7, 60, 30)

    if st.button("Generate Calendar"):
        payload = {
            "goal": goal,
            "audience": audience,
            "topics": [t.strip() for t in topics.split(",") if t.strip()],
            "days": duration,
        }
        with st.spinner("Generating calendar with Gemini..."):
            data = call_api("/api/content_calendar", payload)
        if data:
            st.success("Calendar generated!")
            st.subheader("Preview")
            st.table(data.get("calendar", []))
            st.download_button(
                "Download CSV",
                data=data.get("csv",""),
                file_name="content_calendar.csv",
                mime="text/csv",
            )

def main():
    st.sidebar.title("AI Marketing & SEO Suite")
    page = st.sidebar.radio("Navigation", PAGES)
    if page == "Dashboard":
        dashboard_page()
    elif page == "AI Campaign Builder":
        campaign_builder_page()
    elif page == "SEO Analyzer":
        seo_analyzer_page()
    elif page == "Keyword & Competitor Research":
        keyword_page()
    elif page == "Performance Predictor":
        performance_page()
    elif page == "Content Calendar Automation":
        calendar_page()

if __name__ == "__main__":
    main()
