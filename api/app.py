from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shutil
import uuid
from pathlib import Path

from prototype.ingest import ingest_dir
from prototype.vector_store import build_or_load_vectorstore, query
from prototype.evaluator import evaluate_single
from prototype.app import SAMPLE_CRITERIA, PROGRAM_CONTEXT

UPLOAD_DIR = "sample_docs"

app = Flask(__name__)
CORS(app)

@app.route("/api/ping")
def ping():
    return "pong"

@app.route("/api/evaluate", methods=["POST"])  # multipart/form-data files under 'files'
def evaluate():
    # clear upload dir
    if os.path.isdir(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    for f in files:
        filename = f.filename
        save_path = os.path.join(UPLOAD_DIR, filename)
        f.save(save_path)

    # Ingest
    docs = ingest_dir(UPLOAD_DIR)

    # Use a temp chroma dir per run to avoid collisions
    tmp_chroma = f"chroma_db_{uuid.uuid4().hex}"
    vectordb = build_or_load_vectorstore(docs, persist_directory=tmp_chroma)

    results = []
    for c in SAMPLE_CRITERIA:
        retrieved = query(vectordb, c["text"])
        res = evaluate_single(c, PROGRAM_CONTEXT, retrieved)
        results.append(res)

    # cleanup chroma temp dir
    try:
        shutil.rmtree(tmp_chroma)
    except Exception:
        pass

    return jsonify(results)

@app.route("/api/report", methods=["GET"])
def get_report():
    path = Path("assessment_report.json")
    if not path.exists():
        return jsonify({"error": "No report found"}), 404
    return jsonify(path.read_text())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
