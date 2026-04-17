"""Route uploaded files to the correct text extractor."""
import os
import pdfplumber


def extract_text(file_path: str) -> tuple[str, float]:
    """
    Extract text from a PDF file.
    Returns (raw_text, confidence) where confidence is 1.0 for digital PDFs
    and 0.0 if no text could be extracted.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in (".pdf", ".jpg", ".jpeg", ".png"):
        return "", 0.0

    if ext == ".pdf":
        return _extract_pdf(file_path)

    # Image files — PaddleOCR skipped; return empty so extractor falls back to manual entry
    return "", 0.0


def _extract_pdf(file_path: str) -> tuple[str, float]:
    text_parts = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    except Exception:
        return "", 0.0

    raw_text = "\n".join(text_parts).strip()
    if not raw_text:
        return "", 0.0
    return raw_text, 1.0
