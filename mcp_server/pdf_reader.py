from pathlib import Path
from pypdf import PdfReader

MAX_PDF_FILE_SIZE = 10_000_000
MAX_PDF_PAGES = 100
MAX_EXTRACTED_TEXT = 1_000_000


def read_pdf_file(path: Path) -> str:
    """
    Read text from a PDF file within configured resource limits.
    """

    try:
        file_size = path.stat().st_size
    except (PermissionError, OSError) as error:
        raise ValueError(
            f"Unable to access PDF file: {path}"
        ) from error

    if file_size > MAX_PDF_FILE_SIZE:
        raise ValueError(
            f"PDF file is too large to read: {path}"
        )

    try:
        reader = PdfReader(path)

        if len(reader.pages) > MAX_PDF_PAGES:
            raise ValueError(
                f"PDF contains too many pages: {path}"
            )

        pages = []
        total_text_length = 0

        for page in reader.pages:
            text = page.extract_text() or ""

            total_text_length += len(text)

            if total_text_length > MAX_EXTRACTED_TEXT:
                raise ValueError(
                    f"Extracted PDF text is too large: {path}"
                )

            if text:
                pages.append(text)

        return "\n".join(pages)

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(
            f"Unable to read PDF file: {path}"
        ) from error