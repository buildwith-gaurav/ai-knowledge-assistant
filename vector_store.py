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
def search_documents(
    query: str,
    n_results: int = 5
) -> list[dict]:
    """Search documents using semantic, keyword, and entity relevance."""

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=15
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    query_lower = query.lower()
    query_words = set(query_lower.split())

    scored_documents = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        document_lower = document.lower()
        document_words = set(document_lower.split())

        # 1. Keyword matching
        keyword_matches = len(
            query_words.intersection(document_words)
        )

        # 2. Semantic similarity
        semantic_score = 1 / (1 + distance)

        # 3. Exact phrase matching
        exact_phrase_score = 0

        if query_lower in document_lower:
            exact_phrase_score = 2

        # 4. Important entity/name matching
        entity_score = 0
        if "gaurav kumar" in query_lower and "gaurav kumar" in document_lower:
         entity_score += 5

        if "pranshu singh" in query_lower and "pranshu singh" in document_lower:
         entity_score += 5

        important_words = [
            word for word in query_words
            if len(word) > 3
            and word not in {
                "what",
                "which",
                "where",
                "when",
                "does",
                "have",
                "with",
                "from",
                "this",
                "that"
            }
        ]

        for word in important_words:
            if word in document_lower:
                entity_score += 1

        # Combined score
        final_score = (
            semantic_score * 0.5
            + keyword_matches * 0.2
            + exact_phrase_score * 1.0
            + entity_score * 0.3
        )

        scored_documents.append(
            (
                final_score,
                document,
                metadata
            )
        )

    scored_documents.sort(
        key=lambda x: x[0],
        reverse=True
    )

    selected_documents = scored_documents[:n_results]

    return [
        {
            "text": document,
            "source": metadata["source"]
        }
        for _, document, metadata in selected_documents
    ]
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

