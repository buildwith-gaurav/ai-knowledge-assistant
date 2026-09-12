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
    """Split text into overlapping chunks."""

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks