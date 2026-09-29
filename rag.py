from vector_store import search_documents
from services import generate_response


# Conversation memory
conversation_history = []


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

    # 4. Create conversation history
    history = "\n".join(
        f"User: {item['question']}\nAI: {item['answer']}"
        for item in conversation_history
    )

    # 5. Create prompt for Gemini
    prompt = f"""
Answer the question using only the context provided below.

Previous conversation:
{history}

Context:
{context}

Current question:
{question}

If the answer is not present in the context, say:
"I could not find the answer in the uploaded documents."
"""

    # 6. Generate final answer
    answer = generate_response(prompt)

# 7. Save conversation
    conversation_history.append({
    "question": question,
    "answer": answer
})

# Keep only the last 5 conversations
    if len(conversation_history) > 5:
     conversation_history.pop(0)

# 8. Return answer and sources
    return {
    "answer": answer,
    "sources": sources
}