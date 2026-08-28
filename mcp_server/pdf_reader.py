from pathlib import Path

from pypdf import PdfReader


def read_pdf_file(path: Path) -> str:
    """
    Read text from a PDF file and return its contents.
    """

    try:
        reader = PdfReader(path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    except Exception as error:
        raise ValueError(
            f"Unable to read PDF file: {path}"
        ) from error