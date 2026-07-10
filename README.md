# ABET Readiness Reviewer — Starter Prototype

Overview
- Minimal prototype showing how to ingest program artifacts (PDF/DOCX/TXT), create a vector index, and run an LLM-backed evidence-grounded evaluation against specified ABET criteria.
- The LLM is used as an assistant that returns JSON with scores, justifications, evidence references, and recommended actions. Human sign-off is required.

Quickstart
1. Clone or copy this repo.
2. Create a folder `sample_docs/` and add PDFs/DOCX/TXT of self-study, syllabi, rubrics, assessment reports.
3. Create a Python venv and install dependencies:
   - export OPENAI_API_KEY="sk-..."
   - python -m venv .venv && source .venv/bin/activate
   - pip install -r requirements.txt
4. Run backend API:
   - cd repo root
   - FLASK_APP=api/app.py flask run --port 5000
5. Run the UI:
   - cd web
   - npm install
   - npm run dev

Notes
- The LLM will only be as reliable as the retrieval & prompts. The prototype enforces JSON + evidence citation, but you MUST review the outputs.
- Replace OpenAI model in `prototype/config.py` if you use other providers or local LLMs.

Next steps
- Add more robust ingestion (OCR), pagination-aware citations, multi-model agreement checks, and a UI for human review.
- If you want, I can push this to a GitHub repo for you and wire up a simple React UI.
