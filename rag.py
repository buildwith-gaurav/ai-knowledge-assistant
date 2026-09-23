from vector_store import search_documents
from services import generate_response


def answer_question(question: str) -> str:
    """Retrieve relevant chunks and generate an answer."""

    # 1. Retrieve relevant document chunks
    relevant_chunks = search_documents(question, n_results=5)

    # 2. Combine chunks into one context
    context = "\n\n".join(relevant_chunks)

    # 3. Create prompt for Gemini
    prompt = f"""
Answer the question using only the context provided below.

Context:
{context}

Question:
{question}

If the answer is not present in the context, say:
"I could not find the answer in the uploaded documents."
"""

    # 4. Generate final answer
    answer = generate_response(prompt)

    return answer