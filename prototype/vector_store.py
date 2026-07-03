"""
Create a Chroma vector store using OpenAI embeddings via LangChain.
"""
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Chroma
from typing import List, Dict
from .config import CHROMA_PERSIST_DIR, TOP_K

def build_or_load_vectorstore(docs: List[Dict], persist_directory: str = CHROMA_PERSIST_DIR):
    texts = []
    metadatas = []
    for d in docs:
        texts.append(d["text"])
        metadatas.append({"source": d.get("source"), "page": d.get("page")})
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts(texts, embeddings, metadatas=metadatas, persist_directory=persist_directory)
    vectordb.persist()
    return vectordb

def query(vectordb, query_text: str, k: int = TOP_K):
    docs = vectordb.similarity_search(query_text, k=k)
    # return LangChain Document objects (text + metadata)
    return docs
