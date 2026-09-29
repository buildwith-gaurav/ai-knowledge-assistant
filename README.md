# AI Knowledge Assistant

An AI-powered Knowledge Assistant that allows users to upload PDF documents and ask questions about their content using Retrieval-Augmented Generation (RAG).

The system extracts text from uploaded PDFs, creates embeddings, stores them in ChromaDB, retrieves relevant document chunks for a user query, and uses Google Gemini to generate a context-aware answer.

---

## 🚀 Features

- 📄 Upload PDF documents
- 📚 Support for multiple PDF documents
- 🔍 Semantic document search
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔢 Gemini embeddings
- 🗄️ ChromaDB vector database
- 🤖 Google Gemini for answer generation
- 📌 Source tracking for retrieved documents
- ⚡ FastAPI REST API
- 📝 Automatic PDF text extraction
- ✂️ Document chunking
- 🔐 Environment variable based API key configuration

---

## 🏗️ Architecture

```text
                    PDF Document
                         │
                         ▼
                  PDF Text Extraction
                         │
                         ▼
                     Chunking
                         │
                         ▼
                 Gemini Embeddings
                         │
                         ▼
                    ChromaDB
                         │
                         │
User Question ───────────┘
      │
      ▼
Gemini Embedding
      │
      ▼
Similarity Search
      │
      ▼
Relevant Document Chunks
      │
      ▼
Context + Question
      │
      ▼
Google Gemini
      │
      ▼
Answer + Sources


🛠️ Tech Stack

Technology	            Purpose
Python	                Core programming language
FastAPI	                REST API backend
Google Gemini	        Embeddings and answer generation
ChromaDB	            Vector database
PyMuPDF	                PDF text extraction
python-dotenv	        Environment variable management
Uvicorn	                FastAPI server

-------------PROJET STRUCTURE-------------
ai-knowledge-assistant/
│
├── uploads/
│   └── PDF files
│
├── ├── uploads/
│   └── chroma_db/
│
├── config.py
├── document_processor.py
├── vector_store.py
├── rag.py
├── services.py
├── main.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md