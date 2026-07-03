# Basic config: adjust model/provider here
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # change to your model
CHROMA_PERSIST_DIR = "chroma_db"
TOP_K = 6
