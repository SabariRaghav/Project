import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

question = "What is a token?"

loader = TextLoader("llm_document.txt", encoding="utf-8")

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vector_store = FAISS.from_documents(
    chunks,
    embeddings
)

results = vector_store.similarity_search(
    question,
    k=3
)

context = "\n\n".join(
    r.page_content
    for r in results
)

from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline

pipe = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-1.5B-Instruct",
    max_new_tokens=200,
    temperature=0.3
)

llm = HuggingFacePipeline(pipeline=pipe)

prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""

answer = llm.invoke(prompt)

print(answer)