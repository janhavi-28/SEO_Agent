# AI Marketing & SEO Suite

End-to-end AI-powered marketing and SEO assistant built with **Python**, **FastAPI**, **Streamlit**, **Gemini**, and **SerpAPI**.

## Features

- AI Campaign Builder
- SEO Analyzer
- Performance Predictor
- Keyword & Competitor Research
- Content Calendar Automation

## Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
```

Set environment variables:

```bash
export GEMINI_API_KEY="your_gemini_key"
export SERPAPI_API_KEY="your_serpapi_key"
```

Run backend:

```bash
uvicorn backend_api.main:app --reload --port 8000
```

Run frontend:

```bash
streamlit run app.py
```

Adjust and extend modules in `backend_api/` and the UI in `app.py` as needed.
