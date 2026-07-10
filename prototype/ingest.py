"""
Simple ingestion: load PDF, DOCX, TXT files from sample_docs/ and produce documents
with metadata (filename, page).
"""
import os
from typing import List, Dict
from pypdf import PdfReader
import docx

def load_pdf(path: str) -> List[Dict]:
    out = []
    reader = PdfReader(path)
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        out.append({"text": text, "source": os.path.basename(path), "page": i})
    return out

def load_docx(path: str) -> List[Dict]:
    doc = docx.Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    text = "\n".join(paragraphs)
    return [{"text": text, "source": os.path.basename(path), "page": 1}]

def load_txt(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return [{"text": text, "source": os.path.basename(path), "page": 1}]

def ingest_dir(dir_path: str = "sample_docs") -> List[Dict]:
    docs = []
    if not os.path.isdir(dir_path):
        return docs
    for fn in os.listdir(dir_path):
        path = os.path.join(dir_path, fn)
        if fn.lower().endswith(".pdf"):
            docs.extend(load_pdf(path))
        elif fn.lower().endswith(".docx"):
            docs.extend(load_docx(path))
        elif fn.lower().endswith(".txt"):
            docs.extend(load_txt(path))
    return docs

if __name__ == "__main__":
    docs = ingest_dir()
    print(f"Ingested {len(docs)} document chunks")
