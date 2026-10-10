from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from document_processor import extract_text_from_pdf, split_text_into_chunks
from vector_store import add_chunks, clear_documents
from rag import answer_question


app = FastAPI()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "AI Knowledge Assistant is running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        return {
            "error": "Only PDF files are supported."
        }

    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)

    if not text.strip():
        return {
            "error": "Could not extract readable text from the PDF."
        }

    chunks = split_text_into_chunks(text)

    # Remove previously stored document chunks
    clear_documents()

    # Store chunks from the newly uploaded PDF
    add_chunks(chunks, file.filename)

    return {
        "message": "PDF uploaded and processed successfully",
        "filename": file.filename,
        "chunks": len(chunks)
    }


@app.post("/chat")
async def chat(question: str):

    # Check empty question
    if not question.strip():
        return {
            "error": "Question cannot be empty."
        }

    result = answer_question(question)

    return {
        "question": question,
        "answer": result["answer"],
        "sources": result["sources"]
    }