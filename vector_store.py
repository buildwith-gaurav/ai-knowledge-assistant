import chromadb
from google import genai

from config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)

chroma_client = chromadb.PersistentClient(
    path="uploads/chroma_db"
)
collection = chroma_client.get_or_create_collection(
    name="documents"
)
def add_document(
    text: str,
    embedding: list[float],
    document_id: str
) -> None:
    """Store a document chunk and its embedding in ChromaDB."""

    collection.add(
        ids=[document_id],
        documents=[text],
        embeddings=[embedding]
    )

def add_chunks(chunks: list[str], source: str) -> None:
    """Generate embeddings and store chunks in ChromaDB."""

    ids = []
    embeddings = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)

        ids.append(f"{source}_chunk_{index}")
        embeddings.append(embedding)
        metadatas.append({
            "source": source,
            "chunk": index
        })

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )    
def search_documents(query: str, n_results: int = 5) -> list[str]:
    """Search for relevant document chunks using semantic + keyword relevance."""

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=15
    )

    documents = results["documents"][0]

    # Extract useful keywords from the question
    query_words = set(query.lower().split())

    scored_documents = []

    for document in documents:
        document_words = set(document.lower().split())

        # Count matching keywords
        keyword_matches = len(query_words.intersection(document_words))

        # Combine keyword relevance with document position
        scored_documents.append(
            (keyword_matches, document)
        )

    # Sort by keyword matches
    scored_documents.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [document for _, document in scored_documents[:n_results]]

def generate_embedding(text: str) -> list[float]:
    """Generate an embedding for the given text."""

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values

results = search_documents(
    "What is Agentic Artificial Intelligence?"
)

print("\nRelevant chunks:")

for i, result in enumerate(results, start=1):
    print(f"\n--- Chunk {i} ---")
    print(result)

