"""
BhashaAI — Document Processor
Extract text from TXT, PDF, and DOCX files for translation.
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def extract_text_from_txt(file_content: bytes, encoding: str = "utf-8") -> str:
    """Extract text from a plain text file."""
    try:
        return file_content.decode(encoding)
    except UnicodeDecodeError:
        # Fallback to latin-1
        return file_content.decode("latin-1", errors="replace")


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from a PDF file using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        logger.error("PyMuPDF not installed. Run: pip install PyMuPDF")
        return "[Error: PyMuPDF not installed]"

    try:
        doc = fitz.open(stream=file_content, filetype="pdf")
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        return "\n\n".join(text_parts)
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return f"[Error extracting PDF: {e}]"


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from a DOCX file using python-docx."""
    try:
        from docx import Document
        import io
    except ImportError:
        logger.error("python-docx not installed. Run: pip install python-docx")
        return "[Error: python-docx not installed]"

    try:
        doc = Document(io.BytesIO(file_content))
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n\n".join(paragraphs)
    except Exception as e:
        logger.error(f"DOCX extraction error: {e}")
        return f"[Error extracting DOCX: {e}]"


def extract_text(file_content: bytes, filename: str) -> str:
    """Auto-detect file format and extract text.

    Args:
        file_content: Raw bytes of the uploaded file
        filename: Original filename (used to detect extension)

    Returns:
        Extracted text string
    """
    ext = Path(filename).suffix.lower()

    if ext == ".txt":
        return extract_text_from_txt(file_content)
    elif ext == ".pdf":
        return extract_text_from_pdf(file_content)
    elif ext in (".docx", ".doc"):
        return extract_text_from_docx(file_content)
    else:
        # Try as plain text
        logger.warning(f"Unknown file extension '{ext}', treating as plain text.")
        return extract_text_from_txt(file_content)
