from fastapi import FastAPI, UploadFile, File
import shutil
import os

from document_processor import extract_text_from_pdf, split_text_into_chunks
from vector_store import add_chunks
from rag import answer_question


app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Knowledge Assistant is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)

    chunks = split_text_into_chunks(text)

    add_chunks(chunks, file.filename)

    return {
        "message": "PDF uploaded and processed successfully",
        "filename": file.filename,
        "chunks": len(chunks)
    }


@app.post("/chat")
async def chat(question: str):
    answer = answer_question(question)

    return {
        "question": question,
        "answer": answer
    }