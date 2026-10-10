# AI Knowledge Assistant — RAG-Based PDF Question Answering

An AI-powered Knowledge Assistant that allows users to upload PDF documents and ask questions about their content through a simple web interface.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant document content and generate context-aware answers using Google Gemini.

## Features

- Upload PDF documents through a web interface.
- Extract text from PDF files using PyMuPDF.
- Split document text into chunks.
- Generate embeddings using the Gemini Embedding API.
- Store and retrieve document embeddings using ChromaDB.
- Perform semantic search to find relevant document content.
- Generate answers using Google Gemini.
- Display source document names with answers.
- Maintain recent conversation history.
- Provide a FastAPI backend and HTML/CSS/JavaScript frontend.
- Validate uploaded files and handle errors.
- Process one active PDF at a time; uploading a new PDF replaces the previously indexed document collection.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | REST API backend |
| Google Gemini API | Embeddings and answer generation |
| ChromaDB | Vector storage and similarity search |
| PyMuPDF | PDF text extraction |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend-backend communication |
| python-dotenv | Environment variable management |
| Uvicorn | ASGI server |

## Architecture

```text
PDF Upload
    |
    v
PDF Text Extraction
    |
    v
Text Chunking
    |
    v
Gemini Embeddings
    |
    v
ChromaDB Vector Storage

User Question
    |
    v
Question Embedding
    |
    v
Similarity Search
    |
    v
Relevant Document Chunks
    |
    v
Context + Question
    |
    v
Google Gemini
    |
    v
Answer + Source Documents
```

## Project Structure

```text
ai-knowledge-assistant/
|
|-- uploads/
|   |-- chroma_db/          # Local ChromaDB storage
|   |-- uploaded PDFs       # Ignored by Git
|
|-- frontend/               # If frontend files are stored here
|   |-- index.html
|   |-- style.css
|   |-- script.js
|
|-- config.py
|-- document_processor.py
|-- vector_store.py
|-- rag.py
|-- services.py
|-- main.py
|
|-- requirements.txt
|-- .env                    # Local API key; never commit
|-- .gitignore
|-- README.md
```

> Note: Adjust the frontend folder paths if `index.html`, `style.css`, and `script.js` are stored in the project root instead of `frontend/`.

## Prerequisites

- Python 3.10 or a compatible version supported by the installed dependencies.
- A Google Gemini API key.
- Git (optional, for cloning the repository).

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/buildwith-gaurav/ai-knowledge-assistant.git
cd ai-knowledge-assistant
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace `your_gemini_api_key` with your own API key.

**Never commit your API key or `.env` file to GitHub.**

### 5. Start the backend

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### 1. Upload a PDF

**Endpoint:** `POST /upload`

Uploads and processes a PDF document, extracts its text, creates chunks, generates embeddings, and stores them in ChromaDB.

The application supports one active document collection at a time. Uploading another PDF replaces the previously indexed collection.

### 2. Ask a Question

**Endpoint:** `POST /chat?question=YourQuestion`

Retrieves relevant content from the active PDF and generates an answer using Google Gemini.

The response contains:

- `question`: The submitted question.
- `answer`: The generated answer.
- `sources`: The source document names associated with retrieved content.

## How RAG Works

1. The user uploads a PDF.
2. PyMuPDF extracts its text.
3. The text is divided into chunks.
4. Gemini generates embeddings for the chunks.
5. ChromaDB stores the chunks and embeddings.
6. The user's question is converted into an embedding.
7. ChromaDB retrieves relevant chunks using similarity search.
8. The retrieved context and question are sent to Gemini.
9. Gemini generates an answer based on the supplied context.
10. The application returns the answer and source information.

## Limitations

- Only PDF documents are supported.
- Scanned PDFs may require OCR if they do not contain extractable text.
- Only one active PDF collection is maintained at a time.
- Answer quality depends on document text extraction and retrieval relevance.
- Gemini API availability and usage limits may affect response generation.
- Local ChromaDB data is stored on the machine running the application.

## Future Improvements

- Support multiple documents simultaneously.
- Improve chunking and retrieval accuracy.
- Add document deletion and management.
- Improve chat history management.
- Add OCR support for scanned PDFs.
- Deploy the application to a cloud platform.

## Security

- Store the Gemini API key in environment variables.
- Keep `.env` out of version control.
- Do not upload private documents or API keys to a public repository.

## Author

**Gaurav Kumar**

GitHub: https://github.com/buildwith-gaurav

## License

Add a license before distributing or reusing this project under an open-source license.
