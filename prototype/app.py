"""
Simple CLI runner:
- Ingest sample_docs/
- Build index (Chroma)
- For configured ABET criteria, run evaluate_single and print JSON results.
"""
import json
from .ingest import ingest_dir
from .vector_store import build_or_load_vectorstore, query
from .evaluator import evaluate_single

SAMPLE_CRITERIA = [
    {"id": "SO-1", "text": "An ability to identify, formulate, and solve complex engineering problems by applying principles of engineering, science, and mathematics."},
    {"id": "SO-2", "text": "An ability to apply engineering design to produce solutions that meet specified needs."},
]

PROGRAM_CONTEXT = "BS in Computer Engineering, enrollment ~120, PEOs: industry-ready graduates…"

def main():
    print("Ingesting documents...")
    docs = ingest_dir("sample_docs")
    print(f"Ingested {len(docs)} chunks.")
    print("Building/Loading vector store...")
    vectordb = build_or_load_vectorstore(docs)
    results = []
    for c in SAMPLE_CRITERIA:
        print(f"Querying evidence for {c['id']}...")
        retrieved = query(vectordb, c["text"])
        print(f"Retrieved {len(retrieved)} passages.")
        print("Calling evaluator...")
        res = evaluate_single(c, PROGRAM_CONTEXT, retrieved)
        results.append(res)
        print(json.dumps(res, indent=2))
    # save a JSON report
    with open("assessment_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Report written to assessment_report.json")

if __name__ == "__main__":
    main()
