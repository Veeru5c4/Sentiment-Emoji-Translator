## AI Summary & Sentiment/Emoji Translator

**Stack**: Python, FastAPI, Postgres (optional), Streamlit, OpenAI API  
**Features**:
- **Four-line summary** of up to a few pages of pasted text
- **Sentiment** classification: positive / neutral / negative
- **Highlight sentences with emojis** that drove the sentiment decision

---

### 1. Prerequisites

- Python 3.10+
- (Optional but recommended) Postgres instance
- An OpenAI API key (you can use your own, or configure a server key)

---

### 2. Setup

From the project root (`Intelex1`):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file (or export env vars in your shell) with at least:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
# or, if you prefer a project key:
# export OPENAI_PROJECT_KEY="your_project_level_openai_key_here"

# Optional: Postgres (if you want to persist analyses)
# export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/yourdb"

# Optional: Where the frontend is served from (for CORS)
# export FRONTEND_ORIGIN="http://localhost:8501"
```

If you prefer not to configure a server OpenAI key, users can instead provide their own key in the Streamlit UI; it is forwarded only for that request.

---

### 3. Run the FastAPI backend

From the project root:

```bash
uvicorn backend.main:app --reload --host localhost --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

API example:

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product! It has changed my life.", "api_key": null}'
```

---

### 4. Run the Streamlit frontend

In another terminal (with the same virtualenv active), from the project root:

```bash
export BACKEND_URL="http://localhost:8000"  # optional, this is the default
streamlit run frontend/app.py
```

Then open `http://localhost:8501` in your browser.

**Usage**:
- Paste up to a couple of pages of text into the big text box.
- Optionally enter your own OpenAI API key (or rely on the backend's env key).
- Click **“Analyze ✨”**.
- The app returns:
  - **Summary**: exactly four lines
  - **Sentiment**: positive / neutral / negative, with an emoji indicator
  - **Highlight sentences**: bullet list of key sentences each with an emoji

---

### 5. Notes on Postgres

- If `DATABASE_URL` is set, the backend will create an `analysis_results` table and store:
  - Input text
  - Summary
  - Sentiment
  - Highlight sentences (as JSON)
- If `DATABASE_URL` is **not** set, the API still works; it simply skips persistence.

---

### 6. Editing / Extending

- Core backend logic:
  - FastAPI app: `backend/main.py`
  - OpenAI integration: `backend/openai_client.py`
  - API route: `backend/routers/analysis.py`
- Data models:
  - Pydantic schemas: `backend/schemas.py`
  - SQLAlchemy ORM: `backend/models.py`
- Frontend:
  - Streamlit UI: `frontend/app.py`


# Sentiment-Emoji-Translator
