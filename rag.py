from vector_store import search_documents
from services import generate_response


def answer_question(question: str) -> dict:
    """Retrieve relevant chunks and generate an answer."""

    # 1. Retrieve relevant document chunks
    relevant_chunks = search_documents(question, n_results=5)

    # 2. Create context
    context = "\n\n".join(
        chunk["text"] for chunk in relevant_chunks
    )

    # 3. Get source filenames
    sources = list(
        set(chunk["source"] for chunk in relevant_chunks)
    )

    # 4. Create prompt for Gemini
    prompt = f"""
Answer the question using only the context provided below.

Context:
{context}

Question:
{question}

If the answer is not present in the context, say:
"I could not find the answer in the uploaded documents."
"""

    # 5. Generate final answer
    answer = generate_response(prompt)

    # 6. Return answer and sources
    return {
        "answer": answer,
        "sources": sources
    }