"""
High-level evaluation runner. For each ABET criterion:
- Retrieve top-k passages
- Build prompt (system + user)
- Call OpenAI chat completion and parse JSON
"""
import json
from typing import List, Dict
import openai
from .config import OPENAI_API_KEY, OPENAI_MODEL
from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

openai.api_key = OPENAI_API_KEY

def build_evidence_block(retrieved_docs: List):
    parts = []
    for d in retrieved_docs:
        text = d.page_content.strip()[:1500]  # truncate large chunks
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", 1)
        parts.append(f"---\nSource: {src} | Page: {page}\nExcerpt:\n{text}\n")
    return "\n".join(parts)

def call_model(system_prompt: str, user_prompt: str):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    resp = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.0,
        max_tokens=800,
    )
    return resp["choices"][0]["message"]["content"]

def evaluate_single(criterion: Dict, program_context: str, retrieved_docs: List):
    evidence_block = build_evidence_block(retrieved_docs)
    user_prompt = USER_PROMPT_TEMPLATE.format(
        criterion_id=criterion["id"],
        criterion_text=criterion["text"],
        program_context=program_context or "",
        evidence_block=evidence_block,
    )
    raw = call_model(SYSTEM_PROMPT, user_prompt)
    # Attempt to parse JSON. The model is instructed to return pure JSON.
    try:
        parsed = json.loads(raw)
    except Exception as e:
        # fallback: try to extract first '{...}' substring
        import re
        m = re.search(r"\{.*\}", raw, re.S)
        if m:
            parsed = json.loads(m.group(0))
        else:
            raise RuntimeError("Could not parse model output as JSON: " + str(e) + "\nRaw:\n" + raw)
    # attach retrieval metadata for audit
    parsed["_raw_model_output"] = raw
    parsed["_retrieved_docs"] = [{"source": d.metadata.get("source"), "page": d.metadata.get("page")} for d in retrieved_docs]
    return parsed
