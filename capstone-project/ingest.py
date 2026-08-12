"""
Ingestion pipeline: parses NIST/SEMATECH handbook PDFs into section-aware
chunks and loads them via dlt into a local DuckDB destination.

Usage:
    pip install pdfplumber dlt duckdb --break-system-packages
    python ingest.py
"""

import re
import uuid
from pathlib import Path

import pdfplumber
import dlt

DATA_DIR = Path("data")  # folder containing your 3 PDFs
PDF_FILES = [
    "ppc.pdf",  # Production Process Characterization
    "pmc.pdf",  # Process or Product Monitoring and Control
    "pmd.pdf",  # Process Modeling
]

# Matches headers like "6.3.1.1 Control Charts" or "2.1 What is EDA?"
SECTION_HEADER_RE = re.compile(
    r"^\s*(\d+\.\d+(?:\.\d+)*\.?)\s+([A-Z][^\n]{3,80})\s*$", re.MULTILINE
)

CHUNK_CHAR_LIMIT = 1200
CHUNK_OVERLAP = 200


def extract_pages(pdf_path: Path):
    """Yield (page_number, text) for each page in the PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                yield i, text


def split_by_headers(text: str):
    """Split page text into (section_title, body) using numbered headers.
    Falls back to a single ('', text) tuple if no headers are found."""
    matches = list(SECTION_HEADER_RE.finditer(text))
    if not matches:
        return [("", text)]

    sections = []
    for idx, m in enumerate(matches):
        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        title = f"{m.group(1)} {m.group(2)}".strip()
        body = text[start:end].strip()
        sections.append((title, body))
    return sections


def chunk_text(text: str, limit=CHUNK_CHAR_LIMIT, overlap=CHUNK_OVERLAP):
    """Fallback character-based chunking with overlap for long sections."""
    if len(text) <= limit:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + limit
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def is_low_quality(text: str) -> bool:
    """Filter out TOC pages and near-empty header-only fragments."""
    # TOC pages: many bracketed section references like [3.2.4.]
    bracket_refs = len(re.findall(r"\[\d+(?:\.\d+)*\.?\]", text))
    if bracket_refs >= 3:
        return True
    # Header-only fragments with little real content
    if len(text) < 150:
        return True
    return False


@dlt.resource(name="handbook_chunks", write_disposition="replace")
def handbook_chunks():
    for pdf_name in PDF_FILES:
        pdf_path = DATA_DIR / pdf_name
        if not pdf_path.exists():
            print(f"WARNING: {pdf_path} not found, skipping")
            continue

        source_doc = pdf_path.stem
        for page_num, page_text in extract_pages(pdf_path):
            for section_title, section_body in split_by_headers(page_text):
                for piece in chunk_text(section_body):
                    piece = piece.strip()
                    if is_low_quality(piece):  # skip near-empty fragments
                        continue
                    yield {
                        "chunk_id": str(uuid.uuid4()),
                        "source_doc": source_doc,
                        "page": page_num,
                        "section_title": section_title,
                        "text": piece,
                    }


def main():
    pipeline = dlt.pipeline(
        pipeline_name="handbook_ingestion",
        destination="duckdb",
        dataset_name="handbook_data",
    )
    load_info = pipeline.run(handbook_chunks())
    print(load_info)

    # Quick sanity check
    with pipeline.sql_client() as client:
        with client.execute_query(
            "SELECT COUNT(*) FROM handbook_data.handbook_chunks"
        ) as cur:
            count = cur.fetchone()[0]
    print(f"Total chunks ingested: {count}")


if __name__ == "__main__":
    main()