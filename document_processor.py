import pymupdf


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""

    document = pymupdf.open(file_path)

    text = ""

    for page in document:
        page_text = page.get_text()

        if page_text:
            text += page_text + "\n"

    document.close()

    return text


def split_text_into_chunks(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[str]:
    """Split text into overlapping chunks while respecting paragraphs."""

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # Add paragraph to current chunk
        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += paragraph + "\n\n"

        else:
            # Save current chunk
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            # Start a new chunk
            current_chunk = paragraph + "\n\n"

    # Save the final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks