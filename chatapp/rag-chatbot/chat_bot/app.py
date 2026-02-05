import os
from fastapi import FastAPI
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CSV RAG Chatbot (Groq + Chroma)")
app.add_middleware(
    CORSMiddleware,
     allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



load_dotenv()

text_path = "data.txt"
model_name = "llama-3.1-8b-instant"
topk = 4

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise RuntimeError("GROQ_API_KEY not set")




loader = TextLoader(file_path=text_path)
documents = loader.load()


splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
docs = splitter.split_documents(documents)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
)


llm = ChatGroq(
    model=model_name,
    temperature=0
)


prompt = ChatPromptTemplate.from_template(
    """Answer using the context below.

Context:
{context}

Question:
{question}
"""
)

retriever = vectorstore.as_retriever(search_kwargs={"k": topk})

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(req: ChatRequest):
    result = rag_chain.invoke(req.question)
    return {"answer": result.content}



